FROM python:3-onbuild
MAINTAINER Michael Zhang <failed.down@gmail.com>

RUN mkdir -p /openctf
COPY . /openctf/
WORKDIR /openctf

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:4242", "-w", "1", "app:app"]

