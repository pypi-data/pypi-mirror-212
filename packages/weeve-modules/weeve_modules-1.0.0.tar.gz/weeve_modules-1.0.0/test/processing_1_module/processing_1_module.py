from weeve_modules import listener, send, weeve_logger
from json import dumps
from os import path, remove
from signal import signal, SIGTERM

log = weeve_logger("processing_1_module")

output_file = "/app/artifacts/processing_1_module_report.json"


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def main_module_logic(received_data):
    try:
        log.info(f"Received data: {received_data}")

        processed_data = received_data.copy()

        # add some data
        processed_data["temp_fahrenheit"] = celsius_to_fahrenheit(
            received_data["temperature"]
        )
        processed_data["weather"] = "sunny"

        # send data to the next module
        err = send(processed_data)
        if err:
            log.error("Error while sending the data to the next module: %s", err)

        # save data and response to json file
        with open(output_file, "w") as outfile:
            log.info("Saving results to output file: %s", output_file)

            output_data = {
                "received_data": received_data,
                "processed_data": processed_data,
                "err_msg": err,
            }

            outfile.write(dumps(output_data))

    except Exception as e:
        log.error(f"Exception in module main logic data: {e}")


def teardown_and_exit(*args):
    del args
    if path.exists(output_file):
        remove(output_file)
    exit(0)


if __name__ == "__main__":
    signal(SIGTERM, teardown_and_exit)

    listener(callback_function=main_module_logic)
