import boto3
from dotenv import dotenv_values, set_key
import os

# Load existing environment variables from .env
env_file_path = './api/.env'
config = dotenv_values(env_file_path)

# Initialize a session using Boto3
session = boto3.session.Session()
ssm_client = session.client('ssm')

def fetch_parameters_from_ssm(parameter_names, with_decryption=True):
    """
    Fetch parameters from AWS SSM Parameter Store.

    :param parameter_names: List of parameter names to fetch
    :param with_decryption: Whether to decrypt secure string parameters
    :return: Dictionary of parameter names and their values
    """
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
    """
    Update the .env file with the fetched parameters.

    :param parameters: Dictionary of parameters to update
    """
    for key, value in parameters.items():
        # Ensure keys are formatted correctly for environment variables
        key_name = key.split('/')[-1].upper()

        # Update the .env file
        set_key(env_file_path, key_name, value)
        print(f"Updated {key_name} in .env file.")

def main():
    # List of parameter names to fetch from SSM
    parameter_names = [
        "/dst/dev/SECRET_KEY",
        "/dst/dev/POSTGRES_DB",
        "/dst/dev/POSTGRES_USER",
        "/dst/dev/POSTGRES_PASSWORD",
        "/dst/dev/JIRA_BASE_URL",
        "/dst/dev/JIRA_TOKEN",
        "/dst/dev/JIRA_BOARD_ID",
        "/dst/dev/JIRA_PROJECT",
        "/dst/dev/JIRA_EPIC_ISSUETYPE"
        
    ]

    # Fetch parameters from SSM Parameter Store
    parameters = fetch_parameters_from_ssm(parameter_names)

    if parameters:
        # Update the .env file with fetched parameters
        update_env_file(parameters)
        print(".env file updated successfully.")
    else:
        print("No parameters fetched from SSM.")
        
    # Beacuse only up to 10 parameters might be fetched a a time
    # List of parameter names to fetch from SSM
    parameter_names = [
        "/dst/dev/FRESHDESK_BASE_URL",
        "/dst/dev/FRESHDESK_AUTH_USER",
        "/dst/dev/FRESHDESK_AUTH_PASSWORD",
        "/dst/dev/FRESHDESK_GROUP_ID",
        "/dst/dev/AWS_SITE_URL",
        "/dst/dev/DST_SUPERUSER_EMAIL",
        "/dst/dev/DST_SUPERUSER_PASSWORD"
    ]

    # Fetch parameters from SSM Parameter Store
    parameters = fetch_parameters_from_ssm(parameter_names)

    if parameters:
        # Update the .env file with fetched parameters
        update_env_file(parameters)
        print(".env file updated successfully.")
    else:
        print("No parameters fetched from SSM.")
                

if __name__ == "__main__":
    # Ensure .env file exists
    if not os.path.exists(env_file_path):
        open(env_file_path, 'a').close()

    main()
