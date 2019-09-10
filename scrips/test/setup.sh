#!/bin/bash
docker stop mongodb
docker run -d -p 27017-27019:27017-27019 --name mongodb --rm mongo
# python run_engine.py