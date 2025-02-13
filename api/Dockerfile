# syntax=docker/dockerfile:1
FROM registry.access.redhat.com/ubi8/python-311@sha256:ec7fe289b34142aa81a620d49fc4fffb7f329c419a2d45780bd9055a4e106bee

#FROM --platform=linux/amd64 registry.access.redhat.com/ubi8/python-311@sha256:ec7fe289b34142aa81a620d49fc4fffb7f329c419a2d45780bd9055a4e106bee

ENV APP_HOME=/app \
  PYTHONUNBUFFERED=1 \
  TINI_VERSION=v0.19.0

WORKDIR ${APP_HOME}

COPY . ./

USER 0
RUN set -eux; \
  yum update -y; \
  # install tini
  wget https://github.com/krallin/tini/releases/download/$TINI_VERSION/tini -O /sbin/tini; \
  # install python modules
  python3.11 -m pip install --upgrade pip; \
  python3.11 -m pip install -r requirements.txt; \
  python3.11 -m pip install --upgrade certifi django cryptography; \
  
  # Django collectstatic
  python3.11 /app/manage.py collectstatic --noinput; \

  pip install --upgrade certifi; \
  pip install --upgrade cryptography; \
  python3 -c "import certifi; print(certifi.__version__)"; \
  python3 -c "import cryptography; print(cryptography.__version__)"; \
  python3.11 -c "import certifi; print(certifi.__version__)"; \
  python3.11 -c "import cryptography; print(cryptography.__version__)"; \
  

  # add perms
  chmod a+w ${APP_HOME}/tracker/migrations; \
  chmod a+x ${APP_HOME}/docker_entrypoint.sh; \
  chmod +x /sbin/tini; \
  chown -R 1001:0 ${APP_HOME};


USER 1001


ENTRYPOINT ["/sbin/tini", "--"]
EXPOSE 8000 2222
CMD ["./docker_entrypoint.sh"]