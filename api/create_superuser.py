# create_superuser.py
import os
import django
import environ

# Set DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bdcat_data_submission.settings")

# Load env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    print("Using local .env file: " + env_file)
    env.read_env(env_file)
else:
    print("No local .env detected. Using container environment variables.")

# Setup Django (must come BEFORE get_user_model)
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Get credentials 
email = env("DST_SUPERUSER_EMAIL")
password = env("DST_SUPERUSER_PASSWORD")

# Create superuser if it doesn't exist
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print(f"Superuser '{email}' created.")
else:
    print(f"Superuser '{email}' already exists.")

