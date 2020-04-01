PYTHON_CART_DB_HOST ?= localhost
PYTHON_CART_DB_USERNAME ?= root
PYTHON_CART_DB_PASSWORD ?= password
PYTHON_CART_DB_PORT ?= 3308
PYTHON_CART_DB_NAME = cart

DATABASE_NAME = $(PYTHON_CART_DB_NAME)-db
DATABASE_VERSION = 8.0.17
DATABASE_URL = mysql://$(PYTHON_CART_DB_USERNAME):$(PYTHON_CART_DB_PASSWORD)@$(PYTHON_CART_DB_HOST):$(PYTHON_CART_DB_PORT)/$(PYTHON_CART_DB_NAME)
DATABASE_DIR = $(PWD)/$(PYTHON_CART_DB_NAME)_database
DATABASE_MIGRATIONS_DIR = $(DATABASE_DIR)/migrations
DATABASE_SCHEMA_FILE = $(DATABASE_DIR)/schema.sql

SERVER_PORT = 3000

REGISTRY_USERNAME ?= tjmaynes
REGISTRY_PASSWORD ?= some-password
IMAGE_NAME ?= python-shopping-cart-service
TAG = $(shell cat cart_api/VERSION)

FLASK_ENV ?= development
FLASK_APP ?= "cart_api:create_app()"
FLASK_RUN_PORT = $(SERVER_PORT)

define ensure_command_installed
	command -v $1
endef

define run_python_code
	PYTHON_CART_DB_HOST=$(PYTHON_CART_DB_HOST) \
	PYTHON_CART_DB_USERNAME=$(PYTHON_CART_DB_USERNAME) \
	PYTHON_CART_DB_PASSWORD=$(PYTHON_CART_DB_PASSWORD) \
	PYTHON_CART_DB_NAME=$(PYTHON_CART_DB_NAME) \
	PYTHON_CART_DB_PORT=$(PYTHON_CART_DB_PORT) \
	FLASK_APP=$(FLASK_APP) \
	FLASK_ENV=$(FLASK_ENV) \
	FLASK_RUN_PORT=$(FLASK_RUN_PORT) \
	. .venv/bin/activate; $1
endef

ensure_virtualenv_installed:
	$(call ensure_command_installed,virtualenv)

ensure_docker_installed:
	$(call ensure_command_installed,docker)

ensure_dbmate_installed:
	$(call ensure_command_installed,dbmate)

install_dependencies: ensure_virtualenv_installed
	virtualenv .venv; . .venv/bin/activate; pip install -e ".[dev]"

test: ensure_virtualenv_installed
	$(call run_python_code,python cart_api/api_test.py)

start_local_app: ensure_virtualenv_installed
	$(call run_python_code,flask run)

create_docker_network: ensure_docker_installed
	docker network create $(IMAGE_NAME)-network || true

start_local_db: ensure_docker_installed create_docker_network
	docker run \
	--name=$(DATABASE_NAME) \
	--env MYSQL_ROOT_PASSWORD=$(PYTHON_CART_DB_PASSWORD) \
	--env MYSQL_DATABASE=$(PYTHON_CART_DB_NAME) \
	--network $(IMAGE_NAME)-network \
	--publish $(PYTHON_CART_DB_PORT):3306 \
	--detach mysql:$(DATABASE_VERSION)

stop_local_db: ensure_docker_installed
	docker stop $(DATABASE_NAME) || true && docker rm $(DATABASE_NAME) || true

wait_for_database: ensure_dbmate_installed
	DATABASE_URL=$(DATABASE_URL) dbmate wait

run_migrations: ensure_dbmate_installed wait_for_database
	DATABASE_URL=$(DATABASE_URL) dbmate \
		--migrations-dir $(DATABASE_MIGRATIONS_DIR) \
		--schema-file $(DATABASE_SCHEMA_FILE) \
		up

seed_database: ensure_virtualenv_installed
	$(call run_python_code,python cart_api/seed_database.py)

delete_database: ensure_virtualenv_installed
	$(call run_python_code,python cart_api/delete_database.py)

create_and_install_distribution:
	$(call run_python_code,python setup.py bdist_wheel)
	$(call run_python_code,pip install dist/*.whl)

run_distribution:
	$(call run_python_code,shopping-cart-service)

uninstall_distribution:
	$(call run_python_code,pip uninstall shopping-cart-service)

debug_local_db: ensure_docker_installed create_docker_network
	docker run -it \
	--network $(IMAGE_NAME)-network \
	--rm mysql:$(DATABASE_VERSION) \
	mysql \
	--host=$(DATABASE_NAME) \
	--user=$(PYTHON_CART_DB_USERNAME) \
	--password=$(PYTHON_CART_DB_PASSWORD) \
	$(PYTHON_CART_DB_NAME)

build_image: ensure_docker_installed
	chmod +x ./scripts/build_image.sh
	./scripts/build_image.sh \
	$(REGISTRY_USERNAME) \
	$(REGISTRY_PASSWORD) \
	$(IMAGE_NAME) \
	$(TAG)

debug_image: ensure_docker_installed
	chmod +x ./scripts/debug_image.sh
	./scripts/debug_image.sh \
	$(DATABASE_NAME) \
	$(PYTHON_CART_DB_USERNAME) \
	$(PYTHON_CART_DB_PASSWORD) \
	$(PYTHON_CART_DB_NAME) \
	$(PYTHON_CART_DB_PORT) \
	$(SERVER_PORT) \
	$(REGISTRY_USERNAME) \
	$(IMAGE_NAME) \
	$(TAG)

push_image: ensure_docker_installed
	chmod +x ./scripts/push_image.sh
	./scripts/push_image.sh \
	$(REGISTRY_USERNAME) \
	$(REGISTRY_PASSWORD) \
	$(IMAGE_NAME) \
	$(TAG)

clean:
	rm -rf .venv build/ dist/ *.egg-info .pytest_cache/
