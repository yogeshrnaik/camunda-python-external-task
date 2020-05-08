# Example
# Worker for "Camunda for Non-Java Developers"
import threading
import time

from camunda.worker import Worker


def random_success():
    current_milli_time = lambda: int(round(time.time() * 1000))
    return current_milli_time() % 2 == 0


async def get_iovation_data(context):
    # put the business logic here
    print(f"get_iovation_data: {context}")
    success = random_success()
    return {"success": False, "iokey1": "value1", "iokey2": 2}


async def get_sentilink_data(context):
    # put the business logic here
    print(f"get_sentilink_data: {context}")
    success = random_success()
    result = {"bpmn_success": success, "skey1": "value1", "skey2": 2}
    if not success:
        result["errorCode"] = "SentlinkDetectedFraud"
        result["errorMessage"] = "Sentlink Fraud detected"
    return result


customOptions = {"maxTasks": 1, "pollingInterval": 2000, "asyncResponseTimeout": 5000}


def get_iovation_data_task():
    w = Worker(options=customOptions)
    w.subscribe("GET_IOVATION_DATA", [], get_iovation_data)


def get_sentilink_data_task():
    w = Worker(options=customOptions)
    w.subscribe("GET_SENTILINK_DATA", [], get_sentilink_data)


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
