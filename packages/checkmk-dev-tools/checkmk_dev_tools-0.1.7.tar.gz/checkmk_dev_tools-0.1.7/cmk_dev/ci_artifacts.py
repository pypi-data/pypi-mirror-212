#!/usr/bin/env python3

"""Give information about and download named arguments from Nexus
"""

import hashlib
import logging
import os
import sys
import time
from argparse import ArgumentParser
from argparse import Namespace as Args
from collections.abc import Iterator, Mapping, Sequence
from configparser import ConfigParser
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from subprocess import check_output
from typing import TypeAlias, Union, cast

import yaml
from jenkins import Jenkins, JenkinsException

# pylint: disable=too-many-instance-attributes
# pylint: disable=fixme

GenMapVal: TypeAlias = Union[None, bool, str, float, int, "GenMapArray", "GenMap"]
GenMapArray: TypeAlias = Sequence[GenMapVal]
GenMap: TypeAlias = Mapping[str, GenMapVal]

PathHashes: TypeAlias = Mapping[str, str]
JobParams: TypeAlias = Mapping[str, int | str]


class Fatal(RuntimeError):
    """Rien ne va plus"""


def parse_args() -> Args:
    """Cool git like multi command argument parser"""
    parser = ArgumentParser("Provide CI artifacts locally")
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
        type=str.upper,
        default="INFO",
    )

    parser.set_defaults(func=lambda *_: parser.print_usage())
    subparsers = parser.add_subparsers(help="available commands", metavar="CMD")

    parser_info = subparsers.add_parser("info")
    parser_info.set_defaults(func=_fn_info)
    parser_info.add_argument(
        "job",
        help="Print some useful but informal information about a job",
        type=lambda a: a.strip(" /"),
    )

    parser_fetch = subparsers.add_parser("fetch")
    parser_fetch.set_defaults(func=_fn_fetch)
    parser_fetch.add_argument("job", type=str)
    parser_fetch.add_argument(
        "-c",
        "--credentials",
        type=split_params,
        help=(
            "Provide 'url', 'username' and 'password' "
            "or 'username_env', 'url_env' and 'password_env' respectively."
            " If no credentials are provided, the JJB config at "
            " ~/.config/jenkins_jobs/jenkins_jobs.ini is being used."
        ),
    )
    parser_fetch.add_argument(
        "-p",
        "--params",
        type=split_params,
        action="append",
    )
    parser_fetch.add_argument(
        "-d",
        "--dependency-paths",
        type=str,
        action="append",
        help=(
            "Provide list of files/directories git hashes should be compared against a build"
            "Important: provide the same relative directories as used in the respective build jobs!"
        ),
    )
    parser_fetch.add_argument(
        "-t",
        "--time-constraints",
        type=str,
        help=(
            "Provide a string (currently only 'today') which specifies the max age of a"
            " build to be considered valid."
        ),
    )
    parser_fetch.add_argument(
        "-b",
        "--base-dir",
        help="The base directory used to fetch directory/file hashes (see. --dependency-paths)",
        type=lambda p: Path(p).expanduser(),
    )
    parser_fetch.add_argument(
        "-o",
        "--out-dir",
        default="out",
        type=Path,
        help="Directory to put artifacts to - relative to --base-dir if relative",
    )
    parser_fetch.add_argument(
        "-n",
        "--omit-new-builds",
        action="store_true",
        help="Don't issue new builds, even if no matching build could be found",
    )

    return parser.parse_args()


def logger() -> logging.Logger:
    """Convenience function retrieves 'our' logger"""
    return logging.getLogger("ci-artifacts")


def split_params(string: str) -> Mapping[str, str]:
    """Splits a 'string packed map' into a dict
    >>> split_params("foo=23,bar=42")
    {'foo': '23', 'bar': '42'}
    """
    return {k: v for p in string.split(",") for k, v in (p.split("="),)}


@dataclass
class Build:
    """Models a Jenkins job build"""

    url: str
    number: int
    timestamp: datetime
    result: str
    building: str
    in_progress: bool
    parameters: GenMap
    path_hashes: Mapping[str, str]
    artifacts: list[str]

    def __init__(self, raw_build_info: GenMap):
        def params_from(build_info: GenMap, action_name: str, item_name: str) -> GenMap:
            """Return job parameters of provided @build_info as dict"""
            actions = cast(GenMapArray, build_info.get("actions") or [])
            for action in map(lambda a: cast(GenMap, a), actions):
                if cast(str, action.get("_class") or "").rsplit(".", 1)[-1] == action_name:
                    if action_name == "ParametersAction":
                        return {
                            str(p["name"]): p["value"]
                            for p in map(
                                lambda a: cast(GenMap, a), cast(GenMapArray, action[item_name])
                            )
                        }
                    if action_name == "CustomBuildPropertiesAction":
                        return cast(GenMap, action[item_name])
            return {}

        self.url = cast(str, raw_build_info["url"])
        self.number = cast(int, raw_build_info["number"])
        self.timestamp = datetime.fromtimestamp(cast(int, raw_build_info["timestamp"]) // 1000)
        self.result = cast(str, raw_build_info["result"])
        self.building = cast(str, raw_build_info["building"])
        self.in_progress = cast(bool, raw_build_info["inProgress"])
        self.parameters = params_from(raw_build_info, "ParametersAction", "parameters")
        self.path_hashes = cast(
            Mapping[str, str],
            params_from(raw_build_info, "CustomBuildPropertiesAction", "properties").get(
                "path_hashes", {}
            ),
        )
        self.artifacts = [
            cast(Mapping[str, str], a)["relativePath"]
            for a in cast(GenMapArray, raw_build_info["artifacts"])
        ]
        # SCM could be retrieved via 'hudson.plugins.git.util.BuildData'


@dataclass
class Job:
    """Models a Jenkins job"""

    name: str
    fullname: str
    builds: Mapping[int, Build]

    def __init__(self, raw_job_info: GenMap, raw_build_infos: GenMapArray):
        self.name = cast(str, raw_job_info["name"])
        self.fullname = cast(str, raw_job_info["fullName"])
        self.builds = {
            cast(int, bi["id"]): Build(bi) for bi in map(lambda a: cast(GenMap, a), raw_build_infos)
        }


@dataclass
class Folder:
    """Models a Jenkins folder"""

    name: str
    fullname: str
    jobs: Sequence[str]

    def __init__(self, raw_job_info: GenMap):
        self.name = cast(str, raw_job_info["name"])
        self.fullname = cast(str, raw_job_info["fullName"])
        self.jobs = [cast(str, j["name"]) for j in cast(Sequence[GenMap], raw_job_info["jobs"])]


def extract_credentials(credentials: None | Mapping[str, str]) -> Mapping[str, str]:
    """Turns the information provided via --credentials into actual values"""
    if credentials and (
        any(key in credentials for key in ("url", "url_env"))
        and any(key in credentials for key in ("username", "username_env"))
        and any(key in credentials for key in ("password", "password_env"))
    ):
        return {
            "url": credentials.get("url") or os.environ[credentials.get("url_env", "")],
            "username": credentials.get("username")
            or os.environ[credentials.get("username_env", "")],
            "password": credentials.get("password")
            or os.environ[credentials.get("password_env", "")],
        }
    logger().debug(
        "Credentials haven't been (fully) provided via --credentials, trying JJB config instead"
    )
    jjb_config = ConfigParser()
    jjb_config.read(Path("~/.config/jenkins_jobs/jenkins_jobs.ini").expanduser())
    return {
        "url": jjb_config["jenkins"]["url"],
        "username": jjb_config["jenkins"]["user"],
        "password": jjb_config["jenkins"]["password"],
    }


@contextmanager
def jenkins_client(
    url: str, username: str, password: str, timeout: None | int = None
) -> Iterator[Jenkins]:
    """Create a Jenkins client interface using the config file used for JJB"""
    client = Jenkins(
        url=url,
        username=username,
        password=password,
        timeout=timeout if timeout is not None else 20,
    )
    whoami = client.get_whoami()
    if not whoami["id"] == username:
        logger().warning("client.get_whoami() does not match jenkins_config['user']")

    yield client


def _fn_info(args: Args) -> None:
    """Entry point for information about job artifacts"""
    credentials = extract_credentials(args.credentials)
    with jenkins_client(
        credentials["url"], credentials["username"], credentials["password"]
    ) as client:
        class_name = (job_info := client.get_job_info(args.job))["_class"]
        if class_name == "com.cloudbees.hudson.plugins.folder.Folder":
            # print(yaml.dump(job_info))
            print(Folder(job_info))
        elif class_name == "org.jenkinsci.plugins.workflow.job.WorkflowJob":
            build_infos = [
                client.get_build_info(args.job, cast(int, cast(GenMap, b)["number"]))
                for b in cast(GenMapArray, job_info["builds"])
            ]
            print(Job(job_info, build_infos))
        else:
            raise Fatal(f"Don't know class type {class_name}")


def md5from(filepath: Path) -> str | None:
    """Returns an MD5 sum from contents of file provided"""
    with suppress(FileNotFoundError):
        with open(filepath, "rb") as input_file:
            file_hash = hashlib.md5()
            while chunk := input_file.read(1 << 16):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    return None


@contextmanager
def cwd(path: Path) -> Iterator[None]:
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def git_commit_id(git_dir: Path, path: None | Path | str = None) -> str:
    """Returns the git hash of combination of given paths. First one must be a directory, the
    second one is then considered relative"""
    assert git_dir.is_dir()
    assert not path or (git_dir / path).exists()
    with cwd(git_dir):
        return check_output(
            # use the full hash - short hashes cannot be checked out and they are not
            # unique among machines
            ["git", "log", "--pretty=tformat:%H", "-n1"] + ([str(path)] if path else []),
            text=True,
        ).strip("\n")


def download_artifacts(client: Jenkins, build_url: str, out_dir: Path) -> None:
    """Downloads all artifacts listed for given job/build to @out_dir"""
    # pylint: disable=protected-access
    out_dir.mkdir(parents=True, exist_ok=True)

    # https://bugs.launchpad.net/python-jenkins/+bug/1973243
    # https://bugs.launchpad.net/python-jenkins/+bug/2018576
    fingerprints = client._session.get(
        f"{build_url}api/json?tree=fingerprint[fileName,hash]"
    ).json()["fingerprint"]

    if not fingerprints:
        raise Fatal(f"No (fingerprinted) artifacts found at {build_url}")

    for fingerprint in fingerprints:
        fp_filename, fp_hash = fingerprint["fileName"], fingerprint["hash"]
        logger().debug("Handle artifact: %s (md5: %s)", fp_filename, fp_hash)
        artifact_filename = out_dir / fp_filename
        local_hash = md5from(artifact_filename)

        if local_hash == fp_hash:
            logger().debug("File is already available locally: %s (md5: %s)", fp_filename, fp_hash)
            continue

        if local_hash and local_hash != fp_hash:
            logger().warning(
                "File exists locally but hashes differ: %s %s != %s",
                fp_filename,
                local_hash,
                fp_hash,
            )

        with client._session.get(f"{build_url}artifact/{fp_filename}", stream=True) as reply:
            logger().debug("Download: %s", fp_filename)
            reply.raise_for_status()
            with open(artifact_filename, "wb") as out_file:
                for chunk in reply.iter_content(chunk_size=1 << 16):
                    out_file.write(chunk)


def path_hashes_match(first: PathHashes, second: PathHashes) -> bool:
    """Returns True if two given path hash mappings are semantically equal, i.e. at least one hash
    is prefix of the other (to handle short hashes, as returned with %h)
    >>> path_hashes_match({}, None)
    True
    >>> path_hashes_match({"a": "abc"}, None)
    False
    >>> path_hashes_match({"a": "abc"}, {"a": "abc"})
    True
    >>> path_hashes_match({"a": "abc"}, {"a": "abcde"})
    True
    """
    if not first and not second:
        return True
    if bool(first) != bool(second):
        return False
    if first.keys() != second.keys():
        return False
    return all(
        hash1.startswith(hash2) or hash2.startswith(hash1)
        for key, hash1 in first.items()
        for hash2 in (second[key],)
    )


def meets_constraints(
    build: Build,
    params: None | JobParams,
    time_constraints: None | str,
    path_hashes: PathHashes,
    now: datetime = datetime.now(),
) -> bool:
    """Checks if a set of requirements are met for a given build"""

    result = True
    used_params = params or {}
    # TODO: find solution for unprovided parameters and default/empty values
    mismatching_parameters = [
        (key, build.parameters.get(key, ""), used_params.get(key, ""))
        for key in set(build.parameters.keys() | used_params.keys()) - {"DISABLE_CACHE"}
        if build.parameters.get(key, "") != used_params.get(key, "")
    ]

    assert build.result in {"SUCCESS", "FAILURE"}

    if build.result != "SUCCESS":
        logger().debug("build #%d result was: %s", build.number, build.result)
        return False

    if mismatching_parameters:
        logger().debug(
            "build #%d has mismatching parameters: %s", build.number, mismatching_parameters
        )
        result = False

    if not path_hashes_match(build.path_hashes, path_hashes):
        logger().debug(
            "build #%d has mismatching path hashes: %s != %s",
            build.number,
            build.path_hashes,
            path_hashes,
        )
        result = False

    if time_constraints is None or time_constraints == "today":
        if build.timestamp.date() != datetime.now().date():
            logger().debug(
                "build #%d does not meet time constraints: %s != %s",
                build.number,
                build.timestamp.date(),
                now.date(),
            )
            if result:
                logger().warning(
                    "build #%d seems to have no relevant changes, but is invalidated by time"
                    " constraint only! You might want to check build conditions."
                )
            result = False
    else:
        raise Fatal(f"Don't understand time constraint specifier {time_constraints!r}")

    return result


def find_matching_build(
    job: Job, params: None | JobParams, time_constraints: None | str, path_hashes: Mapping[str, str]
) -> Build | None:
    """Goes through a job's build items and returns the first one to match certain criteria or None
    if none is found"""
    for build_id, build in job.builds.items():
        if meets_constraints(build, params, time_constraints, path_hashes):
            print(
                f"Found matching build: {build_id}"
                f" {build.timestamp} {build.result} {build.parameters}"
            )
            for key, value in build.__dict__.items():
                print(f"  {key}: {value}")
            return build
    return None


def create_new(client: Jenkins, job_full_path: str, params: None | JobParams) -> Build:
    """Starts a job specified by @job_full_path using @params and returns its build info object"""
    queue_id = client.build_job(job_full_path, params)
    while True:
        queue_item = client.get_queue_item(queue_id)
        print(yaml.dump(queue_item))
        if executable := queue_item.get("executable"):
            print(yaml.dump(executable))
            return Build(client.get_build_info(job_full_path, executable["number"]))
        time.sleep(1)


def _fn_fetch(args: Args) -> None:
    """Entry point for fetching artifacts"""
    # logger().debug("Parsed params: %s", params)
    fetch_job_artifacts(
        args.job,
        credentials=args.credentials,
        params={k: v for p in (args.params or []) for k, v in p.items()},
        dependency_paths=[path for paths in args.dependency_paths for path in paths.split(",")],
        base_dir=args.base_dir,
        time_constraints=args.time_constraints,
        out_dir=args.out_dir,
        omit_new_build=args.omit_new_builds,
    )


def fetch_job_artifacts(
    job_full_path: str,
    *,
    credentials: None | Mapping[str, str] = None,
    params: None | JobParams = None,
    dependency_paths: None | Sequence[str] = None,
    base_dir: Path = Path("."),
    time_constraints: None | str = None,
    out_dir: None | Path = None,
    omit_new_build: bool = False,
) -> None:
    """Returns artifacts of Jenkins job specified by @job_full_path matching @params and
    @time_constraints. If none of the existing builds match the conditions a new build will be
    issued. If the existing build has not finished yet it will be waited for."""
    creds = extract_credentials(credentials)
    with jenkins_client(creds["url"], creds["username"], creds["password"]) as client:
        if not str((job_info := client.get_job_info(job_full_path))["_class"]).endswith(
            "WorkflowJob"
        ):
            raise Fatal(f"{job_full_path} is not a WorkflowJob")
        job = Job(
            job_info,
            [
                client.get_build_info(job_full_path, cast(int, cast(GenMap, b)["number"]))
                for b in cast(GenMapArray, job_info["builds"])
            ],
        )
        path_hashes = {path: git_commit_id(base_dir, path) for path in (dependency_paths or [])}

        build_candidate = (
            find_matching_build(job, params, time_constraints, path_hashes) or None
            if omit_new_build
            else create_new(client, job_full_path, params)
        )

        if not build_candidate:
            assert omit_new_build
            raise Fatal(
                f"No matching build could be found for job '{job.name}' and new builds are omitted."
            )

        if build_candidate.in_progress or build_candidate.building:
            print(f"Waiting for job #{build_candidate.number} to finish..")
            while True:
                build_candidate = Build(
                    client.get_build_info(job_full_path, build_candidate.number)
                )
                if build_candidate.in_progress or build_candidate.building:
                    logger().debug(
                        "build.in_progress=%s build.building=%s",
                        build_candidate.in_progress,
                        build_candidate.building,
                    )
                    time.sleep(2)
                    continue
                break
            if not build_candidate.artifacts:
                raise Fatal("Job has no artifacts!")

        download_artifacts(client, build_candidate.url, base_dir / (out_dir or ""))


def main() -> None:
    """Entry point for everything else"""
    try:
        args = parse_args()
        logging.basicConfig(
            format="%(levelname)s %(asctime)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=getattr(logging, args.log_level),
        )
        logger().debug("Parsed args: %s", args)
        args.func(args)
    except Fatal as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(-1) from exc
    except JenkinsException as exc:
        logger().error("%r", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
