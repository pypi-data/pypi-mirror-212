# weeve Modules Python Package

This Python pip package is a specially designed support package for developers to implement their own weeve modules.
The package takes care of all weeve specific intercontainer communication protocols and other aspects of the module's functionality within weeve ecosystem.

For the full documentation on building weeve modules, please see our official docs: [How to create a weeve module](https://docs.weeve.engineering/guides/how-to-create-a-weeve-module).

- [weeve Modules Python Package](#weeve-modules-python-package)
  - [Package specific environment variables](#package-specific-environment-variables)
  - [weeve\_modules.listener()](#weeve_moduleslistener)
  - [weeve\_modules.send()](#weeve_modulessend)
  - [weeve\_modules.weeve\_logger()](#weeve_modulesweeve_logger)
  - [weeve\_modules.add\_graceful\_termination()](#weeve_modulesadd_graceful_termination)
  - [Example: Input Module](#example-input-module)
  - [Example: Processing Module](#example-processing-module)
  - [Example: Output Module](#example-output-module)

## Package specific environment variables

These environment variables are set by the weeve Agent on the edge-node. In order to avoid conflicts, do not override these variables when pushing modules to production.

| Environment Variables | type   | Description                                                                                                                                                                 |
| --------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LOG_LEVEL       | string | Allowed log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Refer to [logging levels package documentation](https://docs.python.org/3/library/logging.html#levels). |
| MODULE_NAME     | string | Name of the module.                                                                                                                                                         |
| INGRESS_HOST    | string | Host to which data will be received.                                                                                                                                        |
| INGRESS_PORT    | string | Port to which data will be received.                                                                                                                                        |
| EGRESS_URLS     | string | HTTP ReST endpoint for the next modules.                                                                                                                                    |


## weeve_modules.listener()

`listener()` is the most important function as it allows the module to set up a listener server to receive data from other modules within the weeve ecosystem. `listener()` takes one argument:

* `callback_function` (`object`): The callback function defined by a user and ready to receive data for further processing. Callback function **must** accept data as an argument.

```python
from weeve_modules import listener

def my_module_logic(data):
    # your module code here

if __name__ == "__main__":
    listener(callback_function=my_module_logic)
```

## weeve_modules.send()

This function enables passing data to the next module in the weeve Edge Application. It takes only one argument:

* `processed_data` (`dict`): Data in JSON format to send to the next module.

It returns empty string ("") on success. Otherwise, error message.

```text
On error:
"Failed sending data to urls: https://testing.com - Error 404."
```

Example:

```python
from weeve_modules import send

# send data to the next module
err = send({"temperature": 12, "pressure": 1019})
if err:
    # your error protocol
```

## weeve_modules.weeve_logger()

Weeve logger is based on [logging package](https://docs.python.org/3/library/logging.html#). There are five supported logging levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Refer to [logging levels package documentation](https://docs.python.org/3/library/logging.html#levels). These messages have a custom weeve logging protocol which is in sync with weeve Agent and API. Current schema:

```text
{
    "timestamp": <timestamp>,
    "level": <logging_level>,
    "filename": <log_message_source_filename>,
    "message": <log_message>
}
```

Example:

```python
from weeve_modules import weeve_logger

# initialize logging by providing logger name, we strongly recommend using the filename
log = weeve_logger("tutorial_module")

# logging examples
log.debug("This is debug log messege.")
log.info("This is info log messege.")
log.warning("This is warning log messege.")
log.error("This is error log messege.")
log.critical("This is critical log messege.")
```

## weeve_modules.add_graceful_termination()

`add_graceful_termination()` function enables Docker to gracefully terminate the module container. This is optional as developers might want to implement their own graceful termination if their modules use extra resources or files. However, we strongly recommend calling `add_graceful_termination()` at the start of your script unless the module uses volumes, external resources, etc. when the custom implementation of graceful termination might be required.

Example:

```python
from weeve_modules import listener, add_graceful_termination

def my_module_logic(data):
    # your module code here

if __name__ == "__main__":
    add_graceful_termination()

    listener(callback_function=my_module_logic)
```

## Example: Input Module

This is an example of a simple input module that receives data over HTTP ReST and passes it to the next module in the weeve Edge Application.
We need `send()` and `weeve_logger()` functions.

```python
from weeve_modules import send, weeve_logger
from bottle import run, post, request

log = weeve_logger("my_input_module")

@post("/")
def _request_handler():
    # receive data
    received_data = request.json

    # send data to the next module
    err = send(received_data)

if __name__ == "__main__":
    add_graceful_termination()

    # start the server on http://0.0.0.0:8080/
    run(
        host="0.0.0.0",
        port=8080,
        quiet=True,
    )
```

## Example: Processing Module

This is an example of a simple processing module that receives data from the previous module and filters out `temperature` lower that 0. Later it sends data to the next module in the weeve Edge Application.
We need `send()`, `weeve_logger()` and `listener()` functions.

```python
from weeve_modules import send, weeve_logger, listener

log = weeve_logger("my_processing_module")

# my module logic functionality
def filter_temperature(data):

    # filter temperature data
    if data["temperature"] >= 0:

        # send data to the next module
        err = send(data)

        # check the success of sending the data
        if err:
            log.error("Failed to pass filetered data: %s", err)
        else:
            log.info("Successfully passed filetered data.")

if __name__ == "__main__":
    add_graceful_termination()

    # set up a listener to receive data from other modules within the weeve ecosystem
    listener(callback_function=filter_temperature)
```

## Example: Output Module

This is an example of a simple output module that receives data from the previous module and sends it over HTTP ReST to a selected endpoint.
We need `weeve_logger()` and `listener()` functions.

```python
from weeve_modules import weeve_logger, listener
from requests import post
from json import dumps

log = weeve_logger("my_output_module")

# my module logic functionality
def send_to_endpoint(data):

    log.info("Sending data to the endpoint.")
    post(url="", json=data)

if __name__ == "__main__":
    add_graceful_termination()

    # set up a listener to receive data from other modules within the weeve ecosystem
    listener(callback_function=send_to_endpoint)
```
