from glob import glob
from smartsim import Experiment
from smartsim.settings import SbatchSettings, SrunSettings
from smartsim.database import SlurmOrchestrator
from smartsim.utils.log import log_to_file
from smartsim import slurm
import sys
import os
import time
import subprocess

DB_NODES=1
MODEL_NODES=1

# get an allocation we will stuff our database and model into
alloc = slurm.get_allocation(nodes=DB_NODES+MODEL_NODES,
                             time="10:00:00",
                             account="t22_ocean_time_step",
                             #options={"exclusive": None # totally optional constraints
                                      #,"constraint": "P100"
                             #         }
                             )


exp = Experiment("E3SM", launcher="slurm")

# if you want a database launched out on compute nodes (assuming this is what you want)
if DB_NODES > 0:
    db = SlurmOrchestrator(port=6379,
                           db_nodes=DB_NODES, # only 1 database (not a cluster)
                           batch=False, # not launching as a seperate batch workload
                           interface="ib0", # high speed network to use (usually ipogif0 for aries CrayXC 50)
                           alloc=alloc # launching into this allocation
                          )
    
    # this will block until db is launched and then release
    exp.start(db)
    print(f"Orchestrator launched on nodes: {db.hosts}")

case_dir = '/lustre/scratch3/turquoise/cbegeman/E3SM-Output/20211108_WCYCL1850NS_ne4_oQU480_master/'
os.chdir(case_dir)

# create reference to the job you will run
MODULEPATH=os.getenv('MODULEPATH')
USER=os.getenv('USER')
srun_settings = SrunSettings(exe="case.submit", alloc=alloc,
                             run_args={'-a --jobid':alloc},
                             env_vars={'MODULEPATH':MODULEPATH, 'USER':USER})
srun_settings.set_nodes(MODEL_NODES)

e3sm = exp.create_model("e3sm_with_db", srun_settings)

print(subprocess.check_output("echo $MODULEPATH", shell=True))

exp.start(e3sm, block=True, summary=True)
print(exp.get_status(e3sm))

if DB_NODES > 0:
    exp.stop(db)

#slurm.release_allocation(alloc)
