django-dev:
	poetry run python manage.py runserver

full-migrate:
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
	django-admin compilemessages

secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'


migrate:
	poetry run python manage.py migrate

setup: migrate
	echo Create a super user
	poetry run python manage.py createsuperuser