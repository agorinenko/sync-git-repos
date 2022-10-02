# Command for syncing git repos

Usage: 
```shell
python -m sync_git_repos [-h] [--settings SETTINGS] [--repo REPO]
```

optional arguments:

  `-h`, `--help` show this help message and exit

General settings:

  `--settings "settings.json"` Path to settings file

  `--repo "sync_git_repos"` Repo key for sync

  `--sleep_timeout 60` If the parameter is set, the synchronization is performed with the specified frequency (in sec.) indefinitely

