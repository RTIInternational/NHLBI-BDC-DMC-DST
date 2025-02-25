# syntax=docker/dockerfile:1
FROM ubuntu:25.04

# Set environment variables
ENV APP_HOME=/app \
  PYTHONUNBUFFERED=1 \
  TINI_VERSION=v0.19.0

# Set working directory
WORKDIR ${APP_HOME}

# Install system dependencies
RUN apt-get update -y && apt-get install -y \
  python3.13 python3.13-dev python3.13-venv \
  gcc g++ libffi-dev libssl-dev wget curl \
  && rm -rf /var/lib/apt/lists/*

# Install Tini for proper signal handling
RUN wget https://github.com/krallin/tini/releases/download/$TINI_VERSION/tini -O /sbin/tini && \
  chmod +x /sbin/tini

# Copy application files
COPY . ./

# Create virtual environment
RUN python3.13 -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r requirements.txt

# Ensure Django loads the .env file during the build
COPY .env ./.env
RUN /venv/bin/python -c "import environ; env = environ.Env(); env.read_env('.env')"
# Run collectstatic for Django
RUN /venv/bin/python /app/manage.py collectstatic --noinput

# Ensure correct permissions
RUN chmod a+w ${APP_HOME}/tracker/migrations && \
  chmod a+x ${APP_HOME}/docker_entrypoint.sh && \
  chmod +x /sbin/tini && \
  chown -R 1001:0 ${APP_HOME}

# Make entrypoint script executable
RUN chmod +x /app/docker_entrypoint.sh

# Switch to non-root user
USER 1001

# Set entrypoint and expose necessary ports
ENTRYPOINT ["/sbin/tini", "--"]
EXPOSE 8000 2222
CMD ["/venv/bin/python", "/app/docker_entrypoint.sh"]
