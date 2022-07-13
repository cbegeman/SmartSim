from smartsim import Experiment

exp = Experiment("hello_world_exp", launcher="local")
srun_settings = exp.create_run_settings(exe="echo",
                               exe_args="Hello World!",
                               run_command="srun",
                               run_args={"account":"e3sm",
                                         "partition":"debug",
                                         "C":"haswell"
                                         })
srun_settings.set_nodes(1)
srun_settings.set_tasks(4)
srun_settings.set_walltime("00:10:00")

model = exp.create_model("hello_world", srun_settings)
exp.start(model, block=True, summary=True)

print(exp.get_status(model))

# SUCCESS
