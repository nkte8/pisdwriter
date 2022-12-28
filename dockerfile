FROM ubuntu:22.04

WORKDIR /tmp/workspace

COPY ./ /tmp/workspace/

RUN apt-get update && \
        apt-get install -y \
        python3 \
        python3-pip \
        wpasupplicant

RUN pip3 install --upgrade pip setuptools wheel && \
    python3 setup.py bdist_wheel && \
    pip3 install dist/PiSDWriter*.whl

ENTRYPOINT ["/bin/sh"]