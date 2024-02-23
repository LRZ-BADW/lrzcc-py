# README

This is the command line tool for the budgeting system.

## Development Quickstart
The command line client needs a working REST API to work with.
Make sure that you have one available. :-)

### Virtual python environment

```python
python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
```

### First initialization
You need an OpenRC file that you need to source.
Usually you might use the `admin-openrc.sh` file we use to authenticate as
admin.

```bash
. admin-openrc.sh
source venv/venv/bin/activate
# Check if authentication works
python main.py user me
python main.py user import
python main.py flavor import
python main.py flavor-price initialize
# Show all project budgets that exist
python main.py project-budget list --all
# Show all user budgets that exist
python main.py user-budget list --all
# Get all projects that are over budget
python main.py project-budget over --all
# Get all users that are over budget
python main.py user-budget over --all
```
