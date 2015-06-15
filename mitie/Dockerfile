FROM ubuntu:14.04
MAINTAINER Casey Hilland <chilland@caerusassociates.com>
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y git build-essential wget tar python-setuptools
RUN easy_install pip
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt
RUN git clone https://github.com/mit-nlp/MITIE.git
RUN cd MITIE; make MITIE-models
RUN cd MITIE/mitielib; make
ADD . /src
EXPOSE 5001
CMD ["python", "/src/mitie_api.py"]
