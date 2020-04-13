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

ensure_kubectl_installed:
	$(call ensure_command_installed,kubectl)

switch_context: ensure_kubectl_installed
	kubectl config use-context docker-for-desktop

add_secrets:
	kubectl apply -f cart_infrastructure/shopping-cart-common/secrets.yml

destroy_secrets:
	kubectl delete -f cart_infrastructure/shopping-cart-common/secrets.yml || true

deploy_db: add_secrets 
	kubectl apply -f cart_infrastructure/shopping-cart-db/persistence.yml
	kubectl apply -f cart_infrastructure/shopping-cart-db/deployment.yml
	kubectl apply -f cart_infrastructure/shopping-cart-db/service.yml

destroy_db: destroy_secrets 
	kubectl delete -f cart_infrastructure/shopping-cart-db/deployment.yml || true
	kubectl delete -f cart_infrastructure/shopping-cart-db/service.yml || true
	kubectl delete -f cart_infrastructure/shopping-cart-db/persistence.yml || true

deploy_app: deploy_db
	kubectl apply -f cart_infrastructure/shopping-cart-service/deployment.yml
	kubectl apply -f cart_infrastructure/shopping-cart-service/service.yml

destroy_app: destroy_db
	kubectl delete -f cart_infrastructure/shopping-cart-service/deployment.yml || true
	kubectl delete -f cart_infrastructure/shopping-cart-service/service.yml || true

clean:
	rm -rf .venv build/ dist/ *.egg-info .pytest_cache/
