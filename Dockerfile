FROM jrottenberg/ffmpeg:4.1-vaapi

ADD requirements.txt /opt
RUN apt update && apt install python3-pip -y && pip3 install -r /opt/requirements.txt && mkdir -p /{input, output}
ADD . /opt
VOLUME ["/input", "/output"]

ENTRYPOINT ["/usr/bin/python3", "/opt/convert.py"]
CMD ["/input", "/output", "--verbose"]
