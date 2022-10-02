import json
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple, Optional, Union


@dataclass
class SyncSetting:
    """
    Settings
    """
    # from repo url
    from_repo_url: str
    # to repo url
    to_repo_url: str
    # Key and local repo  dir
    key: Optional[str]




# def get_repo_folder_name(repo_url: str) -> str:
#     repo_folder_name = os.path.basename(os.path.normpath(repo_url))
#     replace_str = [('.git', ''), ('.', '_'), ('-', '_')]
#
#     for items in replace_str:
#         repo_folder_name = repo_folder_name.replace(*items)
#
#     return repo_folder_name


def create_folder_if_not_exist(folder_path: Union[str, os.PathLike]) -> Tuple[int, str]:
    if os.path.exists(folder_path):
        return 2, f'Folder "{folder_path}" already exists.'

    os.makedirs(folder_path)

    return 1, 'Folder "{folder_path}" created successfully.'


def load_file_as_dict(file: str) -> Dict:
    """
    Load file content
    :param file: pile path
    :return: content as dict
    """
    with open(file, encoding="utf-8") as json_file:
        return json.load(json_file)


def sh(*args, **kwargs) -> str:
    """
    Get subprocess output
    :param args:
    :param kwargs:
    :return:
    """
    return subprocess.check_output(*args, **kwargs).decode().strip()


def sync_git_repo(logger, base_dir: str, sync_setting: SyncSetting) -> None:
    """
    Sync one git repo
    :param logger: logger for printing
    :param base_dir: base dir
    :param sync_setting: sync setting
    :return: status and message
    """
    logger.info(f'Syncing from "{sync_setting.from_repo_url}" to "{sync_setting.to_repo_url}"...')
    try:
        target_dest = Path(base_dir) / sync_setting.key

        status, message = create_folder_if_not_exist(target_dest)
        if status > 0:
            logger.info(message)
        else:
            logger.error(message)

        output = clone_repo(sync_setting.from_repo_url, target_dest)
        if output:
            logger.info(output)

        output = push_to_mirror(sync_setting.to_repo_url)
        if output:
            logger.info(output)

        logger.info(f'Success syncing to {sync_setting.to_repo_url}!')
    except Exception as repo_ex:
        logger.error(repo_ex)


def push_to_mirror(mirror_url: str) -> str:
    return sh(['git', 'push', '--mirror', mirror_url])


def clone_repo(repo_url: str, dest: Union[os.PathLike, str]) -> str:
    if not repo_is_cloned(dest):
        return sh(['git', 'clone', '--no-checkout', '--bare', repo_url, str(dest)])

    return f'Repo "{repo_url}" already clone.'


def get_repo_info(dest: Union[os.PathLike, str]) -> dict:
    if not repo_is_cloned(dest):
        raise ValueError(f'No repo found at {dest}')

    current_remote = sh(shlex.split('git config --get remote.origin.url'), cwd=dest)
    current_branch = sh(shlex.split('git rev-parse --abbrev-ref HEAD'), cwd=dest)

    return {'current_remote': current_remote, 'current_branch': current_branch}


def repo_is_cloned(dest: Union[os.PathLike, str]):
    return os.path.exists(os.path.join(dest, 'HEAD'))
