FROM ubuntu
MAINTAINER Casey Hilland <chilland@caerusassociates.com>
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y git build-essential unzip python-setuptools python-dev wget default-jre
RUN easy_install pip
RUN pip install pexpect unidecode jsonrpclib simplejson
RUN cd /usr/share; git clone https://bitbucket.org/torotoki/corenlp-python.git
RUN cd /usr/share/corenlp-python; wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-08-27.zip; unzip stanford-corenlp-full-2014-08-27.zip
EXPOSE 5003
WORKDIR /usr/share/corenlp-python
CMD python corenlp/corenlp.py -H 0.0.0.0 -p 5003 -S stanford-corenlp-full-2014-08-27/
