# Command for syncing git repos

**Install**

```shell
pip install sync-git-repos
```

If you see

```shell
client_loop: send disconnect: Broken pipe
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly
```

```shell
git config --global http.postBuffer 524288000
git config --global ssh.postBuffer 524288000
```

**Usage:**

```shell
python -m sync_git_repos [-h] [--settings SETTINGS] [--repo REPO]
```

optional arguments:

`-h`, `--help` show this help message and exit

General settings:

`--settings "settings.json"` Path to settings file

`--repo "sync_git_repos"` Repo key for sync

`--sleep_timeout 60` If the parameter is set, the synchronization is performed with the specified frequency (in sec.)
indefinitely

**Start docker**

```shell
docker-compose up -d --build
```

**Config example:**

```json
{
  "sync_folder": "sync_repos",
  "repos": {
    "sync_git_repos": {
      "branches": [
        "test1"
      ],
      "force_push": true,
      "from_repo_url": "https://$GITHUB_TOKEN:x-oauth-basic@github.com/agorinenko/sync-git-repos.git",
      "to_repo_url": "https://$GITHUB_TOKEN:x-oauth-basic@github.com/agorinenko/sync-git-repos_mirror.git",
      "delete_after_sync": true,
      "hooks": {
        "before": [
          {
            "name": "print",
            "args": [
              "Starting the process of synchronizing repositories"
            ]
          }
        ],
        "before_push": [
          {
            "name": "print",
            "args": [
              "Press any key to continue:"
            ]
          },
          "input"
        ],
        "after": [
          {
            "name": "print",
            "args": [
              "Wait 5 seconds"
            ]
          },
          {
            "name": "sleep",
            "kwargs": {
              "seconds": 5
            }
          },
          {
            "name": "print",
            "args": [
              "Thanks"
            ]
          }
        ]
      }
    }
  }
}
```

`sync_folder` - folder with repos tree

`repos` - list of repos

`sync_git_repos` - key and local repo dir

`branches` - list of branches for syncing(push with a branch), if is not set execute push with '--mirror' flag

`force_push` - force push if true. Execute push with '--force' flag

`from_repo_url` - from repo url

`to_repo_url` - to repo url

`delete_after_sync` - delete local repo dir if true

`hook` - hooks are objects for printing message(print), waiting user input(input) or sleeping before, before_push or
after sync repo.

**Hooks livecycle:**

```
before

IF folder created
  after_clone
ELSE
  after_pull

before_push

IF error
  on_sync_error

after
```

**Available hooks:**

``input`` - wait user input

``sleep`` - sleep on 2 second

``print`` - print message

**Env variables**

```
SETTINGS=/opt/app/settings.json, path to settings file

SLEEP_TIMEOUT=60, if the parameter is set, the synchronization is performed with the specified frequency (in sec.)

EMAIL=user email for clone

USER_NAME=user for clone

GITHUB_TOKEN=github token, https://github.com/settings/tokens
```
