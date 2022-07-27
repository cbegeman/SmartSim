from smartsim import Experiment

MPASO_DIR="/global/homes/c/cbegeman/MPAS-Ocean-test-case-output/smartsim/ocean/baroclinic_channel/10km/default/forward/"

exp = Experiment("mpas-ocean_simulation", launcher="slurm")
# define how simulation should be executed
settings = exp.create_run_settings(f"{MPASO_DIR}/ocean_model", 
                                   exe_args=["-n namelist.ocean",
                                             "-s streams.ocean"])
settings.set_nodes(1)
model = exp.create_model("mpas-ocean", settings)
# by default, SmartSim never blocks execution after the database is launched.
exp.start(model, block=True, summary=True)

# launch models, anaylsis, training, inference sessions, etc
# that communicate with the database using the SmartRedis clients
print(exp.get_status(model))
