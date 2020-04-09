# Shopping Cart

> The goal of this project is to demonstrate what managing, testing, building and deploying a CRUD Python service looks like. By building this service, I was able see how the following works:
> - building a CRUD service using [Flask](https://palletsprojects.com/p/flask/), the popular Python web framework
> - using the [Either monad](https://www.schoolofhaskell.com/school/starting-with-haskell/basics-of-haskell/10_Error_Handling) to build operation pipelines
> - integration tests via unittest
> - setting up Postgres via [docker-compose](https://docs.docker.com/compose/)
> - database migrations via [dbmate](https://github.com/amacneil/dbmate)
> - applying type safety (Protocol, Generic, TypeVar) to Python via the [typing](https://docs.python.org/3/library/typing.html) library
> - setting up python app distribution via [wheel](https://pythonwheels.com/)
> - useful build, debug and push scripts for docker

## Requirements

- [GNU Make](https://www.gnu.org/software/make)
- [Python 3.8](https://www.python.org/downloads/release/python-382/)
- [Docker](https://hub.docker.com/)
- [DBMate](https://github.com/amacneil/dbmate)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Git-Secret](https://git-secret.io/)

## Running the App
To run the app in a `kuberenetes` environment, run the following command:
```bash
make deploy_app
```

or to run the app in a `docker-compose` environment, run the following command:
```bash
make development
```

### The Service

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
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Lens&price=120000&manufacturer=Canon" \
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
