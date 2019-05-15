PYTHON_MANAGE := python3 manage.py 

migrations:
	$(PYTHON_MANAGE) makemigrations

migrate:
	$(PYTHON_MANAGE) migrate

pip-install:
	pip install -r requirements.txt

pre-commit:
	pre-commit install

runserver:
	$(PYTHON_MANAGE) runserver

test:
	$(PYTHON_MANAGE) test