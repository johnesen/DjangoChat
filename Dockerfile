FROM python:3.10

RUN mkdir -p /opt/services/njohnny

WORKDIR /opt/services/njohnny

COPY . /opt/services/njohnny/

RUN pipenv install