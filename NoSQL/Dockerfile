FROM ubuntu:16.04

# create db file
RUN mkdir ./data

# install python3
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip

# install python2
RUN apt-get update
RUN apt-get install -y python

# install unzip and wget
RUN apt-get update
RUN apt-get install unzip
RUN apt-get update
RUN apt-get install wget
RUN apt-get update
RUN apt-get install nano

# install mongodb
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
RUN echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.4.list
RUN apt-get update
RUN apt-get install -y mongodb-org

# delare the port to open
EXPOSE 27017
CMD mongod --dbpath ./data











