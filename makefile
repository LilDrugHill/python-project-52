django-dev:
	poetry run python manage.py runserver

make migrate:
	poetry run python manage.py makemigrations statuses labels tasks
	poetry run python manage.py migrate

make new-tables:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate --run-syncdb