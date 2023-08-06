import logging
import time
from datetime import timedelta

import pytest
from sagemaker.pytorch import PyTorch


@pytest.mark.manual
def test_grace_period_after_training_completed_or_failed():
    logging.info("Starting training with remote debugging enabled")

    estimator = PyTorch(entry_point='train.py',
                        source_dir='source_dir/training/',
                        framework_version='1.9.1',
                        py_version='py38',
                        instance_count=1,
                        instance_type='ml.m5.xlarge',
                        max_run=int(timedelta(minutes=15).total_seconds()),
                        keep_alive_period_in_seconds=1800)

    remote_debugger = estimator.enable_remote_debugger()

    remote_debugger.set_grace_period_after_success_or_failure(timedelta(minutes=2))
    # Grace period = wait after completed or failed job, max 1 hour, to avoid overcharges
    # Default is 0 (don't wait)
    # Can be prolonged (see below), but total run time is still limited to max_run

    estimator.fit(wait=False)

    remote_debugger.wait_until_ready(timeout=timedelta(seconds=300))

    # Debug while training is in progress
    status = estimator.latest_training_job.describe()['TrainingJobStatus']
    assert status == 'InProgress'

    remote_debugger.run_command("python --version")
    time.sleep(60)

    remote_debugger.wait_until_grace_period_starts(timeout=timedelta(seconds=300))

    # Debug when training is completed or failed
    status = estimator.latest_training_job.describe()['TrainingJobStatus']
    assert status == 'Completed' or 'Failed'

    # The loop will prolong remote debugging session up to ~15 min in 2 min increments (as an example).
    # Prolongation is needed to avoid overcharges after failed or completed job,
    # e.g., when the person forgets about debugging (gets asleep) and leaves the console.
    # It's effectively an implementation of a "dead man's switch".
    for i in range(1, 15):
        # Do some debugging
        remote_debugger.run_command("python --version")
        time.sleep(60)
        # You can exit the loop if finished debugging, otherwise prolong the grace period.
        # Max 1 hour, same as with initial value
        remote_debugger.prolong_grace_period(new_period_from_now=timedelta(minutes=2))  # Post-GA

    # Wait when the last grace period finishes
    estimator.latest_training_job.wait()
    # or, don't wait and stop the job
    # estimator.latest_training_job.stop()

    logging.info("Finished training and remote debugging")


@pytest.mark.manual
def test_debug_without_training():
    logging.info("Starting training with remote debugging enabled")

    estimator = PyTorch(entry_point='train.py',
                        source_dir='source_dir/training/',
                        framework_version='1.9.1',
                        py_version='py38',
                        instance_count=1,
                        instance_type='ml.m5.xlarge',
                        max_run=int(timedelta(minutes=15).total_seconds()),
                        keep_alive_period_in_seconds=1800)

    remote_debugger = estimator.enable_remote_debugger()

    remote_debugger.skip_train_command()
    # skip_train_command - Mutually exclusive with set_grace_period_after_*()
    # Requires max_run parameter to be set

    estimator.fit(wait=False)

    remote_debugger.wait_until_ready(timeout=timedelta(seconds=300))

    for i in range(1, 15):
        # Do some debugging
        remote_debugger.run_command("python --version")
        time.sleep(60)

    # Finish debugging by stopping the job
    estimator.latest_training_job.stop()
    # or, wait until max_run time:
    # estimator.latest_training_job.wait()

    logging.info("Finished training and remote debugging")


@pytest.mark.manual
def test_debug_of_a_running_job():
    logging.info("Starting training with remote debugging enabled")

    estimator = PyTorch(entry_point='train.py',
                        source_dir='source_dir/training/',
                        framework_version='1.9.1',
                        py_version='py38',
                        instance_count=1,
                        instance_type='ml.m5.xlarge',
                        max_run=int(timedelta(minutes=15).total_seconds()),
                        keep_alive_period_in_seconds=1800)

    estimator.fit(wait=False)

    remote_debugger = estimator.enable_remote_debugger()
    # Can also be called after fit()

    remote_debugger.set_grace_period_after_success_or_failure(timedelta(minutes=2))
    # Can only set grace period after fit()
    # Cannot run 'skip_train_command' because training has already started

    remote_debugger.wait_remote_debug_is_ready(timeout_in_sec=300)

    # Do some debugging
    remote_debugger.run_command("python --version")
    time.sleep(60)

    estimator.latest_training_job.stop()

    logging.info("Finished training and remote debugging")
