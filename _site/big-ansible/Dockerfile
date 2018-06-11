FROM ubuntu:14.04.4
MAINTAINER Vui Le "vui.le@bigswitch.com"

ENV TERM   vt100

RUN apt-get update \
    && apt-get install -y \
              vim \
              libffi-dev \
              openssl \
              libssl-dev \
              libyaml-dev \
              sshpass \
              language-pack-en-base \
              software-properties-common \
              python-software-properties \
              python \
              python-dev \
              python-setuptools \
              python-pip \
              python-yaml \
              curl \
              sudo \
              jq \
              python-lxml

RUN mv /etc/localtime /etc/localtime.old \
    && ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

RUN mkdir -p /code /etc/ansible
RUN pip install \
              ansible \
              httplib2

RUN pip install --upgrade ansible

RUN \
    useradd -m admin \
    && echo "admin:adminadmin" | chpasswd \
    && adduser admin sudo

COPY code/entrypoint_loop.sh /code/

RUN \
    mkdir /home/admin/tools /home/admin/playbooks /home/admin/modules /home/admin/log /home/admin/.ssh \
    && chmod 700 /home/admin/.ssh
COPY configs/id_rsa configs/id_rsa.pub /home/admin/.ssh/
COPY configs/ssh_config /home/admin/.ssh/config

RUN chown -R admin:admin /home/admin \
    && chmod go-rw /home/admin/.ssh/id_rsa

WORKDIR /home/admin
USER admin

