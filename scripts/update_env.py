import boto3
from dotenv import dotenv_values, set_key
import os
import sys

# Load existing environment variables from .env
env_file_path = './api/.env'
config = dotenv_values(env_file_path)

# Initialize a session using Boto3
session = boto3.session.Session()
ssm_client = session.client('ssm')

def fetch_parameters_from_ssm(parameter_names, with_decryption=True):
    try:
        response = ssm_client.get_parameters(
            Names=parameter_names, 
            WithDecryption=with_decryption
        )

        parameters = {}
        for param in response['Parameters']:
            parameters[param['Name']] = param['Value']

        if response.get('InvalidParameters'):
            print(f"Invalid parameters: {response['InvalidParameters']}")

        return parameters
    except Exception as e:
        print(f"Error fetching parameters: {e}")
        return {}

def update_env_file(parameters):
    for key, value in parameters.items():
        key_name = key.split('/')[-1].upper()
        set_key(env_file_path, key_name, value)
        print(f"Updated {key_name} in .env file.")
    set_key(env_file_path, 'DEPLOYED', 'True')

def main(env):
    parameter_keys_1 = [
        "SECRET_KEY", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD",
        "JIRA_BASE_URL", "JIRA_TOKEN", "JIRA_BOARD_ID", "JIRA_PROJECT", "JIRA_EPIC_ISSUETYPE"
    ]
    parameter_keys_2 = [
        "FRESHDESK_BASE_URL", "FRESHDESK_AUTH_USER", "FRESHDESK_AUTH_PASSWORD",
        "FRESHDESK_GROUP_ID", "AWS_SITE_URL", "DST_SUPERUSER_EMAIL", "DST_SUPERUSER_PASSWORD"
    ]

    for parameter_keys in [parameter_keys_1, parameter_keys_2]:
        full_paths = [f"/dst/{env}/{key}" for key in parameter_keys]
        parameters = fetch_parameters_from_ssm(full_paths)
        if parameters:
            update_env_file(parameters)
            print(".env file updated successfully.")
        else:
            print("No parameters fetched from SSM.")

if __name__ == "__main__":
    if not os.path.exists(env_file_path):
        open(env_file_path, 'a').close()

    if len(sys.argv) != 2:
        print("Usage: python3 update_env.py <environment>")
        sys.exit(1)

    env_arg = sys.argv[1]
    main(env_arg)
