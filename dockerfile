FROM ubuntu:22.04

WORKDIR /tmp/workspace

COPY ./ /tmp/workspace/

RUN apt-get update && \
        apt-get install -y \
        python3 \
        python3-pip \
        wpasupplicant

RUN python3 setup.py install

ENTRYPOINT ["/bin/sh"]