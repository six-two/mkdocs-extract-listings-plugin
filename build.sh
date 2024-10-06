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

# delete the output dir
[[ -d public ]] && rm -rf public

# Create a fresh output dir
mkdir public

# Create a redirect to the default theme (material)
cp redirect.html public/index.html

build_with_theme() {
    echo "[*] Building with theme $1"
    sed "/^site_url:/s|\$|/$1/|" mkdocs.yml > "mkdocs-$1.yml"
    python3 -m mkdocs build -f "mkdocs-$1.yml" -t "$1" -d public/"$1"
}

build_with_theme_no_directory_urls() {
    echo "[*] Building with theme $1"
    sed -e "/^site_url:/s|\$|/$1/|" -e 's/use_directory_urls: true/use_directory_urls: false/' mkdocs.yml > "mkdocs-$1-no-dir.yml"
    python3 -m mkdocs build -f "mkdocs-$1-no-dir.yml" -t "$1" -d public/"$1"-no-dir
}


build_with_theme mkdocs
build_with_theme readthedocs
build_with_theme material

build_with_theme_no_directory_urls mkdocs
build_with_theme_no_directory_urls readthedocs
build_with_theme_no_directory_urls material

if [[ -z "$1" ]]; then
    echo "[*] To view the site run:"
    echo python3 -m http.server --directory "'$(pwd)/public/'"
else
    python3 -m http.server --directory public/ "$1"
fi
