from smartsim import Experiment
from smartsim.settings import SrunSettings

exp = Experiment("hello_world_exp", launcher="slurm")
srun = SrunSettings(exe="echo", exe_args="Hello World!")
srun.set_nodes(1)
srun.set_tasks(32)

model = exp.create_model("hello_world", srun)
exp.start(model, block=True, summary=True)

print(exp.get_status(model))
