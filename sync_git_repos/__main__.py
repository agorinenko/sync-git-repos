import argparse
import logging
import sys
import time
from typing import Optional, Any, Dict, Callable

from sync_git_repos import utils

parser = argparse.ArgumentParser()

group = parser.add_argument_group('General settings')
group.add_argument('--settings', required=False, type=str, default='settings.json', help='Path to settings file')
group.add_argument('--repo', required=False, type=str, default=None, help='Repo key for sync')
group.add_argument('--sleep_timeout', required=False, type=int, default=-1,
                   help='If the parameter is set, the synchronization is '
                        'performed with the specified frequency (in sec.) indefinitely')


def _get_settings(settings: dict, name: str) -> Optional[Any]:
    value = settings.get(name)
    if not value:
        raise Exception(f'Setting "{name}" is none or empty. Check "settings.json".')

    return value


def _load_repos(settings: dict) -> Dict[str, utils.SyncSetting]:
    repos = _get_settings(settings, 'repos')
    result = {}
    for key, repo in repos.items():
        branches = repo.get('branches')
        if branches is not None:
            branches = tuple(branches)
        result[key] = utils.SyncSetting(key=key,
                                        branches=branches,
                                        force_push=repo.get('force_push', False),
                                        delete_after_sync=repo.get('delete_after_sync', False),
                                        from_repo_url=utils.prepare_repo_url(_get_settings(repo, 'from_repo_url')),
                                        to_repo_url=utils.prepare_repo_url(_get_settings(repo, 'to_repo_url')))

    return result


def _run_forever(sleep_timeout: int, func: Callable, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        time.sleep(sleep_timeout)


def _sync_all_repos(logger, sync_folder, repos):
    for repo in repos.values():
        utils.sync_git_repo(logger, sync_folder, repo)


def main(logger, args):
    settings = utils.load_file_as_dict(args.settings)

    sync_folder = _get_settings(settings, 'sync_folder')
    status, message = utils.create_folder_if_not_exist(sync_folder)
    if status > 0:
        logger.info(message)
    else:
        logger.error(message)

    repos = _load_repos(settings)

    if args.repo:
        repo = repos.get(args.repo)
        if not repo:
            raise Exception(f'Repo "{args.repo}" not found. Check "settings.json".')
        if args.sleep_timeout > 0:
            _run_forever(args.sleep_timeout, utils.sync_git_repo, logger, sync_folder, repo)
        else:
            utils.sync_git_repo(logger, sync_folder, repo)
    else:
        if args.sleep_timeout > 0:
            _run_forever(args.sleep_timeout, _sync_all_repos, logger, sync_folder, repos)
        else:
            _sync_all_repos(logger, sync_folder, repos)


if __name__ == '__main__':
    logging.basicConfig(
        format="[%(asctime)s - %(levelname)s - %(name)s] %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    main_logger = logging.getLogger('SYNC PROCESS')
    main_logger.setLevel(logging.INFO)

    try:
        main(main_logger, parser.parse_args())
    except Exception as ex:
        logging.error(ex)
