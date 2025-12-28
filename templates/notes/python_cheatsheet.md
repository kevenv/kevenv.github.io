# Python cheatsheet

## PIP
- `pip list --user` : list installed python libs
- `pip install --user [lib]` : install python lib
- `pip install --user -r requirements.txt` : install all python libs in requirements file
- `pipreqs requirements.txt` : create requirements.txt for current project

### Virtual Environment (venv)
- `python -m venv [venv]` : create venv
- `source [venv]/bin/activate` : enable venv
- `pip freeze > requirements.txt` : create requirements.txt
- `deactivate` : disable venv
- `rm -rf [venv]` : remove venv

## HTTP
- `python -m http.server` : run HTTP server

### Debugger (pdb)
TODO:
