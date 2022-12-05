FROM ubuntu AS builder

RUN apt update && apt install -y gcc python3 python3-pip
RUN useradd -u 1000 jail
RUN pip3 install web3

FROM pwn.red/jail

COPY --from=builder / /srv

COPY quinevm.py /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run
RUN chmod 744 /srv/app/flag.txt

COPY hook.sh /jail/hook.sh

ENV JAIL_TIME 60
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 100M

