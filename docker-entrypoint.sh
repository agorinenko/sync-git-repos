#!/bin/bash
set -e

case "$1" in
sync)
  hub config --global hub.protocol https
  hub config --global user.email "$EMAIL"
  hub config --global user.name "$USER_NAME"
  export GITHUB_TOKEN="$GITHUB_TOKEN"

  pip install sync-git-repos

  exec python -m sync_git_repos --sleep_timeout "$SLEEP_TIMEOUT"
  ;;
*)
  exec "$@"
  ;;
esac
