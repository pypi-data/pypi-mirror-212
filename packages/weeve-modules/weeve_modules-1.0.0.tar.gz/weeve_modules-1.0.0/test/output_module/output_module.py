from weeve_modules import listener, weeve_logger
from json import dumps
from os import path, remove
from signal import signal, SIGTERM

log = weeve_logger("output_module")

output_file = "/app/artifacts/output_module_report.json"


def main_module_logic(received_data):
    try:
        log.info(f"Received data: {received_data}")

        # save data to json file
        with open(output_file, "w") as outfile:
            log.info("Saving results to output file: %s", output_file)

            output_data = {"received_data": received_data}

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
