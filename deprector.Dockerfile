FROM python:3.11.0-bullseye

RUN set -ex; \
    apt-get update; \
    apt-get install -y git-core build-essential;

ADD . /deprector_bot
WORKDIR /deprector_bot
RUN python -m pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]