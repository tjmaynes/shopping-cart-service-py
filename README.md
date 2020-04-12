# Sample Python App

> The goal of this project is to demonstrate what managing, testing, building and deploying a CRUD Python service looks like. By building this service, I was able see how the following works:
> - building a CRUD service using [Flask](https://palletsprojects.com/p/flask/), the popular Python web framework
> - using the [Either monad](https://www.schoolofhaskell.com/school/starting-with-haskell/basics-of-haskell/10_Error_Handling) to build operation pipelines
> - integration tests via unittest
> - setting up Postgres via [docker-compose](https://docs.docker.com/compose/)
> - database migrations via [dbmate](https://github.com/amacneil/dbmate)
> - applying type safety (Protocol, Generic, TypeVar) to Python via the [typing](https://docs.python.org/3/library/typing.html) library
> - setting up python app distribution via [wheel](https://pythonwheels.com/)
> - useful build, debug and push scripts for docker

## Getting Started

To get started make sure the following requirements (for development and deployment tooling) are installed on your development machine:

- [GNU Make](https://www.gnu.org/software/make) (Script Runner)
- [Python 3.8](https://www.python.org/downloads/release/python-382/) (Project Programming Language)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (Python Dependency Manager)
- [DBMate](https://github.com/amacneil/dbmate) (Platform-agnostic Database Migrations Tool)
- [Docker](https://hub.docker.com/) (Containerization)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (K8s deployment CLI)
- [Curl](https://curl.haxx.se/) (HTTP REST client)

> This project uses the `make` command quite frequently. Similar to how `gradle` is used in Java, Spring, or many other JVM-based projects, `make` is used as a tool that acts as an "interface" to the project. A big reason as to why I've chosen `make` as my de-facto "project interface tool" is that it acts as a simple, well documented, script runner and it's generally available on most unix-based machines. For more info on the available `make` commands, check out the [usage](https://github.com/tjmaynes/sample-python-app#usage) section. 

Next, make sure that the project dependencies have been installed with the following command:
> If you don't have `virtualenv` currently installed, then run `pip install virtualenv`.
```bash
make install_dependencies
```

### Sanity Check

For a quick sanity check, let's make sure the test suite for the application is running as expected.
1. Check to make sure `Docker` is running.
2. Since our test suite talks to a database, let's make sure that PostgreSQL is running locally via:
```bash
make run_local_db
```
3. Finally, let's run our tests via:
```bash
make test
```

If the test suite is passing, then please move on to the next section else please provide an [issue](https://github.com/tjmaynes/sample-python-app/issues) for the project.

### Running the App

To run the app in a `kuberenetes` cluster, run the following command:
```bash
make deploy_app
```

*or* to run the app using `docker-compose`, run the following command:
```bash
make development
```

### Playing with the Shopping Cart Service

To get the health endpoint, run the following command:
```bash
curl -X GET localhost:5000/healthcheck
```

To get all cart items, run the following command:
```bash
curl -X GET 'localhost:5000/cart/?page_number=0&page_size=20'
```

To get a cart item by id, run the following command:
```bash
curl -X GET localhost:5000/cart/1
```

To add a cart item, run the following command:
```bash
curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"name":"70-200mm Lens","price":240000,"manufacturer": "Canon"}' \
    localhost:5000/cart/
```

To update a cart item, run the following command:
```bash
curl \
    -X PUT \
    -H "Content-Type: application/json" \
    -d '{"name": "Lens Cap", "price": "888888888", "manufacturer": "Canon"}' \
    localhost:5000/cart/1
```

To remove a cart item, run the following command:
```bash
curl -X DELETE localhost:5000/cart/1
```

## Usage
To install `virtualenv` (python dependency manager), run the following command:
```bash
pip install virtualenv
```

To install project dependencies, run the following command:
```bash
make install_dependencies
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
make development
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
make deploy_app
```

To destroy the `shopping-cart-service`, run the following command:
```bash
make destroy_app
```

To get the project in a clean state, run the following command:
```bash
make clean
```

## Todo

- Setup CI pipeline
- Add performance testing
- Setup gunicorn
- Add support for monitoring
- Add better support for logging

## License

```
The MIT License (MIT)

Copyright (c) 2020 TJ Maynes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
