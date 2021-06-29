.PHONY: all clean lint test tox type

CMD := poetry run
PYMODULE := iplib3
TESTS := tests

# Remember to activate Poetry's virtual environment in the project root folder
# 
# Only once (ideally):
# > pip install poetry
# > poetry install
# 
# Every time:
# > poetry shell

all: type lint test

lint:
    # Configured in pyproject.toml
    $(CMD) pflake8
    $(CMD) pylint $(PYMODULE)

type:
    $(CMD) mypy $(PYMODULE) $(TESTS)

test:
    # Configured in pyproject.toml
    $(CMD) pytest

tox:
    # Configured in pyproject.toml
    $(CMD) tox

clean:
    git clean -Xdf # Delete all files in .gitignore
