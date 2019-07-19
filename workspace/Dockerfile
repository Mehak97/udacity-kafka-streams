FROM ubuntu:16.04

RUN apt-get update && apt-get install wget -y

RUN wget -O - https://repo.saltstack.com/py3/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -

RUN echo "deb http://repo.saltstack.com/py3/ubuntu/16.04/amd64/latest xenial main" >> /etc/apt/sources.list.d/saltstack.list

RUN apt-get update

RUN apt-get install salt-master salt-minion python-pygit2 -y

RUN echo "file_client: local" >> /etc/salt/minion
RUN cat /etc/salt/master >> /etc/salt/minion

RUN echo '\n\
fileserver_backend: \n\
  - git\n\
  - roots\n\
\n\
gitfs_remotes:\n\
  - https://github.com/saltstack-formulas/zookeeper-formula\n\
  - https://github.com/benjigoldberg/kafka-formula' >> /etc/salt/minion

RUN cat /etc/salt/minion | grep "gitfs_remotes" -A 3 -B 5

RUN mkdir -p /srv/salt
ADD salt /srv/salt

RUN salt-call --local state.apply
