from services.queue_resource.queue_resource import QueueResourceInternal
from time import sleep
from log import logger


class QueueHandler:
    def _async_poll(self):
        while True:
            sleep(3)
            self._check_queue()

    def _check_queue(self):
        logger.info("Checking data from queue..")
        job = QueueResourceInternal().get()
        if not job:
            logger.info("Queue is currently empty..")
            return
        self._trigger_processing()

    def _trigger_processing(self, data):
        logger.info("Fetching data from the queue..")
        self.run_processing(data['item'])

    def run_processing(self):
        pass

if __name__ == "__main__":
    QueueHandler()._async_poll()