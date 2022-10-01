import argparse
import logging
import sys
from typing import Optional, Any

from sync_git_repos import utils

parser = argparse.ArgumentParser()

group = parser.add_argument_group('Main settings')
group.add_argument('--settings', type=str, default='settings.json', help='Path to settings file')


def _get_settings(settings: dict, name: str) -> Optional[Any]:
    value = settings.get(name)
    if not value:
        raise Exception(f'Setting "{name}" is none or empty. Check "settings.json".')

    return value


def main(logger, args):
    settings = utils.load_file_as_dict(args.settings)

    sync_folder = _get_settings(settings, 'sync_folder')
    status, message = utils.create_folder_if_not_exist(sync_folder)
    if status > 0:
        logger.info(message)
    else:
        logger.error(message)

    repos = _get_settings(settings, 'repos')

    for repo in repos:
        try:
            from_path = _get_settings(repo, 'from')
            to_path = _get_settings(repo, 'to')

            logger.info(f'Syncing from "{from_path}" to "{to_path}"...')
            status, message = utils.sync_git_repo(logger, sync_folder, from_path, to_path)
            if status > 0:
                logger.info(message)
            else:
                logger.error(message)
        except Exception as repo_ex:
            logging.error(repo_ex)


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
