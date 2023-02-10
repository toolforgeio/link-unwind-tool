# Read our base image from ToolForge public images
FROM docker.toolforge.io/public/ubuntu:22.04

# Set up python3
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends python3 \
    && apt-get install -y --no-install-recommends python3-pip

# Set up our execution environment
WORKDIR /root
COPY main.py /root/
COPY requirements.txt /root/
COPY manifest.yml /toolforge/manifest.yml
RUN pip3 install -r requirements.txt

# Go!
ENTRYPOINT [ "python3", "main.py" ]