#!/usr/bin/env bash
# 配置本仓库的 git 使用 .env 中的 GitHub 凭据（credential.helper）。
# 运行：bash scripts/setup-git-auth.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git config credential.helper "!f() { bash '$ROOT/scripts/git-credential-env.sh' \"\$@\"; }; f"

echo "已配置 git credential helper：从 $ROOT/.env 读取 GitHub 凭据"
