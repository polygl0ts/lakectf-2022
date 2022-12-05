FROM docker.io/library/python:slim AS builder

RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail

COPY --from=builder / /srv

COPY chaindle.py /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run
RUN chmod 744 /srv/app/flag.txt

ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
ENV JAIL_TIME 60
