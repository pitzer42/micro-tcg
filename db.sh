#!/usr/bin/env bash
if [[ "$1" = "start" ]]
then
    sudo docker run -d -p 27017-27019:27017-27019 --name mongodb mongo
elif [[ "$1" = "stop" ]]
then
    sudo docker stop mongodb
    sudo docker rm mongodb
fi