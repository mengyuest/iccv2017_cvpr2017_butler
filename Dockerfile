FROM ubuntu:16.04 
MAINTAINER Yue Meng

ARG DEBIAN_FRONTEND=noninteractive

# Install Python and Scrapy
RUN apt-get update
RUN apt-get install -y python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev

RUN pip install Scrapy
RUN pip install beautifulsoup4

ENV BASEDIR=/docker_cvpr
WORKDIR ${BASEDIR}
ADD butler ${BASEDIR}/butler
ADD *.sh *.py ${BASEDIR}/
RUN mkdir cvpr_lib@local

CMD . ./execute_in_local.sh
