#!/bin/sh

docker run --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows \
    "python -m PyInstaller --onefile --add-data 'assets;assets' --noconsole ./main.py"

number=$(git log --oneline | head -n1 | grep -o "[0-9]\.[0-9]" | sed -E 's/^([0-9]+)\./echo $((\1+1))./e')
git add .
git commit -m "charlie $number"
git push
