ARG UBUNTU=jammy
# Build the binary reproducably
FROM ubuntu:$UBUNTU as abnodal
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.10 

FROM pwn.red/jail
COPY --from=abnodal / /srv

COPY run.py /srv/app/run.py
COPY utils.py /srv/app/utils.py
COPY run.sh /run.sh
COPY flag_lv0.txt /srv/app/flag_lv0.txt
COPY flag_lv1.txt /srv/app/flag_lv1.txt

RUN chmod 755 /srv/app/run.py
RUN chmod 755 /srv/app/utils.py
RUN chmod 755 /run.sh
RUN chmod 744 /srv/app/flag_lv0.txt
RUN chmod 744 /srv/app/flag_lv1.txt
ENTRYPOINT /run.sh
