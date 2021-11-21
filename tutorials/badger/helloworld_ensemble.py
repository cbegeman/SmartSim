from smartsim import Experiment
from smartsim.settings import SrunSettings, SbatchSettings

exp = Experiment("hello_world_batch", launcher="slurm")

# define resources for all ensemble members
sbatch = SbatchSettings(nodes=4, time="00:10:00")
#sbatch.set_partition("premium")

# define how each member should run
srun = SrunSettings(exe="echo", exe_args="Hello World!")
srun.set_nodes(1)
srun.set_tasks(32)

ensemble = exp.create_ensemble("hello_world", batch_settings=sbatch,
                               run_settings=srun, replicas=4)
exp.start(ensemble, block=True, summary=True)

print(exp.get_status(ensemble))
