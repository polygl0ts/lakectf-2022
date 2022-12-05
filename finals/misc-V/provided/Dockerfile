FROM docker.io/library/ubuntu:22.04

RUN useradd -u 1000 ctf

WORKDIR /home/ctf
COPY bin/server.64 bin/server.pck ./

RUN chmod 755 server.64

USER ctf
ENTRYPOINT /home/ctf/server.64
