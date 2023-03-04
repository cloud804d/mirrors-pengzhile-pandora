FROM python:3.9

WORKDIR /opt/app
ADD . .
RUN pip install --upgrade pip && pip install .

ENTRYPOINT ["/opt/app/bin/startup.sh"]
