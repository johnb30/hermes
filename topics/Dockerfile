FROM ubuntu:14.04
MAINTAINER Casey Hilland <chilland@caerusassociates.com>
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y build-essential python-setuptools \
python-dev python-numpy python-scipy libatlas-dev libatlas3gf-base wget unzip
RUN easy_install pip
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt
ADD . /src
RUN unzip /src/stopwords.zip
RUN rm /src/stopwords.zip
RUN mkdir /usr/share/nltk_data
RUN mkdir /usr/share/nltk_data/corpora
RUN mv /stopwords /usr/share/nltk_data/corpora
EXPOSE 5002
CMD ["python", "/src/topic_model_api.py"]
