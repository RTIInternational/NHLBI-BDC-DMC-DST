# syntax=docker/dockerfile:1
FROM ubuntu:24.04

# FOR MAC users uncomment the line below and comment "FROM ubuntu:24.04"
#FROM --platform=linux/amd64 ubuntu:24.04

ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TINI_VERSION=v0.19.0

WORKDIR ${APP_HOME}

# Install dependencies and Python 3.12
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3.12-dev \
    wget curl git build-essential libpq-dev \
    && ln -s /usr/bin/python3.12 /usr/bin/python3 \
    && ln -s /usr/bin/python3.12 /usr/bin/python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install tini
RUN wget https://github.com/krallin/tini/releases/download/$TINI_VERSION/tini -O /sbin/tini && chmod +x /sbin/tini

COPY . ./

# Install Python dependencies
RUN python3 -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Django collectstatic
RUN . /opt/venv/bin/activate \
    && python3 /app/manage.py collectstatic --noinput

# Adjust permissions
RUN chmod a+w ${APP_HOME}/tracker/migrations \
    && chmod a+x ${APP_HOME}/docker_entrypoint.sh \
    && chown -R 1001:0 ${APP_HOME}

USER 1001

ENTRYPOINT ["/sbin/tini", "--"]
EXPOSE 8000 2222
CMD ["./docker_entrypoint.sh"]