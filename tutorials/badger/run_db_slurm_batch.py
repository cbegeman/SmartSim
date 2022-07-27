from smartsim import Experiment
from smartsim.database import SlurmOrchestrator

exp = Experiment("db-on-slurm", launcher="slurm")
db_cluster = SlurmOrchestrator(db_nodes=3, db_port=6780, batch=True,
                               time="00:10:00",interface='ib0')

exp.start(db_cluster)

print(f"Orchestrator launched on nodes: {db_cluster.hosts}")
# launch models, anaylsis, training, inference sessions, etc
# that communicate with the database using the SmartRedis clients

exp.stop(db_cluster)
