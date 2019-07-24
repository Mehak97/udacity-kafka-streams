FROM ubuntu:16.04

RUN apt-get update && apt-get install software-properties-common sudo -y
RUN apt-add-repository ppa:ansible/ansible -y
RUN apt-get update && apt-get install ansible git -y

ADD requirements.yaml requirements.yaml
RUN ansible-galaxy install -r requirements.yaml

ADD playbook.yaml playbook.yaml
RUN ansible-playbook playbook.yaml
