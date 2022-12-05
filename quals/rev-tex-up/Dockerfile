ARG UBUNTU=jammy
# Build the binary reproducably
FROM ubuntu:$UBUNTU as latex
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.10 python3-pip 
RUN apt-get install -y --no-install-recommends socat
#COPY requirements.txt requirements.txt
#RUN pip install  --no-cache-dir -r requirements.txt

COPY server.py /srv/app/run
COPY run.sh /run.sh

RUN chmod 755 /srv/app/run
RUN chmod 755 /run.sh
ENTRYPOINT /run.sh
