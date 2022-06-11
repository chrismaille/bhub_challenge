## Development Guide

Use this guide on how to develop this project.

### Migrate

##### Migrating Database in VSCode:

* [https://code.visualstudio.com/docs/remote/containers#_opening-a-terminal](https://code.visualstudio.com/docs/remote/containers#_opening-a-terminal)

1. On menu Terminal, click "New Terminal"
2. Type command `make migrations` or `python manage.py makemigrations`
   (both are equal)
3. Type command `make migrate` or `python manage.py migrate` (both are
   equal)

##### Migrating Database in Pycharm:

1. On *Run Configuration*, click first on "**Run Deps**" to start the
   databases and then the "**Run Migration**" button to start migration.

### Test

##### Testing in VSCode:

* [https://code.visualstudio.com/docs/python/testing#_enable-a-test-framework](https://code.visualstudio.com/docs/python/testing#_enable-a-test-framework)

1. On command-palette select "**Python: Configure Tests**" .
2. Select framework **Pytest** and base folder "."
3. Click "**Run Tests**"

##### Testing in Pycharm:

1. On *Run Configuration*, click first on "**Run Deps**" to start the
   databases and then the "**Run Tests**" button to start testing.

### Run Application

##### Running in VSCode:

* [https://code.visualstudio.com/docs/editor/debugging#_launch-configurations](https://code.visualstudio.com/docs/editor/debugging#_launch-configurations)

1. On *Activity Bar*, click the "**Run**" button.
2. To run **Django**, please select "Python:Django" and click Play.
3. To run **Celery**, please select "Python:Celery" and click Play.

##### Running in PyCharm:

1. To start all dependencies, go to *Run Configuration*, select "Run
   Deps" and click Play.
2. To run **Api**, go to *Run Configuration*, select "Run Server" and
   click Play.
3. To run **Beat**, go to *Run Configuration*, select "Run Beat" and
   click Play.
4. To run **Worker**, go to *Run Configuration*, select "Run Celery" and
   click Play.

### Lint and Format Code

This Project is linted using [Pre-Commit](https://pre-commit.com/)
configured with the following packages:

* [Bandit](https://bandit.readthedocs.io/en/latest/)
* [Black](https://black.readthedocs.io/en/stable/?badge=stable)
* [iSort](https://github.com/PyCQA/isort)
* [Pylint](https://www.pylint.org/)

When possible we are using the default options for these tools. Per
based project exceptions are handled in `pyproject.toml` and `.pylintrc`
files.

Make sure you have resolved all *Bandit*, *Pylint*, *iSort* and *Black*
issues before upload code to Github. The CI/CD process will check all.
To run the tools:

1. Open *VSCode Terminal* and type `make pre-commit`

##### Linting and Format in VSCode:

* [https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00](https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00)
* [https://code.visualstudio.com/docs/python/linting](https://code.visualstudio.com/docs/python/linting)

1. Use the Console "Problems" tab to see Pylint issues
2. Run "Open Settings (UI)" and search for "Format on Save". Mark the
   "Editor: Format on Save" option.
3. Search for "Python Formatting Provider" and in "Python > Formatting:
   Provider" select "black".

##### Linting and Format in PyCharm:

1. On *Run Configuration*, click on "**Run Pre-Commit**" button to start
   lint/format.

### Open a Shell (Terminal)

##### Open VSCode Terminal:

* [https://code.visualstudio.com/docs/remote/containers#_opening-a-terminal](https://code.visualstudio.com/docs/remote/containers#_opening-a-terminal)

1. On menu Terminal, click "New Terminal"

##### Open Docker Terminal in PyCharm:

1. Open PyCharm Terminal and type `docker compose run --rm
   --entrypoint="" api bash`

or

2. Go to `Services` tab, on *Docker*, select the current running
   container and right-click `New Terminal`

##### Terminal Commands available inside Container:

```shell
$ make update       # update poetry.lock
$ make test         # run pytest
$ make lint         # run pre-commit, unit tests and coverage
$ make format       # run Black
$ make bandit       # run Bandit
$ make pylint       # run Pylint
$ make pre-commit   # run Pre-Commit
$ make migrate      # run python manage.py migrate
$ make migrations   # run python manage.py makemigrations
```

### Add/Removing Dependencies

To add or remove project dependencies:

1. Modify the `pyproject.toml` file with the dependency alterations
2. Open *VSCode terminal* and type `make update` (it's an alias for the
   `poetry update` command). This command will update the `poetry.lock`
   file.
3. On VSCode select the "**Rebuild Container**" command. On HOST
   terminal, type `docker-compose build`. Make sure the `poetry.lock` is
   updated before running this command.

#### Example

Open the `pyproject.toml` file to add *my_awesome_lib* dependency:

```toml
[tool.poetry.dependencies]
my_awesome_lib = "*"
```

Always select the latest version, using `"*"`. But if you need to pin a
version, please add a comment with the reason:

```toml
[tool.poetry.dependencies]
my_awesome_lib = "<1.2.3"  # reason: Because github issue #123
```

After edit `pyproject.toml` open your Terminal and type:

```shell
# Alias for "poetry update", this command will work too.
$ make update
```

This command will update the `poetry.lock`, pinning the latest
compatible version for this dependency.

After that, on **VSCode**, select the command "**Rebuild Container**" or
in *HOST Terminal*, type `docker-compose build`
