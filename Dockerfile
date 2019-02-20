FROM python:3.7-alpine 
#as in docker you can use images on top of images so using this image here as alpine image is lightweight version of docker
MAINTAINER Sarthak Kumar ksarthak4ever.

ENV PYTHONUNBUFFERED 1 #telling python to run unbuffered

# Install dependencies
COPY ./requirements.txt /requirements.txt 
#i.e copying requirement file we create here and copying it to docker image

#installing dependencies for postgres
RUN apk add --update --no-cache postgresql-client
#what it does is it uses the package manager that comes with alpine i.e apk and we add a package,--update means update registry before we add it, --no-cache means dont store registry index on our dockerfile we do this to minimize the no of extra files and packages that are included in our docker container, so the docker container for our app/project has smallest footprint possible And it also means we don't include any extra dependencies or anything on your system which may cause unexpected side effects or it may even create security vulnerabilities in your system. 

RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
#virtual sets up an alias for our temp dependencies so its easier to delete in the future

RUN pip install -r /requirements.txt 
#installing req file we just copied into the docker image

RUN apk del .tmp-build-deps
#deletes temporary builds

# Setup directory structure
RUN mkdir /project
WORKDIR /project 
#so that any application we run using our docker container will run starting from this location
COPY ./project/ /project 
#copies code from our local machine to the docker image

RUN adduser -D user 
#for security purposes we try avoiding using root user and create a seperate user
USER user 