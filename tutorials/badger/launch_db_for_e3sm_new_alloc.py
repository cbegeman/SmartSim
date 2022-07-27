from glob import glob
from smartsim import Experiment
from smartsim.settings import SbatchSettings, RunSettings
from smartsim.database import Orchestrator
from smartsim.log import get_logger, log_to_file
from smartsim import slurm
import sys
import os
import time
import subprocess
import argparse

db_command_input = 'echo "Entering launch_db"'
db_command = subprocess.run(db_command_input, shell=True, capture_output=True)

parser = argparse.ArgumentParser()
#parser.add_argument("-c", "--caseroot", type=str, help="case directory")
parser.add_argument("-N", "--nodes", type=int, help="number of database nodes")
args = parser.parse_args()

DB_NODES=args.nodes
db_port=6379
#case_dir = args.caseroot
case_dir = '.'

os.chdir(case_dir)

if os.path.exists('{}/db_debug.log'.format(case_dir)):
    os.system('rm {}/db_debug.log'.format(case_dir))
log_to_file('{}/db_debug.log'.format(case_dir))
logger = get_logger('db_launcher')

if DB_NODES > 0:
    exp = Experiment("db", launcher="slurm")
    db = Orchestrator(launcher="slurm",
                      port=db_port,
                      db_nodes=DB_NODES, 
                      account="condo",
                      queue="acme-small",
                      batch=True, # launching as a seperate batch workload
                      time="00:30:00",
                      interface="ib0", # high speed network to use (usually ipogif0 for aries CrayXC 50)
                     )
    exp.start(db)
    os.environ['SSDB'] = f"{db.hosts[0]}:{db_port}"
    logger.debug('SSDB={}'.format(os.environ.get('SSDB')))
#exp.stop(db)
