FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y software-properties-common \
               && add-apt-repository ppa:deadsnakes/ppa \
               && apt install -y python3.10 && apt install -y python3.11 \
               && apt install -y python3-pip && pip3 install tox

VOLUME /code

WORKDIR /code
ENTRYPOINT tox
CMD ["-e", "ci"]
