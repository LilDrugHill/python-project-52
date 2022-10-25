django-dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations task_manager statuses labels tasks
	poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager

test:
	poetry run python manage.py test task_manager

test-cov:
	poetry run coverage run manage.py test task_manager
	poetry run coverage xml

install:
	poetry install

translate:
	django-admin makemessages -l ru

translate-comp:
	django-admin compilemessage
