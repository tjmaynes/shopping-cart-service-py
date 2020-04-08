FROM python:3.8-slim as base
LABEL AUTHOR "TJ Maynes <tj@tjmaynes.com>"

RUN apt-get update \
&& apt-get install -y --no-install-recommends git curl \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/download/v1.7.0/dbmate-linux-amd64
RUN chmod +x /usr/local/bin/dbmate

WORKDIR /builder

COPY . .

RUN chmod +x ./scripts/create_and_install_distribution.sh
RUN ./scripts/create_and_install_distribution.sh

EXPOSE 5000

RUN chmod +x ./scripts/run_app.sh
ENTRYPOINT [ "./scripts/run_app.sh" ]
