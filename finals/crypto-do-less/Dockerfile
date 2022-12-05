FROM ubuntu:20.04 AS builder

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install pycryptodome

# Actual jail image
FROM pwn.red/jail
COPY --from=builder / /srv

COPY 0/* /srv/app/0/
COPY 1/* /srv/app/1/
COPY 2/* /srv/app/2/
COPY 3/* /srv/app/3/
COPY 4/* /srv/app/4/
COPY pub0.pem /srv/app/pub0.pem
COPY pub1.pem /srv/app/pub1.pem
COPY pub2.pem /srv/app/pub2.pem
COPY pub3.pem /srv/app/pub3.pem
COPY pub4.pem /srv/app/pub4.pem
COPY server.py /srv/app/server.py
COPY dealer.py /srv/app/dealer.py
COPY player.py /srv/app/player.py
COPY run /srv/app/run

RUN chmod 755 /srv/app/run
RUN chmod 644 /srv/app/server.py
RUN chmod 644 /srv/app/player.py
RUN chmod 644 /srv/app/dealer.py
RUN chmod 644 /srv/app/0/privkey.pem
RUN chmod 644 /srv/app/1/privkey.pem
RUN chmod 644 /srv/app/2/privkey.pem
RUN chmod 644 /srv/app/3/privkey.pem
RUN chmod 644 /srv/app/4/privkey.pem
RUN chmod 644 /srv/app/1/flag
RUN chmod 644 /srv/app/2/flag
RUN chmod 644 /srv/app/3/flag
RUN chmod 644 /srv/app/4/flag

ENV JAIL_TIME 120
ENV JAIL_CONNS_PER_IP 20
ENV JAIL_MEM 10M