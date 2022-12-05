ARG UBUNTU=jammy

# Build the binary reproducably
FROM ubuntu:$UBUNTU as builder

# Enable APT package caching
RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# Install base packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libc-dev

WORKDIR /tmp

RUN --mount=type=bind,source=rev-baby.c,target=/tmp/rev-baby.c \
    gcc -O2 -o rev-baby rev-baby.c

# Build output exporter -- see Makefile
FROM scratch as exporter

COPY --from=builder /tmp/rev-baby .


# Base image for our jail
FROM ubuntu:$UBUNTU as rever

RUN useradd -u 1000 jail


# Actual jail image
FROM pwn.red/jail

COPY --from=rever / /srv
COPY --from=builder /tmp/rev-baby /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run
RUN chmod 644 /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_CONNS_PER_IP 5
