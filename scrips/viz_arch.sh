#!/usr/bin/env bash

rm *.dot

pyreverse -AS engine
rm -rf diagrams/engine
mkdir diagrams/engine
mv *.dot diagrams/engine/.

pyreverse -AS game
rm -rf diagrams/game
mkdir diagrams/game
mv *.dot diagrams/game/.

pyreverse -AS test
rm -rf diagrams/test
mkdir diagrams/test
mv *.dot diagrams/test/.