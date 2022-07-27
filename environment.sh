#!/bin/bash
export RAI_PATH=/turquoise/users/cbegeman/envs/SmartSim-v0.3.2/lib/python3.8/site-packages/smartsim/lib/redisai.so
export REDIS_PATH=/usr/bin/redis-server
export REDIS_CLI_PATH=/usr/bin/redis-cli

# optional settings
export SMARTSIM_LOG_LEVEL=debug # (more verbose outputs)
export SMARTSIM_JM_INTERVAL=20  # (control how often SmartSim pings schedulers like Slurm)
