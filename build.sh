[[ -d _build ]] && rm -rf _build
. venv/bin/activate.fish
python3 -m pip install -r requirements.txt
make html
deactivate
