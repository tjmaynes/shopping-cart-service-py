# Shopping Cart

> Learning Python by building a shopping cart CRUD service with concepts introduced/learned:
> - building a Flask app
> - building pipelines with the Either monad
> - integration tests via unittest
> - setting up Postgres via Docker
> - database migrations via dbmate
> - typing library (Protocol, Generic, TypeVar)
> - setting up python app distribution
> - useful build, debug and push scripts for docker

## Requirements

- [Python 3.8](https://www.python.org/downloads/release/python-382/)
- [Docker](https://hub.docker.com/)
- [DBMate](https://github.com/amacneil/dbmate)

## Usage
To install `virtualenv`, run the following command:
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

To remove dependencies the project, run the following command:
```bash
make clean
```

## Running App

In order to run the app, run the following commands:
```bash
make development
```

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
