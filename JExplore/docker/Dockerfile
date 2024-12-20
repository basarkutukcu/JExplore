FROM ubuntu:22.04

RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip

RUN pip install pyzmq
RUN pip install notebook