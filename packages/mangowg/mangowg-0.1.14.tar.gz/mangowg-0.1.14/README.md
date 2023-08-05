# MangoWG
Mango Website Generator PyPi Package 

## Python Venv

* `python -m venv venv`
* `venv\Scripts\activate.bat`
* `pip install -r requirements.txt`
* `pip freeze > requirements.txt`

## Usage
Get started `python mangowg.py --help`

To use command selection rather than typing the command name, use `python mangowg.py cut` then select the command to be executed.

Run the commands in order
```
start >  new > updateWholeProfile > getGithubInfo > getRepos > selectRepos > updateTemplate > push 
```

## PyPi publish 
Publish new package

* install poetry
* `poetry init`
* `poetry build`
* `poetry publish -u USERNAME -p PASSWORD`
    * use pypi password for this step

To update version number:

* `poetry version 0.1.2`
* `poetry build`
* `poetry publish -u USERNAME -p PASSWORD`
    * use github password for this step