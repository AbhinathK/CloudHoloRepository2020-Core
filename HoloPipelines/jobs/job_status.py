import logging
from datetime import datetime
from enum import Enum
from multiprocessing import Manager

# Use a python manager dict to share across processes. Note that this is a bit of a
# misuse, as typically the reference to the variable would be explicitly handed to all
# processes. But this works, and it's not critical; also this way is much more readable.
jobs_status = Manager().dict()

JobStage = Enum(
    "JobStage",
    (
        "QUEUED",
        "STARTED",
        "FETCHING_INPUT",
        "READING_INPUT",
        "PREPROCESSING",
        "PERFORMING_SEGMENTATION",
        "POSTPROCESSING",
        "DISPATCHING_OUTPUT",
        "FINISHED",
    ),
)


def update_status(job_id: str, new_stage: str, logger=logging):
    """
    Updates the global dictionary that keeps track of all jobs. Note that new_stage
    must be a string, not an Enum, as the latter leads to problems with multiprocessing.
    :param job_id: ID of the job to update
    :param new_stage: new stage (preferably use the "name" of a JobStage Enum constant)
    :param logger: optional override to the default logger (use to write to file log)
    """
    if job_id in jobs_status:
        prev_stage = jobs_status[job_id]["stage"]
        prev_timestamp = jobs_status[job_id]["timestamp"]
        time_diff = (datetime.now() - prev_timestamp).total_seconds()
        logger.info(f"[{job_id}] Finished stage {prev_stage} in {time_diff} seconds")

    new_status_for_job = {"stage": new_stage, "timestamp": datetime.now()}
    logger.info(f"[{job_id}] Entering next stage => {new_stage}")
    jobs_status[job_id] = new_status_for_job
