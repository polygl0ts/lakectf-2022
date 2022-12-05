FROM docker.io/library/ubuntu:22.04 as builder

RUN apt update && apt install -y --no-install-recommends \
        gcc \
        libc6-dev \
        python3-minimal

RUN useradd -u 1000 jail
FROM pwn.red/jail
COPY --from=builder / /srv

COPY challenge.py /srv/app/run
COPY main.c /srv/app/
COPY jail-hook.sh /jail/hook.sh

RUN chmod 755 /srv/app/run

# TODO
ENV JAIL_TIME 60
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
ENV JAIL_TMP_SIZE 5M
ENV JAIL_ENV_PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

