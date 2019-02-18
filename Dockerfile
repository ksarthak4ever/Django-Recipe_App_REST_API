FROM python:3.7-alpine 
#as in docker you can use images on top of images so using this image here as alpine image is lightweight version of docker
MAINTAINER Sarthak Kumar ksarthak4ever.

ENV PYTHONUNBUFFERED 1 #telling python to run unbuffered

# Install dependencies
COPY ./requirements.txt /requirements.txt 
#i.e copying requirement file we create here and copying it to docker image
RUN pip install -r /requirements.txt 
#installing req file we just copied into the docker image

# Setup directory structure
RUN mkdir /project
WORKDIR /project 
#so that any application we run using our docker container will run starting from this location
COPY ./project/ /project 
#copies code from our local machine to the docker image

RUN adduser -D user 
#for security purposes we try avoiding using root user and create a seperate user
USER user 