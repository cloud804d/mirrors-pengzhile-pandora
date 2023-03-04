FROM python:3.9 as build

RUN apt-get update && apt-get install -y gcc curl
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && apt-get install --reinstall libc6-dev -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --upgrade pip && pip install tiktoken==0.3.0

FROM python:3.9

COPY --from=build /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

WORKDIR /opt/app
ADD . .
RUN pip install --upgrade pip && pip install .

ENTRYPOINT ["/opt/app/bin/startup.sh"]
