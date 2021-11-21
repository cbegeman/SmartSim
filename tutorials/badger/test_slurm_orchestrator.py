from glob import glob
from smartsim import Experiment
from smartsim.settings import SbatchSettings, SrunSettings
from smartsim.database import SlurmOrchestrator
from smartsim.utils.log import log_to_file
from smartsim import slurm
import sys
import os
import time

DB_NODES=1
MODEL_NODES=1

# get an allocation we will stuff our database and model into
alloc = slurm.get_allocation(nodes=DB_NODES+MODEL_NODES,
                             time="10:00:00",
                             account="e3sm",
                             #options={"exclusive": None # totally optional constraints
                                      #,"constraint": "P100"
                             #         }
                             )

exp = Experiment("E3SM", launcher="slurm")

# if you want a database launched out on compute nodes (assuming this is what you want)
db = SlurmOrchestrator(port=6379,
                       db_nodes=1, # only 1 database (not a cluster)
                       batch=False, # not launching as a seperate batch workload
                       interface="ib0", # high speed network to use (usually ipogif0 for aries CrayXC 50)
                       alloc=alloc # launching into this allocation
                      )

# this will block until db is launched and then release
exp.start(db)
print(f"Orchestrator launched on nodes: {db_cluster.hosts}")

os.chdir('/lustre/scratch4/turquoise/cbegeman/E3SM/scratch/20211108_WCYCL1850NS_ne4_oQU480_master/')

# create reference to the job you will run
srun_settings = SrunSettings(exe="case.submit", alloc=alloc)
e3sm = exp.create_model("e3sm_test", srun_settings)
print(exp.get_status(model))

exp.stop(db_cluster)
