FROM docker.io/library/python:slim AS builder

RUN apt-get update && apt-get install -y gcc libssl-dev

RUN pip install --no-cache-dir pycryptodome gensafeprime

FROM pwn.red/jail

COPY --from=builder / /srv

COPY samado.py /srv/app/run
COPY secret.py /srv/app/secret.py

RUN chmod 755 /srv/app/run

ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
ENV JAIL_TIME 60
