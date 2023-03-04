FROM python:3.7

WORKDIR /opt/app
ADD . .
RUN pip install .

ENTRYPOINT ["/opt/app/bin/startup.sh"]
