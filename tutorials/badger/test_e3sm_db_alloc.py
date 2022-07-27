from glob import glob
from smartsim import Experiment
from smartsim.settings import SbatchSettings, RunSettings
from smartsim.database import SlurmOrchestrator
from smartsim.utils.log import log_to_file
from smartsim import slurm
import sys
import os
import time
import subprocess

DB_NODES=1
MODEL_NODES=1

case_dir = '/lustre/scratch3/turquoise/cbegeman/E3SM-Output/20211108_WCYCL1850NS_ne4_oQU480_master/'
os.chdir(case_dir)

if os.path.exists('{}/jobid.sh'.format(case_dir)):
    os.system('rm {}/jobid.sh'.format(case_dir))
if os.path.exists('{}/SSDB.sh'.format(case_dir)):
    os.system('rm {}/SSDB.sh'.format(case_dir))

exp = Experiment("E3SM", launcher="local")

# create reference to the job you will run
MODULEPATH=os.getenv('MODULEPATH')
USER=os.getenv('USER')
run_settings = RunSettings(exe="case.submit",
                           env_vars={'MODULEPATH':MODULEPATH, 'USER':USER})

e3sm = exp.create_model("e3sm_test", run_settings)

exp.start(e3sm, block=False, summary=True)
print(exp.get_status(e3sm))
