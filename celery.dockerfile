FROM python:latest
ENV PYTHONUNBUFFERED 1

#ENV C_FORCE_ROOT true

ENV APP_USER myapp
ENV APP_ROOT /src
RUN mkdir /src;
RUN groupadd -r  \
    && useradd -r -m \
    --home-dir  \
    -s /usr/sbin/nologin \
    -g  

WORKDIR 

RUN mkdir /config
ADD requirements.txt /config/
RUN pip install --no-cache-dir -r /config/requirements.txt

USER 
ADD . 
