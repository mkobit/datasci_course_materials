FROM ubuntu:12.04

MAINTAINER Mike Kobit

RUN set -x \
        && apt-get update \
        && apt-get install --only-upgrade -y python-setuptools \
        && apt-get install -y python-pip \
        && apt-get clean all

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt \
        && rm /tmp/requirements.txt
