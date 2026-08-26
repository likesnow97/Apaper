#!/usr/bin/env bash
# git credential helper：从项目根目录的 .env 读取 GitHub 凭据。
# 供 setup-git-auth.sh 配置为 git 的 credential.helper 使用。
# 本脚本不包含任何密钥，凭据只存在于 .env 文件中。

set -euo pipefail

ENV_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.env"

username=""
token=""

if [[ -f "$ENV_FILE" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
        # 去掉行首空白
        line="${line#"${line%%[![:space:]]*}"}"
        # 跳过空行和注释
        [[ -z "$line" || "$line" == \#* ]] && continue

        key="${line%%=*}"
        value="${line#*=}"
        # 去掉首尾引号
        value="${value%\"}"; value="${value#\"}"
        value="${value%\'}"; value="${value#\'}"

        case "$key" in
            GITHUB_USERNAME) username="$value" ;;
            GITHUB_TOKEN) token="$value" ;;
        esac
    done < "$ENV_FILE"
fi

if [[ "${1:-}" == "get" && -n "$username" && -n "$token" ]]; then
    echo "username=$username"
    echo "password=$token"
fi
