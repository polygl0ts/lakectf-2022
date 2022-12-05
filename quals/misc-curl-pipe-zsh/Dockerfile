FROM ubuntu AS builder
RUN apt update && apt install -y zsh curl git python3 && rm -rf /var/lib/apt/lists/*
RUN useradd -u 1000 jail

#FROM redpwn/jail
FROM pwn.red/jail

COPY --from=builder / /srv

COPY curl-pipe-zsh.py /srv/app/run
RUN chmod 755 /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 744 /srv/app/flag.txt

COPY hook.sh /jail/hook.sh

ENV JAIL_TIME 60
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
