FROM docker.io/python:3.8

WORKDIR /opt/app
COPY . .

RUN apt-get update
RUN apt-get install git hub

RUN chgrp -R 0 /opt/app/ && chmod -R g=u /opt/app/
RUN ["chmod", "+x", "/opt/app/docker-entrypoint.sh"]

ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]
