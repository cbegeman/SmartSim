#!/bin/bash

salloc --partition=debug --nodes=1 --time=00:30:00 -C haswell
source load_compass_env.sh
compass run
