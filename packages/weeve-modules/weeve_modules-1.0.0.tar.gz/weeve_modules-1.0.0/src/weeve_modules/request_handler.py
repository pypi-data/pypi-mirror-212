"""
This file implements input aspect of the module's intercontainer communication.
It receives data over REST API POST method and passes it for processing.
"""

from queue import Queue
from bottle import post, request, response
from weeve_modules.logger import weeve_logger
from weeve_modules.processing_thread import ProcessingThread

# set up logging
log = weeve_logger("weeve_modules.request_handler")

# declare queue storing data
data_Q = Queue()

# initialise processing thread
data_processing_thread = ProcessingThread(data_Q)
data_processing_thread.start()


@post("/")
def _request_handler():
    """
    Handles incoming data.
    """

    global data_Q
    global data_processing_thread

    try:
        # receive data from the previous module
        received_data = request.json
        log.debug("Received data: %s", received_data)

        # add data to the queue
        data_Q.put(received_data)

        try:
            # pass data to processing thread
            log.debug("Invoking the thread to process new data.")
            data_processing_thread.resume()

        except Exception as e:
            log.error(f"Failed to invoke a thread to process new data. {e}")

        # notify previous module that data has been received
        return "OK - data accepted"

    except Exception as e:
        response.status = 400
        return f"Exception occurred in the successive module while handling your POST request. {e}"
