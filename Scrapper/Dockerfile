FROM ubuntu:16.04

COPY /chromedriver /chromedriver
COPY /Tweet.py /Tweet.py

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip
RUN apt-get update
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install flask
RUN python3.6 -m pip install requests
RUN python3.6 -m pip install selenium
RUN python3.6 -m pip install numpy
RUN python3.6 -m pip install pandas
RUN python3.6 -m pip install beautifulsoup4
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
RUN apt-get install -y chromium-browser
RUN apt-get update
RUN apt-get install -y iputils-ping

RUN chmod +x /chromedriver
RUN mv -f /chromedriver /usr/local/share/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/bin/chromedriverr

CMD python3.6 Tweet.py blockchain





