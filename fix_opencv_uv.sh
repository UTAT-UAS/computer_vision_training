#!/usr/bin/env bash

# To ensure opencv GUI works correctly, we need to enforce the non-headless package.
# Some dependencies (like label-studio-sdk) pull in opencv-python-headless.
# If uv has been run and created the venv, force remove headless and ensure opencv-python is installed.
export VIRTUAL_ENV="$PWD/.venv"
if [ -d "$VIRTUAL_ENV" ] && command -v uv &> /dev/null; then
    uv pip uninstall opencv-python-headless
    uv pip install opencv-python --force-reinstall
fi