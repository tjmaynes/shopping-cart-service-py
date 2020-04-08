#!/bin/sh

set -e

python setup.py bdist_wheel
pip install dist/*.whl

which shopping_cart_service