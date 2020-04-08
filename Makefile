ENVIRONMENT ?= debug
PYTHON_CART_DB_USERNAME ?= postgres
PYTHON_CART_DB_NAME = cart
REGISTRY_USERNAME ?= tjmaynes
IMAGE_NAME ?= python-shopping-cart-service
TAG = $(shell cat cart_api/VERSION)

define ensure_command_installed
	command -v $1
endef

ensure_virtualenv_installed:
	$(call ensure_command_installed,virtualenv)

ensure_docker_installed:
	$(call ensure_command_installed,docker)

ensure_dbmate_installed:
	$(call ensure_command_installed,dbmate)

install_dependencies: ensure_virtualenv_installed
	test -d .venv || virtualenv .venv
	. .venv/bin/activate; pip install -e ".[dev]"

test: ensure_virtualenv_installed install_dependencies
	chmod +x ./scripts/run_tests.sh
	. .venv/bin/activate; source .env.${ENVIRONMENT} && ./scripts/run_tests.sh

development: ensure_docker_installed ensure_dbmate_installed install_dependencies
	docker-compose build && docker-compose up

debug_local_db: ensure_docker_installed
	docker-compose run cart-db psql -h cart-db -U $(PYTHON_CART_DB_USERNAME) $(PYTHON_CART_DB_NAME)

build_image: ensure_docker_installed
	chmod +x ./scripts/$@.sh
	./scripts/$@.sh \
	$(REGISTRY_USERNAME) \
	$(IMAGE_NAME) \
	$(TAG)

debug_image: ensure_docker_installed
	chmod +x ./scripts/$@.sh
	source .env.debug && ./scripts/$@.sh \
	$(REGISTRY_USERNAME) \
	$(IMAGE_NAME) \
	$(TAG)

push_image: ensure_docker_installed
	chmod +x ./scripts/$@.sh
	./scripts/$@.sh \
	$(REGISTRY_USERNAME) \
	$(IMAGE_NAME) \
	$(TAG) \
	$(REGISTRY_PASSWORD)

clean:
	rm -rf .venv build/ dist/ *.egg-info .pytest_cache/
