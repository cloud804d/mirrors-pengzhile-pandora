FROM python:3.7

WORKDIR /opt/app
ADD . .
RUN pip install .

ENTRYPOINT ["pandora"]
