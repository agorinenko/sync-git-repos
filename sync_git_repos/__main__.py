import argparse
import logging
import sys
from typing import Optional, Any, List, Dict

from sync_git_repos import utils

parser = argparse.ArgumentParser()

group = parser.add_argument_group('Main settings')
group.add_argument('--settings', required=False, type=str, default='settings.json', help='Path to settings file')
group.add_argument('--repo', required=False, type=str, default=None, help='Repo key for sync')


def _get_settings(settings: dict, name: str) -> Optional[Any]:
    value = settings.get(name)
    if not value:
        raise Exception(f'Setting "{name}" is none or empty. Check "settings.json".')

    return value


def _load_repos(settings: dict) -> Dict[str, utils.SyncSetting]:
    repos = _get_settings(settings, 'repos')
    result = {}
    for key, repo in repos.items():
        result[key] = utils.SyncSetting(key=key,
                                        from_repo_url=_get_settings(repo, 'from_repo_url'),
                                        to_repo_url=_get_settings(repo, 'to_repo_url'))

    return result


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
        utils.sync_git_repo(logger, sync_folder, repo)
    else:
        for repo in repos.values():
            utils.sync_git_repo(logger, sync_folder, repo)


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
