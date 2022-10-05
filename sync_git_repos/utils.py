import json
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Optional, Union


@dataclass
class SyncSetting:
    """ Settings """
    # from repo url
    from_repo_url: str
    # to repo url
    to_repo_url: str
    # Key and local repo  dir
    key: str
    # Delete local repo dir if True
    delete_after_sync: Optional[bool] = False
    # Force push if True. Execute push with '--force' flag
    force_push: Optional[bool] = False
    # List of branches for syncing(push with branch), if is not set execute push with '--mirror' flag
    branches: Optional[Tuple] = None


def prepare_repo_url(repo_url: str):
    envs = ['GITHUB_TOKEN']
    for env in envs:
        env_val = os.environ.get(env)
        if env_val:
            repo_url = repo_url.replace(f'${env}', env_val)

    return repo_url


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
    target_dest = Path(base_dir) / sync_setting.key
    try:
        create_folder_status, create_folder_message = create_folder_if_not_exist(target_dest)
        if create_folder_status > 0:
            logger.info(create_folder_message)
        else:
            logger.error(create_folder_message)

        # Folder created
        if create_folder_status == 1:
            output = clone_repo(sync_setting.from_repo_url, target_dest)
            if output:
                logger.info(output)
        else:
            output = fetch(str(target_dest))
            if output:
                logger.info(output)

            output = pull()
            if output:
                logger.info(output)
        if sync_setting.branches:
            for branch in sync_setting.branches:
                output = push(sync_setting.to_repo_url, str(target_dest), branch, force=sync_setting.force_push)
                if output:
                    logger.info(output)
        else:
            output = push(sync_setting.to_repo_url, str(target_dest), mirror=True)
            if output:
                logger.info(output)

        logger.info(f'Success syncing to {sync_setting.to_repo_url}!')
    except Exception as repo_ex:
        logger.error(repo_ex)
    finally:
        if sync_setting.delete_after_sync:
            shutil.rmtree(target_dest, ignore_errors=True)


def fetch(dest: str) -> str:
    return sh(['git', 'fetch', 'origin'], cwd=dest)


def pull() -> str:
    return sh(['git', 'pull', '--ff-only'])


def push(repo_url: str, dest: str, branch: Optional[str] = None, force: Optional[bool] = False,
         mirror: Optional[bool] = False) -> str:
    main_args = ['git', 'push', repo_url]
    if branch:
        main_args.append(branch)

    if force:
        main_args.append('--force')

    if mirror:
        main_args.append('--mirror')

    return sh(main_args, cwd=dest)


def clone_repo(repo_url: str, dest: Union[os.PathLike, str]) -> str:
    if not repo_exists(dest):
        return sh(['git', 'clone', '--no-checkout', '--bare', repo_url, str(dest)])

    return f'Repo "{repo_url}" already clone.'


def get_repo_info(dest: Union[os.PathLike, str]) -> dict:
    if not repo_exists(dest):
        raise ValueError(f'No repo found at {dest}')

    current_remote = sh(shlex.split('git config --get remote.origin.url'), cwd=dest)
    current_branch = sh(shlex.split('git rev-parse --abbrev-ref HEAD'), cwd=dest)

    return {'current_remote': current_remote, 'current_branch': current_branch}


def repo_exists(dest: Union[os.PathLike, str]):
    return os.path.exists(os.path.join(dest, 'HEAD'))
