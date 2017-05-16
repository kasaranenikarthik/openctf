FROM python:3-onbuild
MAINTAINER EasyCTF <team@easyctf.com>

# install dependencies
RUN apt-get update && \
    apt-get install -y python-nose libjpeg-dev libffi-dev libssl-dev mysql-client libmysqlclient-dev git

# copy required files
RUN mkdir /openctf
COPY . /openctf
WORKDIR /openctf

# run application
ENTRYPOINT ["/openctf/start.sh", "runserver"]
