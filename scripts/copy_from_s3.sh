#!/bin/bash
#docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
#docker rmi $(docker images -q)


#!/bin/bash
sudo rm /home/ubuntu/dst-pipeline/nhlbi-bdc-dmc-dst_bdc-dashboard-app-test.tar

aws s3 cp s3://bdc-dmc-dst-dashboard-app/nhlbi-bdc-dmc-dst_bdc-dashboard-app-test.tar /home/ubuntu/dst-pipeline




