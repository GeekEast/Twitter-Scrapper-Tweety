<div align=center><img src="/img/Tweet.jpeg"/></div>
<div align=center>
<img height = 100 src='/img/docker.jpeg'>
&#160&#160&#160&#160
<img height = 100 src="/img/selenium.png"/>
<img height = 100 src='/img/gcp.png'>
</div>

-------------

# Main Features

- Scrap tweet on **Any** topic during **Any** period of time.
- **No** username, password, key or token required.
- Suppport **Local Test** for both scapper and sentimeal analyser.
- Deploy **MongoDB** in **Docker** to store the scrapped Data
- Deploy **Google Cloud NLP** to rate the sentiment of tweets
-----------
# Local Test
###### Python Environment: 
```python
Python 3.6.4 Anaconda; Python 2.7

Please CD to the Demo Directory at first.
```
-----------

###### 1. Configure and run the Scrapper (Instructor)

```shell
#######################
####    Scrapper    ###
#######################

#######################
## Environment Setup ##
#######################

# download chromedriver
wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_mac64.zip
# unzip the file
unzip chromedriver_mac64.zip
# modify the permission
sudo chmod +x chromedriver
# move the chromedriver to right directory
sudo mv chromedriver /usr/local/bin
# install selenium
pip install selenium
# install beautifulsoup
pip install beautifulsoup4
# install pandas
pip install pandas
# install numpy
pip install numpy

#######################
###   Run Scrapper  ###
#######################

# enter the local demo directory
cd Demo 
# run the scrapper
python Scrapper.py 

# Please check the current directory for the result
```
###### 2. Configure and run the sentiment analyser (Student)
1. You need one [google cloud platform account](https://accounts.google.com/signup/v2/webcreateaccount?service=ahsid&continue=https%3A%2F%2Fcloud.google.com%2Fnatural-language%2Fdocs%2Fquickstart&flowName=GlifWebSignIn&flowEntry=SignUp
) with the nlp api enabled.
2. download your google [ service account](
https://cloud.google.com/natural-language/docs/quickstart#quickstart-analyze-entities-gcloud) credential into the directory - demo.
```shell
#######################
# Sentiment Analyser  #
#######################

#######################
## Environment Setup ##
#######################

# download google cloud sdk
wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-203.0.0-darwin-x86_64.tar.gz
# unzip the gz file
tar google-cloud-sdk-203.0.0-darwin-x86_64.tar.gz
# install python2.7
You have to install python 2.7 for google nlp engine to run
# install google cloud sdk
./google-cloud-sdk/install.sh
# install google cloud nlp into python 3.6
pip install google-cloud-language --upgrade
# export your credential absolute path to environment
export GOOGLE_APPLICATION_CREDENTIALS=<CREDENTIAL_PATH> 

#######################
###   Run Analyser  ###
#######################

# run Sentiment py file
python Sentiment.py

# Please check the current directory for the result
```
###### 3. Run the Scrapper and Analyser as pipline (Student)
```shell
# export your credential absolute path to environment
export GOOGLE_APPLICATION_CREDENTIALS=<CREDENTIAL_PATH> 
# run the pipeline
python Tweety.py
```

###### 4. Data analysis (Instructor)

```shell
# Please CD to the "Result" Directory at first

# RawData: Store the Scrapped Data.
# CleanData: Store the cleaned Data.
# Dataclean.py: python file to preprocess data
# DataAnalysis.py.py: python file to do regression forecast

# install dependencies
pip install seaborn
pip install sklearn
# run the analysis
python DataAnalysis.py
```
-----------

# Server Deployment (Student)
### Environment:
```python
Ubuntu 16.04 LTS VM
```

### Install Docker
```shell
# update and install necessary security packs
sudo apt update
sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv \
           --keyserver hkp://ha.pool.sks-keyservers.net:80 \
           --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
# add the docker repository
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
# update the package and verify 
sudo apt-get update
apt-cache policy docker-engine
# Install the docker and start the service
sudo apt-get install docker-engine
sudo service docker start
# Add the ubuntu user to the docker group. You must log out and log back in for this to take effect:
sudo usermod -aG docker <your_username>
exit
# After logging back in, verify that Docker is installed correctly:
docker run hello-world
# If you see a list of text output with one line indicating :
This message shows that your installation appears to be working correctly.

```


### Deploy MongoDB
```shell
# cd to the mongodb directory
cd NoSQL
# build the image using docker
docker build --rm --tag nosql/mongod:1.0 .
# run the images as a container
docker run -dit -p <port>:27017 nosql/mongod:1.0 
# inspect the nosql container's ip address
docker inspect <container_id>
```
##### Please take note of the nosql container's ip address.


### Deploy Tweety
```shell
# cd to the scrapper directory
cd Scrapper
# modify the py file to enter the nosql container ip
nano Tweet.py
# build the image using docker
docker build --rm --tag scrapper/tweet:1.0 .
# run the images as a container
docker run -dit scrapper/tweet:1.0
```
#####  Please pre-process the csv file and move it into the Analytics directory

### Deploy Sentimenal API

```shell
###########################
###  Build Base Docker  ###
###########################
# build the docker as sentiment/analytics:latest
docker build --rm --tag sentiment/analytics:1.0 .
# run the version 1.0
docker run -dit sentiment/analytics:1.0 tail -f /bin/bash
# enter the docker 1.0
docker exec -it <containerID> /bin/bash
# download google cloud sdk
wget google-cloud-sdk-203.0.0-darwin-x86_64.tar.gz
# unzip the gz file
tar google-cloud-sdk-203.0.0-darwin-x86_64.tar.gz
# install google cloud sdk
./google-cloud-sdk/install.sh
# install google cloud nlp into python 3.6
python3.6 -m pip install google-cloud-language --upgrade
# enter another shell and commit the change of version 1.0
docker commit <container_id> sentimen/analytics:latest

###########################
###  Customized Docker  ###
###########################

# run the base docker
docker run -dit sentiment/analytics:latest tail -f /bin/bash
# enter the docker
docker exec -it <containerID> /bin/bash
# initialize google cloud with google account (create new gcp if necessary)
./google-cloud-sdk/bin/gcloud init
# create the credential file and then export the credential file to environment
export GOOGLE_APPLICATION_CREDENTIALS=<CREDENTIAL_PATH>
# chunk the csv file into bulks to multiprocess the data
sed -n '<start_line>,<end_line>p' bitcoin.csv > bitcoin<Num>.csv
# run the py file to analyse the sentiment of tweet
python3.6 TweetNLPEngine.py <mongodb_ip> <mongodb_port> <db_name> <collection_name> <data_source>
# exmaple 172.17.0.2 27017 scrapper sentiment bitcoin.csv
```
#####  For this part, you may sign up for multiple google accounts.
[Sign up for Google](
    https://accounts.google.com/signup/v2/webcreateaccount?service=ahsid&continue=https%3A%2F%2Fcloud.google.com%2Fnatural-language%2Fdocs%2Fquickstart&flowName=GlifWebSignIn&flowEntry=SignUp
)

[Register the NLP Serveice](https://cloud.google.com/natural-language/docs/quickstart#quickstart-analyze-entities-gcloud)

-------------

# Sample Output

Scrapper
<div align=center><img src="/img/result.png"/></div>

Sentimental Analyser 
<div align=center><img src="/img/output.png"/></div>

Plot and Regression
<div align=center><img src="/img/1.png"/></div>
<div align=center><img src="/img/2.png"/></div>
<div align=center><img src="/img/3.png"/></div>
<div align=center><img src="/img/4.png"/></div>
<div align=center><img src="/img/5.png"/></div>
<div align=center><img src="/img/6.png"/></div>
<div align=center><img src="/img/7.png"/></div>
<div align=center><img src="/img/8.png"/></div>
<div align=center><img src="/img/8.png"/></div>
<div align=center><img src="/img/analysis.png"/></div>

----------
# Reference
[[1] Upzip File in linux](https://blog.csdn.net/tjcyjd/article/details/78267219)

[[2] Save changes of Docker](https://www.jianshu.com/p/95bafb2c14bc)

[[3] Install GCP SDK](https://cloud.google.com/sdk/docs/)

[[4] Get credentials of GCP NLP](
    https://cloud.google.com/natural-language/docs/quickstart#quickstart-analyze-entities-gcloud
)

[[5] Select lines of raw file in Linux](
https://blog.csdn.net/kangaroo_07/article/details/43733891
)

[[6] Combiner Multiple CSV files](
    https://blog.csdn.net/taolusi/article/details/81074105 
)

[[7] Import your py file as  package](
    https://blog.csdn.net/wcx1293296315/article/details/81156036
)

[[8] Configure Jupyter Notebook on AWS](
https://blog.csdn.net/tuzixini/article/details/79105482)


