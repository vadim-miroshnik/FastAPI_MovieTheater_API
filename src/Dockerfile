FROM python:3.9.7 

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN set -xe; \
    apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY ./requirements.txt /usr/src/app

# install dependencies
RUN pip install --upgrade pip && \ 
    pip install -r requirements.txt --no-cache-dir

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["bash", "/usr/src/app/entrypoint.sh"]

