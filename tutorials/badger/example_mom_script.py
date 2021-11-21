from glob import glob
from smartsim import Experiment
from smartsim.settings import SbatchSettings, SrunSettings
from smartsim.database import SlurmOrchestrator
from smartsim.utils.log import log_to_file
from smartsim import slurm
import sys
import os
import time

# create reference to MOM6 ensemble
mom_model = experiment.create_model("MOM", run_settings=mom_settings)

# Attach input files and configuration files to each
# MOM6 simulation
mom_model.attach_generator_files(
    to_configure=glob("../MOM6/MOM6_config/*"),
    to_copy="../MOM6/OM4_025_JRA",
    to_symlink="../MOM6/INPUT",
)

# configs to write into 'to_configure' files listed
# above. If you change the number of processors for
# each MOM6 simulation, you will need to change this.
MOM6_config = {
    "SIM_MONTHS": 12, # length of simlations
    "SIM_DAYS": 0,
    "DOMAIN_LAYOUT": "90,144",
    "MASKTABLE": "mask_table.3785.90x144",
    }
if is_restart:
    MOM6_config['IS_RESTART'] = 'r'
    restarts = glob(f'{ARCHIVE_DIRECTORY}/{run_year-1}/RESTART/*')
    for restart_file in restarts:
        safe_link(restart_file,f'../MOM6/INPUT/{os.path.basename(restart_file)}')
else:
    MOM6_config['IS_RESTART'] = 'n'

mom_model.params = MOM6_config

# register models so keys don't overwrite each other
# in the database
# model.register_incoming_entity(model)

# creation of ML database specific to Slurm.
# there are also PBS, Cobalt, and local variants
db = SlurmOrchestrator(db_nodes=DB_NODES, time="10:00:00",
    threads_per_queue=4,
    interface = "ipogif0")
db.set_cpus(36)
db.set_batch_arg("constraint", "P100")
db.set_batch_arg("exclusive", None)

# generate run directories and write configurations
experiment.generate(mom_model, db, overwrite=True)

# start the database and ensemble batch jobs.
experiment.start(mom_model, db, summary=True)

# print a summary of the run.
print(experiment.summary())

experiment.stop(db)
slurm.release_allocation(mom_alloc)

archive_run(mom_model.path,run_year)
os.remove(mom_model.path)
