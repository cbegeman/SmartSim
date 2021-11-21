from smartsim import Experiment
from smartsim.settings import RunSettings
import os

case_dir = '/lustre/scratch3/turquoise/cbegeman/E3SM-Output/20211108_WCYCL1850NS_ne4_oQU480_master/'
os.chdir(case_dir)

exp = Experiment("e3sm-test", launcher="local")
settings = RunSettings(exe="case.submit")
model = exp.create_model("e3sm", settings)
exp.start(model, block=True)
print(exp.get_status(model))
