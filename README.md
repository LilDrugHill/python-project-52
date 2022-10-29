### Hexlet tests and linter status:
[![Actions Status](https://github.com/LilDrugHill/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/LilDrugHill/python-project-52/actions) 
<a href="https://codeclimate.com/github/LilDrugHill/task-manager/maintainability"><img src="https://api.codeclimate.com/v1/badges/099cd5cc372b8fda668a/maintainability" /></a>
<a href="https://codeclimate.com/github/LilDrugHill/task-manager/test_coverage"><img src="https://api.codeclimate.com/v1/badges/099cd5cc372b8fda668a/test_coverage" /></a>
### Check task manager on:
[![HEROKU](https://img.shields.io/badge/HEROKU-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://afternoon-sands-50209.herokuapp.com)

### Training website for task management.

# Installing and running the app

You can run the application using Poetry.

**Poetry** is setup by the commands:

**Linux, macOS, Windows (WSL):**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Details on installing and using the **Poetry** package are available in [official documentation](https://python-poetry.org/docs/).

To install **Poetry** you need **Python 3.7+** use the information from the official website [python.org](https://www.python.org/downloads/)

---

## 1. Installation

### 1.1 Cloning the repository and installing dependencies

```bash
git clone https://github.com/LildrugHill/task_manager
cd task_manager
```

Installing dependencies if you use **Poetry**

```bash
make install
```

Activate virtual environment

```bash
source $HOME/.cache/pypoetry/virtualenvs/<name of the created environment>/bin/activate
```

---

### 1.2 To work with the project, you will need to set the values of the environment variables in the .env file

The value for `SECRET_KEY` can be generated with the terminal command `make secretkey` in the project directory or you can make one up.

`DEBUG_MODE` is `True` for dev and `False` for prod.

`access_token` - [Rollbar docs](https://docs.rollbar.com/docs)

---

### 1.3 Finishing the installation

```bash
make setup
```

---

## 2. Running a server for development

```bash
make django-dev
```

---