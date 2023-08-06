from weeve_modules import send, weeve_logger
from bottle import run, post, request
from json import dumps
from os import path, remove, getenv
from signal import signal, SIGTERM

log = weeve_logger("input_module")

output_file = "/app/artifacts/input_module_report.json"


@post("/")
def request_handler():
    try:
        received_data = request.json
        log.info("Received data: %s", received_data)

        # send data to the next module
        err = send(received_data)
        if err:
            log.error("Error while sending the data to the next module: %s", err)

        # save data and response to json file
        with open(output_file, "x") as outfile:
            log.info("Saving results to output file: %s", output_file)

            output_data = {"received_data": received_data, "err_msg": err}

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

    log.info(
        "%s running with end-point set to %s",
        getenv("MODULE_NAME"),
        getenv("EGRESS_URLS"),
    )

    # start the server
    run(host="0.0.0.0", port=8080, quiet=True)
