if test -e _build
    rm -rf _build
end
. venv/bin/activate.fish
python3 -m pip install -r requirements.txt
make html
deactivate
