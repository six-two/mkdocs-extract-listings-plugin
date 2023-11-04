#!/bin/bash
# This script is used to build the documentation (for the vercel hosted website)
# Thus I didn't bother setting up stuff like venv here ;)

# Switch to the directory of this file
cd "$( dirname "${BASH_SOURCE[0]}" )"

# install the dependencies
pip install -r requirements.txt
# also install the latest (dev) version of this package
pip install .

# Vercel prefers outputs to be in public/
mkdocs build -d public

if [[ -n "$1" ]]; then
    echo "[*] Starting web server on 127.0.0.1:$1"
    python3 -m http.server --bind 127.0.0.1 --directory public "$1"
fi