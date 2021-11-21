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
db_port=6379

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
time.sleep(30)

#JOBID = waitForAlloc()
if os.path.exists('{}/jobid.sh'.format(case_dir)):
    with open('{}/jobid.sh'.format(case_dir),'r') as myfile:
        E3SM_JOBID=myfile.read().rstrip()
        print('JOBID={}'.format(E3SM_JOBID))
else:
    E3SM_JOBID = "None"
    print('jobid has not been written to file')

if DB_NODES > 0:
    if E3SM_JOBID == "None":
        print("JOBID not available for simulation")
        DB_NODES = 0
    else:
        db = SlurmOrchestrator(port=db_port,
                               db_nodes=DB_NODES, # only 1 database (not a cluster)
                               batch=False, # not launching as a seperate batch workload
                               interface="ib0", # high speed network to use (usually ipogif0 for aries CrayXC 50)
                               alloc=E3SM_JOBID# launching into this allocation
                              )
        print(db.hosts)
        print(db_port)
        os.system('bash -c \'echo "{}:{}" >> {}/SSDB.sh\''.format(db.hosts[0],db_port,case_dir))
        if os.path.exists('{}/SSDB.sh'.format(case_dir)):
            with open('{}/SSDB.sh'.format(case_dir),'r') as myfile:
                SSDB = myfile.read().rstrip()
        else:
            print('SSDB has not been written to file')
        print("SSDB=",SSDB)
        os.environ["SSDB"] = SSDB
        # this will block until db is launched and then release
        exp.start(db)
        print(f"Orchestrator launched on nodes: {db.hosts}")

print(exp.get_status(e3sm))

if DB_NODES > 0:
    exp.stop(db)

def waitForAlloc():
    timeLimit = 60
    tic = time.perf_counter()
    JOBID = "None"
    while toc-tic < timeLimit and JOBID == "None":
        if os.exists('{}/jobid.sh'.format(case_dir)):
            os.system('source {}/jobid.sh'.format(case_dir))
            JOBID = os.environ.get("E3SM_JOBID","None")
            if JOBID != "None":
                return JOBID
        else:
            time.sleep(60)
            toc = time.perf_counter()
    print('time limit was reached')
