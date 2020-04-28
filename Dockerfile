FROM python:3-slim

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/nyquist/scorobot.git

WORKDIR /usr/src/app/scorobot
RUN git checkout version2


VOLUME /usr/src/app/scorobot/storage

CMD [ "python", "-m","scorobot" ]