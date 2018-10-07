###########################
###   Sentimenal API    ###
###########################

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


# linux 解压缩文件
https://blog.csdn.net/tjcyjd/article/details/78267219

# 保存对容器的修改
https://www.jianshu.com/p/95bafb2c14bc

# 获取credentials
https://cloud.google.com/sdk/docs/
https://cloud.google.com/natural-language/docs/quickstart#quickstart-analyze-entities-gcloud

# linux文本筛选中间行
https://blog.csdn.net/kangaroo_07/article/details/43733891

# 合并多个csv表
https://blog.csdn.net/taolusi/article/details/81074105


# 部署完毕
docker exec -it 908e1456ff5c /bin/bash 
sed -n '1,57950p' bitcoin.csv > bitcoin1.csv
sed -n '57951,115899p' bitcoin.csv > bitcoin2.csv
export GOOGLE_APPLICATION_CREDENTIALS="/pythongrouptweet-3d3cedd5450f.json"

# 部署完毕
docker exec -it 0dfa4a225043 /bin/bash
sed -n '115900,173848p' bitcoin.csv > bitcoin3.csv
sed -n '173849,231797p' bitcoin.csv > bitcoin4.csv
export GOOGLE_APPLICATION_CREDENTIALS="/tweety-218516-7d146ecb64f7.json"

# 部署完毕
docker exec -it b80bf44443ff /bin/bash
sed -n '231798,289746p' bitcoin.csv > bitcoin5.csv
sed -n '289746,347695p' bitcoin.csv > bitcoin6.csv
export GOOGLE_APPLICATION_CREDENTIALS="/tweet-218516-32234af08b42.json"

# 部署完毕
docker exec -it 986d3c473581 /bin/bash
sed -n '347696,405644p' bitcoin.csv > bitcoin7.csv
sed -n '405645,463601p' bitcoin.csv > bitcoin8.csv
export GOOGLE_APPLICATION_CREDENTIALS="/tweet-218517-e2b58104269d.json"

# md tutorial
https://pandao.github.io/editor.md/
# convert csv to md table
https://www.tablesgenerator.com/markdown_tables
