ENV_FILE := $(or $(ENV_FILE), .env.development)

include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))

export TAG=$(shell git rev-parse --short HEAD)

install:
	./scripts/install.sh

migrate:
	./scripts/migrate.sh

test: migrate
	. .venv/bin/activate; python3 -m pytest

lint:
	. .venv/bin/activate; mypy api/

start: migrate
	. .venv/bin/activate; uvicorn --host 0.0.0.0 --port $(PORT) api.main:app 

seed: migrate
	. .venv/bin/activate; python3 -m api.seed

run_local_db:
	kubectl apply -f ./k8s/shopping-cart-common/secret.yml
	kubectl apply -f ./k8s/shopping-cart-db/deployment.yml
	kubectl apply -f ./k8s/shopping-cart-db/persistence.local.yml

connect_localhost_to_remote_db:
	kubectl port-forward svc/shopping-cart-db 5432:5432

debug_local_db:
	kubectl run cart-db-debug --rm -i --tty --image=postgres:11.5-alpine -- \
		psql -h shopping-cart-db --username $(POSTGRES_USER) --password $(POSTGRES_PASS) $(POSTGRES_DB)

stop_local_db:
	kubectl delete -f ./k8s/shopping-cart-common/secret.yml
	kubectl delete -f ./k8s/shopping-cart-db/deployment.yml
	kubectl delete -f ./k8s/shopping-cart-db/persistence.local.yml

build_image:
	./scripts/build-image.sh

debug_image:
	./scripts/debug-image.sh

push_image:
	./scripts/push-image.sh

deploy: install lint test build_image push_image

clean:
	rm -rf .venv build/ dist/ *.egg-info .pytest_cache/ bin/*