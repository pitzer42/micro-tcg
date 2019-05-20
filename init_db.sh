#!/usr/bin/env bash
sudo docker run -d -p 27017-27019:27017-27019 --name mongodb mongo
sudo docker exec -it mongodb bash