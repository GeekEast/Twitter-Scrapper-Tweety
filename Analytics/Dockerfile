FROM ubuntu:16.04

COPY /TweetNLPEngine.py /TweetNLPEngine.py
COPY /bitcoin.csv /bitcoin.csv

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip
RUN apt-get update
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install requests
RUN python3.6 -m pip install pymongo
RUN apt-get update
RUN apt-get install -y python
RUN apt-get update
RUN apt-get install -y unzip
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get update
RUN apt-get install -y nano
RUN apt-get update
RUN apt-get install -y iputils-ping







