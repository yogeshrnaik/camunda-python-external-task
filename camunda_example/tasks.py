# Example
# Worker for "Camunda for Non-Java Developers"
import asyncio
import logging
import time
from datetime import datetime

from camunda.external_task.external_task import ExternalTask
from camunda.external_task.external_task_worker import ExternalTaskWorker

logger = logging.getLogger(__name__)


def random_true():
    current_milli_time = lambda: int(round(time.time() * 1000))
    return current_milli_time() % 2 == 0


async def get_iovation_data(task: ExternalTask):
    # put the business logic here
    logger.info(f"get_iovation_data: {task}")
    failure = random_true()
    if failure:
        return task.failure("iovation task failed", "failed iovation task details", 3, 5000)

    return task.complete({"success": True, "iovation_task_completed_on": str(datetime.now())})


async def get_sentilink_data(task: ExternalTask):
    # put the business logic here
    logger.info(f"get_sentilink_data: {task}")
    is_bpmn_error = random_true()

    if is_bpmn_error:
        return task.bpmn_error("SentlinkDetectedFraud")

    return task.complete({"success": True, "sentilink_task_completed_on": str(datetime.now())})


custom_config = {"maxTasks": 1, "pollingInterval": 2000, "asyncResponseTimeout": 5000}


def configure_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.StreamHandler()])


async def main():
    configure_logging()
    loop = asyncio.get_event_loop()

    iovation_topic = loop.create_task(ExternalTaskWorker(config=custom_config)
                                      .subscribe(["GET_IOVATION_DATA"], get_iovation_data))

    sentilink_topic = loop.create_task(ExternalTaskWorker(config=custom_config)
                                       .subscribe(["GET_SENTILINK_DATA"], get_sentilink_data))

    await asyncio.gather(iovation_topic, sentilink_topic)


if __name__ == '__main__':
    asyncio.run(main())
