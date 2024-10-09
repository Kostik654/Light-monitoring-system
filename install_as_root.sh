#!/bin/bash

set -e

rm -rf /etc/monsys
mkdir /etc/monsys

cp ./templates/jobs_list.template /etc/monsys/jobs_list
cp ./templates/env.template /etc/monsys/.env

docker-compose up -d --build

cd /etc/monsys/

docker ps -a

cat jobs_list
