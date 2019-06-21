#!/usr/bin/env bash

rm *.dot

pyreverse -AS engine
mkdir diagrams/engine
mv *.dot diagrams/engine/.

pyreverse -AS game
mkdir diagrams/game
mv *.dot diagrams/game/.