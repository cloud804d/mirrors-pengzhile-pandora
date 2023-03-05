FROM python:3.7-slim

WORKDIR /opt/app
ADD . .
RUN pip install --upgrade pip && pip install .

ENTRYPOINT ["/opt/appbin/startup.sh"]
