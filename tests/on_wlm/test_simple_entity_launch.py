import pytest

from smartsim import Experiment, constants

"""
Test the launch of simple entity types on pre-existing allocations.

All entities will obtain the allocation from the environment of the
user
"""

# retrieved from pytest fixtures
if pytest.test_launcher not in pytest.wlm_options:
    pytestmark = pytest.mark.skip(reason="Not testing WLM integrations")


def test_models(fileutils, wlmutils):
    exp_name = "test-models-launch"
    exp = Experiment(exp_name, launcher=wlmutils.get_test_launcher())
    test_dir = fileutils.make_test_dir(exp_name)

    script = fileutils.get_test_conf_path("sleep.py")
    settings = wlmutils.get_run_settings("python", f"{script} --time=5")
    M1 = exp.create_model("m1", path=test_dir, run_settings=settings)
    M2 = exp.create_model("m2", path=test_dir, run_settings=settings)

    exp.start(M1, M2, block=True)
    statuses = exp.get_status(M1, M2)
    assert all([stat == constants.STATUS_COMPLETED for stat in statuses])


def test_ensemble(fileutils, wlmutils):
    exp_name = "test-ensemble-launch"
    exp = Experiment(exp_name, launcher=wlmutils.get_test_launcher())
    test_dir = fileutils.make_test_dir(exp_name)

    script = fileutils.get_test_conf_path("sleep.py")
    settings = wlmutils.get_run_settings("python", f"{script} --time=5")
    ensemble = exp.create_ensemble("e1", run_settings=settings, replicas=2)
    ensemble.set_path(test_dir)

    exp.start(ensemble, block=True)
    statuses = exp.get_status(ensemble)
    assert all([stat == constants.STATUS_COMPLETED for stat in statuses])


def test_summary(fileutils, wlmutils):
    """Fairly rudimentary test of the summary dataframe"""

    exp_name = "test-launch-summary"
    exp = Experiment(exp_name, launcher=wlmutils.get_test_launcher())
    test_dir = fileutils.make_test_dir(exp_name)

    sleep = fileutils.get_test_conf_path("sleep.py")
    bad = fileutils.get_test_conf_path("bad.py")
    sleep_settings = wlmutils.get_run_settings("python", f"{sleep} --time=3")
    bad_settings = wlmutils.get_run_settings("python", f"{bad} --time=6")

    sleep = exp.create_model("sleep", path=test_dir, run_settings=sleep_settings)
    bad = exp.create_model("bad", path=test_dir, run_settings=bad_settings)

    # start and poll
    exp.start(sleep, bad)
    assert exp.get_status(bad)[0] == constants.STATUS_FAILED
    assert exp.get_status(sleep)[0] == constants.STATUS_COMPLETED

    summary_df = exp.summary()
    print(summary_df)
    row = summary_df.loc[0]

    assert sleep.name == row["Name"]
    assert sleep.type == row["Entity-Type"]
    assert 0 == int(row["RunID"])
    assert 0 == int(row["Returncode"])

    row_1 = summary_df.loc[1]

    assert bad.name == row_1["Name"]
    assert bad.type == row_1["Entity-Type"]
    assert 0 == int(row_1["RunID"])
    assert 0 != int(row_1["Returncode"])
