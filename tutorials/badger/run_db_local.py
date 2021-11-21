# run_db_local.py
from smartsim import Experiment
from smartsim.database import Orchestrator

exp = Experiment("local-db", launcher="local")
db = Orchestrator(port=6780)

# by default, SmartSim never blocks execution after the database is launched.
exp.start(db)

# launch models, anaylsis, training, inference sessions, etc
# that communicate with the database using the SmartRedis clients

# stop the database
exp.stop(db)
