#!/bin/bash
# add user to dockerg group to do not need sudo

# sudo groupadd docker
# sudo usermod -aG docker $USER

# logout and log back (or reboot)

# use --rm option if mongo db is epheremal
if [[ "$1" = "start" ]]; then
	docker run -d -p 27017-27019:27017-27019 --name mongodb --rm mongo
elif [[ "$1" = "stop" ]]; then
	docker stop -t 0 mongodb
fi
