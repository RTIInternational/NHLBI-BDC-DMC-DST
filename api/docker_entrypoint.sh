#!/usr/bin/bash

export PATH="/.pyenv/bin:${PATH}"; \
eval "$(pyenv init -)"; \

# Apply database migrations
echo "Apply database migrations"
python3 manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

# Address vulnarebilities findings
pip install --upgrade certifi

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000