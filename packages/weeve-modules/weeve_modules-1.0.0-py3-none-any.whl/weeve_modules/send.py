"""
This file implements output aspect of the module's intercontainer communication.
It sends data over REST API POST method to the next module in the edge application.
"""

from os import getenv
from requests import exceptions, post
from weeve_modules.logger import weeve_logger

log = weeve_logger("weeve_modules.send")


def send(processed_data: dict) -> str:
    """
    Send processed data to the next module in weeve Edge Application.

    Args:
        processed_data (dict): processed data in JSON format to send to the next module.

    Returns:
        string: Empty string ("" / None) on success. Otherwise, error message.
    """

    try:
        # parse egress urls for fanout
        urls = [
            url.strip() for url in getenv("EGRESS_URLS").strip(",").split(",")
        ]

        # for collecting REST API POST responses
        failed_responses = []

        # fan-out
        for url in urls:
            # send data to the next module
            response = post(url=url, json=processed_data)

            if response.status_code != 200:
                # on sending error
                log.debug(
                    f"Failed sending data to {url} | Response: {response.status_code} {response.reason}"
                )

                failed_responses.append(
                    {
                        "url": url,
                        "status_code": response.status_code,
                        "message": response.text,
                    }
                )
            else:
                # on sending success
                log.debug(
                    f"Successfully sent data to url {url} | Response: {response.status_code} {response.reason}"
                )

        if failed_responses:
            # info on failed responses
            error_msg = "Failed sending data to the following urls: "
            for resp in failed_responses:
                error_msg = (
                    error_msg
                    + f"{resp['url']} - {resp['status_code']}: {resp['message']}. "
                )

            return error_msg

        return ""

    except (
        exceptions.RequestException,
        exceptions.ConnectionError,
        exceptions.ConnectTimeout,
    ) as e:
        return f"Exception when sending data to the next module: {e}"
