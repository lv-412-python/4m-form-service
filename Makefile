.PHONY: help install clear lint run-dev run-prod
#SHELL := /bin/bash
PYTHON_PATH_FORM_SERVICE := ./form_service
.DEFAULT: help
help:
	@echo "make install"
	@echo "       creates venv and installs requirements"
	@echo "make run-dev"
	@echo "       run project in dev mode"
	@echo "make run-prod"
	@echo "       run project in production mode"
	@echo "make lint"
	@echo "       run pylint"
	@echo "make clear"
	@echo "       deletes venv and .pyc files"

install:
	python3 -m venv venv
	. ./venv/bin/activate; \
	pip install setuptools --upgrade --ignore-installed --user
	pip install pip --upgrade --ignore-installed --user
	pip install -r requirements.txt --user;

clear:
	rm -rf venv
	find -iname "*.pyc" -delete

set-path:
	export PYTHONPATH=$(PYTHON_PATH_FORM_SERVICE);\
	export FLASK_APP="setup.py"; \

dev-env:
	make install; \
	make set-path; \
	export FLASK_ENV="development"; \
	flask run --port=5050;

prod-env:
	make install; \
	make set-path; \
	flask run --port=5050;

lint:
	pylint setup.py form_service/
