from smartsim import Experiment

exp = Experiment("batch-db-on-slurm", launcher="slurm")
db_cluster = exp.create_database(db_nodes=1,
                                 db_port=6780,
                                 batch=True,
                                 time="00:10:00",
                                 interface="lo",
                                 account="e3sm",
                                 partition="debug",
                                 batch_args={"C":"haswell"})

exp.start(db_cluster)

print(f"Orchestrator launched on nodes: {db_cluster.hosts}")
# launch models, analysis, training, inference sessions, etc
# that communicate with the database using the SmartRedis clients

exp.stop(db_cluster)
