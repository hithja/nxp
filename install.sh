#!/bin/bash

VERSION="v1.0.1"
INSTALL_PATH="/usr/bin/nxp"
DOWNLOAD_URL="https://github.com/hithja/nxp/releases/download/$VERSION/nxp"

if command -v curl &> /dev/null; then
    curl -L $DOWNLOAD_URL -o $INSTALL_PATH
    chmod +x $INSTALL_PATH
else
    echo "To continue, please, install curl"
    exit 0
fi