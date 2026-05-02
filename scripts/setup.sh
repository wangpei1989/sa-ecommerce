#!/bin/bash
set -eo pipefail

# 设置 UV 超时环境变量
export UV_HTTP_TIMEOUT=300
export UV_CONNECT_TIMEOUT=60

# 初始化目录
if [ "$COZE_PROJECT_ENV" = "DEV" ]; then
  if [ ! -d "${COZE_WORKSPACE_PATH}/assets" ]; then
    mkdir -p "${COZE_WORKSPACE_PATH}/assets"
  fi
fi

# uv 安装依赖
if [ -n "$PIP_TARGET" ]; then
  echo "[setup] Deploy mode (uv): installing to PIP_TARGET=$PIP_TARGET"
  echo "[setup] UV timeout: UV_HTTP_TIMEOUT=$UV_HTTP_TIMEOUT"
  uv export --frozen --no-hashes --no-dev | uv pip install --no-cache --target "$PIP_TARGET" --no-build-isolation -r - || {
    echo "[setup] First attempt failed, retrying..."
    sleep 5
    uv export --frozen --no-hashes --no-dev | uv pip install --no-cache --target "$PIP_TARGET" --no-build-isolation -r -
  }
else
  echo "[setup] Devbox mode (uv): installing to .venv"
  if [ -f "uv.lock" ]; then
    uv sync --frozen || uv sync
  else
    uv sync
  fi
  touch .venv/.uv_ready
fi
