#!/bin/bash

cp -f /data/config.py /usr/src/app/

python /usr/src/app/pypod.py | tee /data/log.txt