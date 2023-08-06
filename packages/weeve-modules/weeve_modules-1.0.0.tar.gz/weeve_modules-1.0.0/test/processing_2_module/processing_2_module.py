from weeve_modules import listener, send, weeve_logger
from json import dumps
from os import path, remove
from signal import signal, SIGTERM

log = weeve_logger("processing_2_module")

output_file = "/app/artifacts/processing_2_module_report.json"


def main_module_logic(received_data):
    try:
        log.info(f"Received data: {received_data}")

        processed_data = received_data.copy()

        # add some data
        processed_data["voltage"] = 215.23
        processed_data["altitude"] = 2405
        processed_data["warnings"] = True

        # send data to the next module
        err = send(processed_data)
        if err:
            log.error("Error while sending the data to the next module: %s", err)

        if err:
            # change the error message erronous object memory location to be compatible with ground truth test as it is assigned randomly by the system
            in_string_memory_address_location = err.find("object at")
            if in_string_memory_address_location > -1:
                # remove memory address
                err = err.replace(
                    err[
                        in_string_memory_address_location
                        + 10 : err.find(">", in_string_memory_address_location + 10)
                    ],
                    "",
                )
                # remove other string artefacts
                err = err.replace("'", "")
                err = err.replace('"', "")

            # remove the error number due to the disparities in error numbering between OS i.e. macOS and Linux.
            in_string_error_number_location = err.find("Errno -")
            if in_string_error_number_location > -1:
                # remove the error number
                err = (
                    err[: in_string_error_number_location + 7]
                    + err[in_string_error_number_location + 8 :]
                )

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
