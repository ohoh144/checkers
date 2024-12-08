# !/bin/bash
# test
pipenv run pytest test/**.py

# lint
pipenv run pylint **/*.py
