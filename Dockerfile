FROM python:3.7

WORKDIR /opt/app
ADD . .
RUN python setup.py install

ENTRYPOINT ["pandora"]
