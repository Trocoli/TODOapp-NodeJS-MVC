FROM python:3.7
ENV PYTHONUNBUFFERED 1

#CRIA A PASTA INGRESSO DENTRO DO CONTAINER DOCKER

RUN mkdir /FSproject
WORKDIR /FSproject

ADD requirements.txt /FSproject/

ENV http_proxy="http://10.10.32.1:3128"
ENV https_proxy="http://10.10.32.1:3128"
ENV https_proxy="http://:bkuounipe45@10.10.32.1:3128"
RUN apt-get -y update && apt-get install -y libzbar-dev
RUN pip install -r requirements.txt


ADD . /FSproject/
