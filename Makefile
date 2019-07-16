.PHONY: help install lint run-dev run-prod
PYTHON_PATH_FORM_SERVICE := form-service-repo
.DEFAULT: help
help:
	@echo "make install"
	@echo "       installs requirements"
	@echo "make run-dev"
	@echo "       run project in dev mode"
	@echo "make run-prod"
	@echo "       run project in production mode"
	@echo "make lint"
	@echo "       run pylint"

install:
	pip3 install -r requirements.txt;

run-dev:
	export LC_ALL=C.UTF-8;\
	export LANG=C.UTF-8;\
    export PYTHONPATH=$(PYTHON_PATH_FORM_SERVICE);\
	export FLASK_ENV="development"; \
	export FLASK_APP="setup.py"; \
	python3 -m flask run -p 5050;

run-prod:
	export LC_ALL=C.UTF-8;\
    export LANG=C.UTF-8;\
	export PYTHONPATH=$(PYTHON_PATH_FORM_SERVICE); \
	export FLASK_ENV="production"; \
	export FLASK_APP="setup.py"; \
	flask run --port=5050;

lint:
	pylint setup.py form_service/
