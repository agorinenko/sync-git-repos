import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any, Dict, Tuple, Optional, Union


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


def sync_git_repo(logger, base_dir: str, from_path: str, to_path: str, branch_name: Optional[str] = 'main') -> Tuple[
    int, str]:
    """
    Sync one git repo
    :param branch_name: branch name
    :param logger: logger for printing
    :param base_dir: base dir
    :param from_path: from path
    :param to_path: to path
    :return: status and message
    """

    target_dest = get_repo_folder_name(from_path)
    target_dest = Path(base_dir) / target_dest
    status, message = create_folder_if_not_exist(target_dest)
    if status > 0:
        logger.info(message)
    else:
        logger.error(message)

    output = clone_repo('main', from_path, target_dest)
    if output:
        logger.info(output)

    info = get_repo_info(target_dest)
    remote_repo, branch = info['current_remote'], info['current_branch']
    assert remote_repo == from_path
    assert branch == branch_name

    output = push_to_mirror(to_path)
    if output:
        logger.info(output)

    # 'Success syncing!'
    return 1, f'Success syncing to {to_path}!'


def push_to_mirror(mirror_url: str) -> str:
    #     git push --mirror ssh://git@git.service.t1-cloud.ru:7999/clportal/python/tags_service.git
    return sh(['git', 'push', '--mirror', mirror_url])


def get_repo_folder_name(repo_url: str) -> str:
    repo_folder_name = os.path.basename(os.path.normpath(repo_url))
    replace_str = [('.git', ''), ('.', '_'), ('-', '_')]

    for items in replace_str:
        repo_folder_name = repo_folder_name.replace(*items)

    return repo_folder_name


def clone_repo(branch: str, repo_url: str, dest: Union[os.PathLike, str]) -> str:
    if not repo_is_cloned(dest):
        return sh(['git', 'clone', '--no-checkout', '--bare', '--branch', branch, repo_url, str(dest)])

    return f'Repo "{repo_url}" already clone.'


def get_repo_info(dest: Union[os.PathLike, str]) -> dict:
    if not repo_is_cloned(dest):
        raise ValueError(f'No repo found at {dest}')

    current_remote = sh(shlex.split('git config --get remote.origin.url'), cwd=dest)
    current_branch = sh(shlex.split('git rev-parse --abbrev-ref HEAD'), cwd=dest)

    return {'current_remote': current_remote, 'current_branch': current_branch}


def repo_is_cloned(dest: Union[os.PathLike, str]):
    return os.path.exists(os.path.join(dest, 'HEAD'))
