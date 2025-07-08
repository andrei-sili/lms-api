run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

test:
	pytest

freeze:
	pip freeze > requirements.txt

startapp: # ex: make startapp app=user
	python manage.py startapp $(app) apps/$(app)

