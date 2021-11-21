from smartsim import Experiment
from smartsim.settings import RunSettings, SrunSettings
from smartsim import slurm
from smartsim.database import SlurmOrchestrator, Orchestrator

# get an allocation we will stuff our database and model into
alloc = slurm.get_allocation(nodes=2,
                             time="10:00:00",
                             account="mycoolaccount",
                             options={"exclusive": None, # totally optional constraints
                                      "constraint": "P100"})


exp = Experiment("E3SM", launcher="slurm")

# if you want a database launched out on compute nodes (assuming this is what you want)
db = SlurmOrchestrator(port=6379,
                       db_nodes=1, # only 1 database (not a cluster)
                       batch=False, # not launching as a seperate batch workload
                       interface="ipogif0", # high speed network to use (usually ipogif0 for aries CrayXC 50)
                       alloc=alloc # launching into this allocation
                      )
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

# this will block until db is launched and then release
exp.start(db)

# now the database is started you can preload the DB with models
# and scripts and what not
from smartredis import Client
client = Client(address=db.get_address()[0], # get address from database
                cluster=False) # database is not a cluster because it's less than 3 nodes
client.set_model...
client.set_script...
#ETC ETC


# so if you want the case submitted to the same allocation as the database
# then break up the case submission here as follows
run_settings = SrunSettings("e3sm.exe",
                            alloc=alloc)
                            run_settings.set_nodes(1)
                            run_settings.set_tasks(32)
# this is how most users use SmartSim

# OR

# if you just want the case submission (which im guessing submits a batch file) to
# run in a different allocation then run
# using RunSettings will run this command locally (aka head node)
run_settings = RunSettings("case.submit")


# create reference to the job you will run
e3sm = exp.create_model("e3sm_test", run_settings)

exp.start(e3sm,
          block=True, # block and report status until completed
          summary=True # give a quick summary of the launch before the launch
          )

exp.stop(db) # stop the database when the run is over (it doesn't stop itself on purpose)
