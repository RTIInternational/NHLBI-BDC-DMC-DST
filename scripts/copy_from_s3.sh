#!/bin/bash


#!/bin/bash
sudo rm /home/ubuntu/dst-pipeline/nhlbi-bdc-dmc-dst_bdc-dashboard-app.tar

aws s3 cp s3://bdc-dmc-dst-dashboard-app/nhlbi-bdc-dmc-dst_bdc-dashboard-app.tar /home/ubuntu/dst-pipeline



