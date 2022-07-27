from smartsim import Experiment
import time
import os

db_port=6379
exp = Experiment("batch-db-on-slurm", launcher="slurm")
db_cluster = exp.create_database(db_nodes=1,
                                 db_port=db_port,
                                 batch=True,
                                 interface="lo",
                                 time="00:30:00",
                                 account="e3sm",
                                 partition="debug",
                                 batch_args={"C":"haswell"})

exp.start(db_cluster)

print(f"Orchestrator launched on nodes: {db_cluster.hosts}")
# launch models, analysis, training, inference sessions, etc
# that communicate with the database using the SmartRedis clients
os.environ['SSDB'] = f"{db_cluster.hosts[0]}:{db_port}"
print(os.environ.get('SSDB'))
time.sleep(3600)
#exp.stop(db_cluster)
#SUCCESS
