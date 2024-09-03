ENV_FILE := $(or $(ENV_FILE), .env.development)

include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))

export REGISTRY_USERNAME=tjmaynes
export IMAGE_NAME=shopping-cart-service-py
export TAG=$(shell git rev-parse --short HEAD)

install:
	chmod +x ./scripts/install.sh
	./scripts/install.sh

migrate:
	DATABASE_URL=$(DATABASE_URL) bin/dbmate wait
	DATABASE_URL=$(DATABASE_URL) bin/dbmate up
	DATABASE_URL=$(DATABASE_URL) bin/dbmate migrate

test: migrate
	. .venv/bin/activate; python3 -m pytest

lint:
	. .venv/bin/activate; python3 -m ruff check --config ruff.toml shoppingcart/

format:
	. .venv/bin/activate; python3 -m ruff format --config ruff.toml shoppingcart/

start: migrate
	. .venv/bin/activate; uvicorn --host 0.0.0.0 --port $(PORT) shoppingcart.main:api

seed: migrate
	. .venv/bin/activate; python3 -m shoppingcart.seed

build_image:
	chmod +x ./scripts/build-image.sh
	./scripts/build-image.sh

debug_image:
	chmod +x ./scripts/debug-image.sh
	./scripts/debug-image.sh

push_image:
	chmod +x ./scripts/push-image.sh
	./scripts/push-image.sh

connect_localhost_to_remote_db:
	kubectl port-forward svc/shopping-cart-db 5432:5432

run_local_db:
	docker compose up

debug_local_db:
	docker run -it --rm \
		--network shopping-cart-service-py_shopping-cart-network \
		postgres:16.3-alpine \
		psql \
		-h shopping-cart-db \
		--username postgres

stop_local_db:
	docker compose down
	docker volume rm shopping-cart-service-py_shopping-cart-db

ship_it: lint test
	git push

deploy: install lint test build_image push_image

clean:
	rm -rf .venv build/ dist/ *.egg-info .pytest_cache/ bin/*

.PHONY: shoppingcart