#!/usr/bin/env bash

# Change into the project root
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

# If you created a virtual python environment, source it
if [[ -f venv/bin/activate ]]; then
    echo "[*] Using virtual python environment"
    source venv/bin/activate
fi

echo "[*] Installing dependencies"
python3 -m pip install -r requirements.txt

# Install the pip package
python3 -m pip install .

# Do not use directory urls, since the browser does not map from /path/ to /path/index.html for file:// urls
sed -e '/^use_directory_urls:/s|true|false|' -e '/offline:/s|false|true|' -e '/plugins:/a- offline' mkdocs.yml > "mkdocs-offline.yml"

echo "[*] Building site"
python3 -m mkdocs build -f "mkdocs-offline.yml" || exit 1

echo "[*] Opening path in firefox"
firefox site/plugin/index.html
