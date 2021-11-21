from smartsim import Experiment
from smartsim import slurm
from smartsim.settings import SrunSettings
import os

case_dir = '/lustre/scratch3/turquoise/cbegeman/E3SM-Output/20211108_WCYCL1850NS_ne4_oQU480_master/'
os.chdir(case_dir)

alloc = slurm.get_allocation(nodes=1,
                             time="10:00:00",
                             account="e3sm",
                             #options={"exclusive": None, # totally optional constraints
                             #         "constraint": "P100"}
                            )

exp = Experiment("e3sm-test", launcher="slurm")
srun = SrunSettings(exe="case.submit", alloc=alloc)
srun.set_nodes(1)

model = exp.create_model("e3sm", srun)

exp.start(model, block=True, summary=True)
print(exp.get_status(model))
