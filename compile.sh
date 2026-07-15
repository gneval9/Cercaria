set -e

clear

source ~/venv/bin/activate

pyinstaller --onefile --name Cercaria\
    --add-data "mapas_cercaria:." \
    main.py

mv dist/* ./
rm -rf build dist Cercaria.spec

clear

echo "Results are in:"
pwd

echo
