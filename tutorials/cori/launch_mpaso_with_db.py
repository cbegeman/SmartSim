from smartredis import Client
from smartsim import Experiment
from smartsim.database import Orchestrator

MPASO_DIR="/global/homes/c/cbegeman/MPAS-Ocean-test-case-output/smartsim/ocean/baroclinic_channel/10km/default"

print('Create Experiment object')
exp = Experiment("mpas-ocean_simulation", launcher="slurm")
print('Create database')
db = exp.create_database(db_nodes=1,
                         port=6379,
                         batch=True,
                         interface="lo",
                         time="00:30:00",
                         account="e3sm",
                         partition="debug",
                         batch_args={"C":"haswell"})


# define how simulation should be executed
print('Set run settings')
settings = exp.create_run_settings(f"{MPASO_DIR}/forward/ocean_model", 
                                   exe_args=["-n namelist.ocean",
                                             "-s streams.ocean"])
# Option 1 will look something like
#settings = exp.create_run_settings(f"{MPASO_DIR}/run_ocean_model.sh")
# And option 1's bash script will look something like
#--------------------------
#!/bin/bash
#source load_compass_env.sh
#compass run
#--------------------------

# Option 2 will look something like
#settings = exp.create_run_settings("sbatch",
#                                    f"{MPASO_DIR}/submit_ocean_model")

# This option gives the error "compass executable not found"
#settings = exp.create_run_settings("compass", 
#                                   exe_args=["run"])

# Invoke this line if using launcher="slurm"
#     settings.set_nodes(1)
print('Create model')
model = exp.create_model("mpas-ocean", settings)

# Include this line to add machine learning scripts
#   model.attach_generator_files(to_copy="ml.py")

# start the database and connect client to get data
print('Start database')
exp.start(db)
print('Create client object')
client = Client(address="127.0.0.1:6379", cluster=False)

# block=True appears to be used to make the model wait for the
# client to be launched before execution
#print('Start experiment')
#exp.start(model, block=True, summary=True)

# launch models, anaylsis, training, inference sessions, etc
# that communicate with the database using the SmartRedis clients
print(exp.get_status(db))
print(exp.get_status(model))
