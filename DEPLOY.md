# Data Submission Tracker Deployment Guide -test
The Data Submission Tracker (DST) is a web-based tool for following the progress of Data Submissions through the NHLBI BioData Catalyst Data Management Core ingest pipeline, allowing self-service data submission and tracking. The tool is designed to be deployed on a cloud platform, such as Google Cloud Platform (GCP) or Amazon Web Services (AWS), and is built using the Django web framework in Docker containers with a PostgreSQL database.

This guide will walk you through the deployment process for the Data Submission Tracker, including setting up the necessary environment variables, deploying the Django server, and configuring the database. Currently, the tool is deployed to an AWS EC2 instance; we will document the steps for deploying to AWS. If other cloud platforms are used we will need to modify this guide to reflect the changes.

## Getting started
See the CONTRIBUTING.md file for information on how to set up the repository for development and install the prerequisites. 

## New Instance Deployment Instructions
Deployment of the Data Submission Tracker requires an AWS EC2 instance. Once the instance is set up, we will install docker, clone the repository, run the docker images, and set up the PostgreSQL database. Then the Django server will be deployed and accessible through the public IP address of the EC2 instance.

### Create a new AWS EC2 instance
If you do not already have access to an AWS instance for the DST, you will need to create one. To set up the appropriate instance for the DST, create a new EC2 instance with the following specifications:

- **Instance Type**: t2.micro
- **Operating System**: Ubuntu Server 24.04 LTS
- **Storage**: 12 GB
- **Security Group**: Open ports 22, 80, 800, and 443
  - The existing security group for the DST is called `launch-wizard-1`
  - Note: We'll be changing the security group to `bdcat-data-tracker-sg` in the future
- **Key Pair**: Use the DataSubmissionTool key pair or create a new one
- **Tags**: Add the following tags to the instance
  - Name: DataSubmissionTool
  - Owner: Your Name
- **Network**: Use the default VPC or create a new one
- **Public IP**: Enable a public IP address for the instance?
- **Elastic IP**: Allocate an Elastic IP address for the instance?
- **Security Group**: Use the existing security group or create a new one

### Connect to the EC2 instance
Once the instance is set up, connect to the instance using SSH. You can use the following command to connect to the instance:

```bash
ssh -i DataSubmissionTool.pem ubuntu@<instance-public-ip>
```

### Install Docker
We're using docker containers to run the Django server and PostgreSQL database. We will need to install Docker on the EC2 instance.

#### Prepare for installation
Make sure everything is up-to-date and allow using a repository over HTTPS
```shell
sudo apt update
sudo apt install -y ca-certificates curl gnupg
```

#### Add Docker GPG Key
We need the Docker official GPG public key to use their apt repository.
```shell
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

#### Update Apt to fetch Docker Repository
We need to update the Apt cache in order to install from the Docker repository.
```shell
sudo apt update
```
This should show a line accessing downloader.docker.com for the systems installed release.

#### Install Docker and tools
Now we can install Docker Engine, containerd, and Docker Compose. This will install the latest version, which is currently version 24.0.2.
```shell
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose docker-compose-plugin
```
If you need to install a different version see the [Docker Engine Installation](https://docs.docker.com/engine/install/ubuntu/#install-docker-engine) page.

#### Fix Docker permissions
Docker requires root access to run. This is a security risk and we need to fix it. The recommended way to do this is to add your user to the docker group. This will allow your user to run docker commands without sudo.
```shell
sudo usermod -aG docker ${USER}
```
You will then need to log in again or run the command below to gain the group permissions.
```shell
newgrp docker
```

### Clone the repository
Once you are connected to the instance, clone the Data Submission Tracker repository to the instance. You can use the following command to clone the repository:

```bash
export GITHUB_USER=your-github-username
export GITHUB_TOKEN=your-github-token
git clone https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/amc-corey-cox/BDC_Dashboard.git
```

### Copy the .env file
The Data Submission Tracker uses environment variables to configure the Django server. You will need to copy the `.env` file to the `api` directory. You can use the following command to copy the `.env` file:

```bash
cp api/.env.sample api/.env
```
Set up the environment variables in the `.env` file with the appropriate values for your deployment.

### Set up nginx
We need a local proxy to send the requests to the application after the docker containers are running.
```bash
cp nginx.default /etc/nginx/sites-available/default
sudo service nginx start
```

### Build and run the Docker images
The Data Submission Tracker uses Docker containers to run the Django server and PostgreSQL database. You will need to build the Docker images for the Django server and PostgreSQL database. You can use the following commands to build the Docker images:

```bash 
./docker-compose-up.sh
```

### Set up the PostgreSQL database
Before deploying the Django server, you will need to set up the PostgreSQL database. You can use the following commands to set up the PostgreSQL database:

```bash 
docker exec -it bdc-dashboard-app /bin/bash
python manage.py createsuperuser
```
Enter the appropriate values for the superuser when prompted.

### Set up Let's Encrypt SSL certificate
The Data Submission Tracker uses Let's Encrypt to secure the Django server with an SSL certificate. You will need to set up the Let's Encrypt SSL certificate for the Django server. You can use the following commands to set up the Let's Encrypt SSL certificate:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx
```
Follow the prompts to set up the Let's Encrypt SSL certificate for the Django server.

### Configure Nginx
The Data Submission Tracker uses Nginx as a reverse proxy server to route traffic to the Django server. You will need to configure Nginx to route traffic to the Django server. You can use the following commands to configure Nginx:

```bash
sudo apt install nginx
sudo rm /etc/nginx/sites-enabled/default
sudo cp /home/ubuntu/BDC_Dashboard/deployment/nginx/bdc-dashboard /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/bdc-dashboard /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Nginx Configuration
The Nginx configuration file is located at `/etc/nginx/sites-available/bdc-dashboard`. You can edit this file to configure the Nginx server. The configuration file should look like this:

```nginx
server {
    listen 80;
    server_name your-deployed-domain.com www.your-deployed-domain.com;

    # Redirect all HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your-deployed-domain.com www.your-deployed-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-deployed-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-deployed-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```




### Access the Data Submission Tracker
Once the Django server is deployed, you can access the Data Submission Tracker by navigating to the public IP address of the EC2 instance in your web browser. You should see the Data Submission Tracker homepage, where you can log in and begin using the tool.

## Updating the Data Submission Tracker





# Old Deployment Instructions

### Environment variables
For local development, the `api` directory should have an `.env` file with the following:

| name                    | value      | description                                                   |
| ----------------------- | ---------- | ------------------------------------------------------------- |
| DEBUG                   | `False`    | Set to `True` for local dev and `False` for prod              |
| DJANGO_LOG_LEVEL        |            | Set to `DEBUG` for local dev and `INFO` for prod              |
| SECRET_KEY              |            | The `SECRET_KEY` generated by Django                          |
| POSTGRES_DB             | `postgres` | The Postgres database name                                    |
| POSTGRES_USER           |            | The username of the Postgres User                             |
| POSTGRES_PASSWORD       |            | A (secure) password for the Postgres User                     |
| POSTGRES_HOST           |            | The external IP for the Compute Engine instance with Postgres |
| POSTGRES_PORT           | `5432`     | The port for the Postgres Database                            |

### The Postgres Database
In order to run, the Django tool-chain must have access to a Postgres database to manage stored information. For local development, the docker-compose-up.sh script will start a Postgres container with the necessary configuration. Once the postgres container is running, you will need to log into the app container and create a superuser to access the admin panel. The superuser can be created by running the following command in the app container:
```
docker exec -it bdcat-data-tracker_app /bin/bash
python manage.py createsuperuser
```

For deployment, the Postgres database my require addiational or manual configuration. The Postgres database must be accessible to the Django tool-chain via the `POSTGRES_HOST` environment variable.

### The Django Server

Docker Compose should start a Django server on [`http://0.0.0.0:8000/`](http://0.0.0.0:8000/).
The server uses the `.env` file for configuration

### Admin Panel

NHLBI Admins are able to view all tickets, but Data Custodians are only able to view their own tickets.
In the code, Admins are `staff`.
To access the Admin panel visit [`http://localhost:8000/admin`](http://localhost:8000/admin) as a `superuser` member

Go to the "Tracker/User" panel and select the user you want to grant admin permissions.
You should only need to check the `Is staff` permission for HNLBI Admins.
If you would like to allow that user to access the Admin panel, check the `Is superuser` permission as well

> NOTE: Make sure you save your changes at the bottom

### Docker Compose
Docker is used to standardize the development environment. For automatic setup locally, run the following command in the root directory:

```commandline
bash docker-compose-up.sh
```
You can also run `./docker-compose-up.sh`.

To setup the app manually, run the following commands in the `api` directory:

```commandline
docker-compose up --build
```

> NOTE: This may take a several minutes

You should only need to build this once (or when you make changes to the `Dockerfile` or `docker-compose.yml`).
Any subsequent runs do not require the `--build` flag:

To take down the containers, run the following command in the root directory:

```commandline
bash docker-compose-down.sh
```
You can also run `./docker-compose-down.sh`.

Alternatively, each container can be stopped individually:

```commandline
docker stop bdcat-data-tracker_app
docker stop bdcat-data-tracker_db
```

## Deployment

#### GitHub Secrets

For your convenience, this repo contains automatic deployment scripts.
These scripts will run depending on different triggers as detailed in the [`.github/workflows/`](.github/workflows/) directory.
To utilize these scripts, you will need to create a GitHub Secret with the following:

| name                 | description                             |
| -------------------- | --------------------------------------- |
| SECRET_KEY           | The `SECRET_KEY` generated by Django    |
| QUAY_NIMBUS_USERNAME | A username with access to the Quay repo |
| QUAY_NIMBUS_PASSWORD | The password of the Quay user           |

> NOTE: You can read more about this in the [Quay section below](#Quay)

### Instructions

**Ensure all prior setup is complete before continuing**

To prepare the project for deployment, run the following commands in the `api` directory:

```
python manage.py collectstatic --noinput
python manage.py makemigrations tracker
python manage.py migrate
```

> NOTE: The `collectstatic` command is not required if you are using the GitHub Actions workflow



# Everything below this line is for the old deployment method and is only here for reference

#### Quay

This repo has been configured to use GitHub Actions to build and push images to Quay on pushes to the `main` branch.
Specifically, the `Dockerfile` in the `api` directory will be used to build the image.
The image will be pushed to the [`nimbusinformatics/bdcat-data-tracker`](https://quay.io/repository/nimbusinformatics/bdcat-data-tracker) repository on Quay.
The image will be named `quay.io/nimbusinformatics/bdcat-data-tracker` and two tags: `latest` and a shortened commit hash.
Be sure to include the following in your GitHub Secrets:

| name                 | description                             |
| -------------------- | --------------------------------------- |
| QUAY_NIMBUS_USERNAME | A username with access to the Quay repo |
| QUAY_NIMBUS_PASSWORD | The password of the Quay user           |

> NOTE: Robot accounts are the preferred method of pushing images to Quay.
> These accounts are usually in the format: `<repo-name+<robot-name>`

##### Testing the Image

You can test the image locally by pulling the image from Quay

```
docker pull quay.io/nimbusinformatics/bdcat-data-tracker:latest
```

> NOTE: You will need a RedHat account with the correct permissions to pull the image

When running the image, you must bind a port to the container to access the API

```
docker run -p 8000:8000 quay.io/nimbusinformatics/bdcat-data-tracker:latest
```

A more detailed writeup can be found on the [Quay repository](https://quay.io/repository/nimbusinformatics/bdcat-data-tracker?tab=info)

#### Microsoft Azure

Azure must be set up manually.
You can find a detailed writeup in the [`azure`](/azure) directory

#### Google Cloud

We will be using [this guide to deploy to App Engine](https://cloud.google.com/python/django/appengine#macos-64-bit)

##### [Permissions](https://cloud.google.com/iam/docs/understanding-roles#predefined)

- [`roles/appengine.appAdmin`](https://cloud.google.com/iam/docs/understanding-roles#app-engine-roles)
- [`roles/cloudbuild.integrationsOwner`](https://cloud.google.com/iam/docs/understanding-roles#cloud-build-roles)
- [`roles/cloudbuild.builds.editor`](https://cloud.google.com/build/docs/iam-roles-permissions#predefined_roles)
- [`roles/secretmanager.admin`](https://cloud.google.com/iam/docs/understanding-roles#secret-manager-roles)
- [`roles/iam.serviceAccountAdmin`](https://cloud.google.com/iam/docs/understanding-roles#service-accounts-roles)
- [`roles/serviceusage.serviceUsageAdmin`](https://cloud.google.com/iam/docs/understanding-roles#service-usage-roles)
- [`roles/storage.admin`](https://cloud.google.com/iam/docs/understanding-roles#cloud-storage-roles)

> NOTE: You will also need to grant yourself the [`roles/iam.serviceAccountUser`](https://cloud.google.com/iam/docs/understanding-roles#service-accounts-roles) on the `App Engine default service account`

##### [Secrets Manager](https://cloud.google.com/python/django/appengine#create-django-environment-file-as-a-secret)

In GCP Secret Manager, you must create a secret called `django_settings`.
You can either upload the `.env` file or paste the secrets in there

> NOTE: If the Compute Engine instance restarts and the IP changes, you must update the `POSTGRES_HOST` variable

##### App Engine

This repo has been configured to use GitHub Actions to deploy to App Engine on pushes to the `main` branch.
For this to work, you must have GitHub Secrets with the following:

| name       | description                                         |
| ---------- | --------------------------------------------------- |
| PROJECT_ID | The Project ID for GCP                              |
| GCP_SA_KEY | The full service account key json exported from GCP |

Alternatively, can navigate to the `api` directory and run:

```
gcloud app deploy
```

#### SendGrid

You will also need to create your own dynamic templates and copy the `TEMPLATE_ID` and assign them into the correct variables in the [`mail.py`](/api/tracker/templates) file

The dynamic templates use handlebars syntax.
These must be included in the dynamic template you make on SendGrid.
These variables are listed under the `self.dynamic_template_data` dictionary of the [`mail.py`](/api/tracker/mail.py) file.
Some templates have been provided for you, but you must create your own if you want to make edits

> NOTE: You will need to [verify the sender identity in SendGrid]("https://docs.sendgrid.com/for-developers/sending-email/sender-identity") for the `SENDGRID_ADMIN_EMAIL`
