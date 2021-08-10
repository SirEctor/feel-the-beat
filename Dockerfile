FROM python:3.8-slim-buster

RUN mkdir feel-the-beat-docker/
COPY requirements.txt /feel-the-beat-docker
WORKDIR /feel-the-beat-docker
RUN pip3 install -r requirements.txt

COPY . /feel-the-beat-docker

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]