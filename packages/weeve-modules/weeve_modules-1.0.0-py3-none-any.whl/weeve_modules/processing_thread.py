"""
This file sets up multithread processing of data and weeve intercontainer communication.
"""

from queue import Queue
from threading import Thread, Event
from weeve_modules.logger import weeve_logger
from weeve_modules.listener_callback_function import get_listener_callback_function

# set up logging
log = weeve_logger("weeve_modules.processing_thread")


class ProcessingThread(Thread):
    """
    Thread subclass for processing data received by the module.
    """

    def __init__(self, data_queue: Queue):
        super(ProcessingThread, self).__init__()
        self.data_queue = data_queue
        self.msg_received = Event()

    def run(self) -> None:
        """
        Runs the processing thread.
        """

        while self.msg_received.wait(timeout=None):
            while not self.data_queue.empty():
                # pass data to the module logic defined by the module developer
                log.debug("Passing data to user defined module logic function...")
                next_payload = self.data_queue.get()
                try:
                    get_listener_callback_function()(next_payload)

                except Exception as e:
                    log.error(f"Error while processing the data. {e}")
                    # break this loop that queues data as if exception happens then queue is never empty and we get infinite loop
                    break

            self.msg_received.clear()

    def resume(self) -> None:
        """
        Resumes processing thread if stopped.
        """
        self.msg_received.set()
