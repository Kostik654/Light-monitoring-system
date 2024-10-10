#!/bin/bash

set -e

rm -rf /etc/monsys
rm -rf /var/log/monsys

mkdir /etc/monsys
mkdir /var/log/monsys

touch /var/log/monsys/monitor.log

cp ./templates/jobs_list.template /etc/monsys/jobs_list
cp ./templates/env.template /etc/monsys/.env

docker rm -f monitoring-system

docker-compose up -d --build

cd /etc/monsys/

docker ps -a

cat jobs_list
