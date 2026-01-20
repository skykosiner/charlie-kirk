#!/bin/sh

docker run --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows \
    "python -m PyInstaller --onefile --add-data 'assets;assets' --noconsole ./main.py"
