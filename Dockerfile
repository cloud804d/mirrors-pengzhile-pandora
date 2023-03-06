FROM python:3.7-slim

WORKDIR /opt/app
ADD . .
RUN pip install --upgrade pip && pip install .

ENTRYPOINT ["bin/startup.sh"]
