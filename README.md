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
      "from_repo_url": "https://$GITHUB_TOKEN:x-oauth-basic@github.com/agorinenko/sync-git-repos.git",
      "to_repo_url": "https://$GITHUB_TOKEN:x-oauth-basic@github.com/agorinenko/sync-git-repos_mirror.git",
      "delete_after_sync": true
    }
  }
}
```

`sync_folder` - folder with repos tree

`repos` - list of repos

`sync_git_repos` - key and local repo dir

`from_repo_url` - from repo url

`to_repo_url` - to repo url

`delete_after_sync` - delete local repo dir if True

**Env variables**

SETTINGS=/opt/app/settings.json, path to settings file

SLEEP_TIMEOUT=60, if the parameter is set, the synchronization is performed with the specified frequency (in sec.)

EMAIL=user email for clone

USER_NAME=user for clone

GITHUB_TOKEN=github token, https://github.com/settings/tokens

main branch