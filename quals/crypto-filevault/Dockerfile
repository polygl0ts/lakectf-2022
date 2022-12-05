FROM python:3-slim AS builder

RUN useradd -u 1000 jail
RUN pip install rich

FROM pwn.red/jail

COPY --from=builder / /srv

COPY filevault.py /srv/app/run
COPY flag.png /srv/app/flag.png

RUN chmod 755 /srv/app/run
RUN chmod 744 /srv/app/flag.png

COPY hook.sh /jail/hook.sh

ENV JAIL_TIME 300
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
