# Shopping Cart Service

> Sample shopping cart CRUD service using Python3/FastAPI and Kubernetes

## Getting Started

To get started make sure the following requirements (for development and deployment tooling) are installed on your development machine:

- [GNU Make](https://www.gnu.org/software/make) (Script Runner)
- [Python 3.10](https://www.python.org/downloads/) (Project Programming Language)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (Python Dependency Manager)
- [DBMate](https://github.com/amacneil/dbmate) (Platform-agnostic Database Migrations Tool)
- [Docker](https://hub.docker.com/) (Containerization)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (K8s deployment CLI)
- [cURL](https://curl.haxx.se/) (HTTP REST client)

## Background

The goal of this project is to demonstrate what managing, testing, building and deploying a CRUD Python service looks like. By building this service, I was able see how the following works:
    - building an API service using [fastapi](https://fastapi.tiangolo.com/)
    - setting up integration tests via `pytest`
    - applying type safety (`Protocol`, `Generic`, `TypeVar`) to Python via the [typing](https://docs.python.org/3/library/typing.html) library and [mypy](http://www.mypy-lang.org/)
    - using the [Result](https://github.com/rustedpy/result) library
    - setting up Postgres via [Kubernetes](https://docs.docker.com/compose/)
    - setting up Database migrations via [DBMate](https://github.com/amacneil/dbmate)

Also, this project uses the `make` command quite frequently. Similar to how `gradle` is used in Java, Spring, or many other JVM-based projects, `make` is used as a tool that acts as an "interface" to the project. A big reason as to why I've chosen `make` as my de-facto "project interface tool" is that it acts as a simple, well documented, script runner and it's generally available on most unix-based machines. For more info on the available `make` commands, check out the [usage](https://github.com/tjmaynes/shopping-cart-service#usage) section. 

## Playing with the Shopping Cart Service

To get the health endpoint, run the following command:
```bash
curl -X GET localhost:5001/health
```

To get all cart items, run the following command:
```bash
curl -X GET 'localhost:5001/cart/?page_number=0&page_size=20'
```

To get a cart item by id, run the following command:
```bash
curl -X GET localhost:5001/cart/1
```

To add a cart item, run the following command:
```bash
curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"name":"70-200mm Lens","price":240000,"manufacturer": "Canon"}' \
    localhost:5001/cart/
```

To update a cart item, run the following command:
```bash
curl \
    -X PUT \
    -H "Content-Type: application/json" \
    -d '{"name": "Lens Cap", "price": "888888888", "manufacturer": "Canon"}' \
    localhost:5001/cart/1
```

To remove a cart item, run the following command:
```bash
curl -X DELETE localhost:5001/cart/1
```

### Development
First, make sure that the project dependencies have been installed with the following command:
```bash
make install
```

Next, let's make sure the test suite for the application is running as expected.

1. Check to make sure `Docker` is running.

2. Since our test suite talks to a database, let's make sure that PostgreSQL is running locally via:
```bash
make run_local_db
```

3. Finally, let's run our tests via:
```bash
make test
```

*If the test suite is not passing, please provide an [issue](https://github.com/tjmaynes/shopping-cart-service/issues) for the project.*

## Usage
To install project dependencies, run the following command:
```bash
make install
```

To run all tests (**make sure database is running**), run the following command:
```bash
make test
```

To make sure the database is running, run the following command:
```bash
make run_local_db
```

To start the app and database locally, run the following command:
```bash
make start
```

To debug the local database, run the following command:
```bash
make debug_local_db
```

To build the docker image, run the following command:
```bash
make build_image
```

To debug the docker image, run the following command:
```bash
make debug_image
```

To push the docker image, run the following command:
```bash
make push_image
```

To deploy the `shopping-cart-service`, run the following command:
```bash
make deploy
```

To get the project in a clean state, run the following command:
```bash
make clean
```

## [License](./LICENSE)
