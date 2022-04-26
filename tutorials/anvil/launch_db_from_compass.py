import shutil, time, sys, os, subprocess, fileinput

mach='anvil'
#test_case='default'
test_case='performance_test'
DB_NODES=1
SMARTDIR = '{}/tutorials/{}'.format(os.environ.get('SMARTSIM_PATH'),mach)

db_cmd = f'python {SMARTDIR}/launch_db_for_e3sm_new_alloc.py -N {DB_NODES}'
conda_cmd = 'conda run -n SmartE3SM {db_cmd}'
subprocess.check_output(conda_cmd, stderr=subprocess.STDOUT, shell=True)

with open('db_debug.log') as f:
    lines = f.readlines()
    for line in lines:
       if 'SSDB' in line:
           SSDB = line.split('=')[1]

with fileinput.FileInput(f'{test_case}.cfg', inplace=True,
               backup='.bak') as f:
    for line in f:
        print(line.replace('SSDB = None', f'SSDB = {SSDB}'), end='')
