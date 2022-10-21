django-dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations task_manager statuses labels tasks
	poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=task_manager . --cov-report xml

install:
	poetry install
