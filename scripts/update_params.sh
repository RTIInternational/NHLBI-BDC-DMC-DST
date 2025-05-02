#!/bin/bash
#cp scripts/update_env.py /home/ubuntu/dst-pipeline/scripts
#cp api/.env.sample /home/ubuntu/dst-pipeline/scripts/api/.env
cd /home/ubuntu/dst-pipeline/scripts

cp api/.env.sample /home/ubuntu/dst-pipeline/scripts/api/.env
sudo chown ubuntu -R /home/ubuntu/dst-pipeline/scripts/api
python3 update_env.py test

chmod  664 /home/ubuntu/dst-pipeline/scripts/api/.env