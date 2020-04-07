FROM python:3.8-slim as base
LABEL AUTHOR "TJ Maynes <tj@tjmaynes.com>"

RUN apt-get update \
&& apt-get install -y --no-install-recommends git \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /builder

COPY . .

RUN python setup.py bdist_wheel
RUN pip install dist/*.whl

# Safety check
RUN which shopping_cart_service

CMD ["shopping_cart_service"]