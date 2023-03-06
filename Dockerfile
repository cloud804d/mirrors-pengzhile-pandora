FROM python:3.7-slim

MAINTAINER "Neo Peng <pengzhile@gmail.com>"

ENV USER_CONFIG_DIR /data
VOLUME ${USER_CONFIG_DIR}

WORKDIR /opt/app
ADD . .
RUN pip install --upgrade pip && pip install .

ENTRYPOINT ["bin/startup.sh"]
