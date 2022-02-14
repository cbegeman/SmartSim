
def waitForAlloc():
    timeLimit = 60
    tic = time.perf_counter()
    JOBID = "None"
    while toc-tic < timeLimit and JOBID == "None":
        if os.exists('{}/jobid.sh'.format(case_dir)):
            os.system('source {}/jobid.sh'.format(case_dir))
            JOBID = os.environ.get("E3SM_JOBID","None")
            if JOBID != "None":
                return JOBID
        else:
            time.sleep(60)
            toc = time.perf_counter()
    print('time limit was reached')
