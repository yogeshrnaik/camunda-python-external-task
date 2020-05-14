# Example
# Worker for "Camunda for Non-Java Developers"
import logging
import threading
import time

from camunda.external_task.external_task_worker import ExternalTaskWorker

logger = logging.getLogger(__name__)


def random_true():
    current_milli_time = lambda: int(round(time.time() * 1000))
    return current_milli_time() % 2 == 0


async def get_iovation_data(context):
    # put the business logic here
    logger.info(f"get_iovation_data: {context}")
    is_error = random_true()
    return {"error": is_error, "iokey1": "value1", "iokey2": 2}


async def get_sentilink_data(context):
    # put the business logic here
    logger.info(f"get_sentilink_data: {context}")
    is_bpmn_error = random_true()
    result = {"bpmn_error": is_bpmn_error, "skey1": "value1", "skey2": 2}
    if is_bpmn_error:
        result["errorCode"] = "SentlinkDetectedFraud"
        result["errorMessage"] = "Sentlink Fraud detected"
    return result


custom_options = {"maxTasks": 1, "pollingInterval": 2000, "asyncResponseTimeout": 5000}


def get_iovation_data_task():
    w = ExternalTaskWorker(options=custom_options)
    w.subscribe("GET_IOVATION_DATA", get_iovation_data)


def get_sentilink_data_task():
    w = ExternalTaskWorker(options=custom_options)
    w.subscribe("GET_SENTILINK_DATA", get_sentilink_data)


def configure_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.StreamHandler()])


def main():
    configure_logging()
    t1 = threading.Thread(target=get_iovation_data_task, args=())
    t2 = threading.Thread(target=get_sentilink_data_task, args=())

    t1.start()
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    # both threads completely executed
    print("Done!")


if __name__ == '__main__':
    main()
