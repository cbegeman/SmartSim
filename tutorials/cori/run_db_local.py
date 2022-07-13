# run_db_local.py
from smartsim import Experiment
import os

db_port=6380

exp = Experiment("local-db", launcher="local")
db = exp.create_database(port=db_port, interface="lo")

# by default, SmartSim never blocks execution after the database is launched.
exp.start(db)

# launch models, anaylsis, training, inference sessions, etc
# that communicate with the database using the SmartRedis clients
os.environ['SSDB'] = f"{db.hosts[0]}:{db_port}"
print(os.environ.get('SSDB'))

# stop the database
exp.stop(db)
