TEST_ENVIRONMENT ?= local 
PYTHON_CART_DB_USERNAME ?= postgres
PYTHON_CART_DB_NAME = cart
REGISTRY_USERNAME ?= tjmaynes
IMAGE_NAME ?= python-shopping-cart-service
TAG = $(shell cat cart_api/VERSION)

define ensure_command_installed
	command -v $1 || (echo "Command '$1' not found..." && false)
endef

ensure_virtualenv_installed:
	$(call ensure_command_installed,virtualenv)

ensure_docker_installed:
	$(call ensure_command_installed,docker)

ensure_dbmate_installed:
	$(call ensure_command_installed,dbmate)

ensure_git_secret_installed:
	$(call ensure_command_installed,git-secret)

ensure_kubectl_installed:
	$(call ensure_command_installed,kubectl)

install_dependencies: ensure_virtualenv_installed
	test -d .venv || virtualenv .venv
	. .venv/bin/activate; pip install -e ".[dev]"

test: ensure_virtualenv_installed 
	chmod +x ./scripts/run_tests.sh
	. .venv/bin/activate; source .env.$(TEST_ENVIRONMENT) && ./scripts/run_tests.sh

development: ensure_docker_installed ensure_dbmate_installed 
	docker-compose build && docker-compose up

run_local_db: ensure_docker_installed
	docker-compose run --service-ports cart-db 

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
	./scripts/$@.sh \
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

reveal_secrets: ensure_git_secret_installed
	git secret reveal -f

create_secrets_config:
	cp -rf cart_infrastructure/secrets.example.yml cart_infrastructure/secrets.yml

add_secrets: ensure_kubectl_installed
	kubectl apply -f cart_infrastructure/secrets.yml

remove_secrets: reveal_secrets ensure_kubectl_installed
	kubectl delete -f cart_infrastructure/secrets.yml

add_deployment: ensure_kubectl_installed
	kubectl apply -f cart_infrastructure/deployment.yml

remove_deployment: ensure_kubectl_installed
	kubectl delete -f cart_infrastructure/deployment.yml

add_service: ensure_kubectl_installed
	kubectl apply -f cart_infrastructure/service.yml

remove_service: ensure_kubectl_installed
	kubectl delete -f cart_infrastructure/service.yml

switch_context: ensure_kubectl_installed
	kubectl config use-context docker-for-desktop

deploy_app: switch_context add_deployment add_secrets add_service 

destroy_app: switch_context remove_deployment remove_secrets remove_service

clean:
	rm -rf .venv build/ dist/ *.egg-info .pytest_cache/
