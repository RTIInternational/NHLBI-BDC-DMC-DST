#!/bin/bash
cp scripts/upda_env.py /home/ubuntu/dst-pipeline/scripts
cp api/.env.sample /home/ubuntu/dst-pipeline/scripts
cd /home/ubuntu/dst-pipeline/scripts

python3 update_env.py