from smartsim import Experiment
from smartsim.settings import RunSettings

exp = Experiment("simple", launcher="local")

settings = RunSettings("echo", exe_args="Hello World")
model = exp.create_model("hello_world", settings)

exp.start(model, block=True)
print(exp.get_status(model))
