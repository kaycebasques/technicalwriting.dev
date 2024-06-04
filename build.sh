[[ -d _build ]] && rm -rf _build
source venv/bin/activate
make html
deactivate
