FROM python:3-onbuild
MAINTAINER Michael Zhang <failed.down@gmail.com>

RUN mkdir -p /openctf
COPY . /openctf/
WORKDIR /openctf

ENTRYPOINT ["python", "app.py"]
