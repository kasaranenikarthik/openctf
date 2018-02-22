#!/bin/bash

# This script installs OpenCTF to /openctf on a clean server. If you're
# installing OpenCTF on an existing server, I'd recommend just running this
# step-by-step and modifying this to fit your server config.

set -e

REPOSITORY="https://github.com/easyctf/openctf.git"
THIS=$(realpath $0)
PROJECT=$(dirname `dirname $THIS`)

echo "Installing dependencies..."
apt-get update && apt-get install -y\
    git \
    libmysqlclient-dev \
    mysql-client \
    python3 \
    python3-dev \
    python3-pip \
    systemd

echo "Installing pip dependencies..."
PYTHON=$(which python3)
$PYTHON -m pip install -U pip # upgrade pip real quick
$PYTHON -m pip install gunicorn
$PYTHON -m pip install -r $PROJECT/requirements.txt
