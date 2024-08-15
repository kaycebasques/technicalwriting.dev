[[ -d _build ]] && rm -rf _build
source venv/bin/activate
python3 -m pip install -r requirements.txt
make html
deactivate
