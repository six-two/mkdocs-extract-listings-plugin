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
# use AWK instead of sed '/plugins:/a- offline' to make it work on macOS
sed -e '/^use_directory_urls:/s|true|false|' -e '/offline:/s|false|true|' mkdocs.yml | awk '{print} /plugins:/ {print "- offline"}' > "mkdocs-offline.yml"

echo "[*] Building site"
python3 -m mkdocs build -f "mkdocs-offline.yml" || exit 1

echo "[*] Opening path in firefox"
if [[ $(uname) == Darwin ]]; then
    open -a Firefox.app site/plugin/index.html
else
    firefox site/plugin/index.html
fi
