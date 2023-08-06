"""
This file stores user's callback function with implemented module's main logic.
This function is later accessed by processing thread.
"""

# variable to store user's callback function
LISTENER_CALLBACK_FUNCTION = None


def set_listener_callback_function(function: object) -> None:
    """
    Saves user's callback function with implemented module's main logic.

    Args:
        function (object): The callback function defined by a user and ready to receive data for further processing.
    """

    global LISTENER_CALLBACK_FUNCTION
    LISTENER_CALLBACK_FUNCTION = function


def get_listener_callback_function() -> object:
    """
    Returns:
        object: The callback function defined by a user where receive data is passed for further processing.
    """

    return LISTENER_CALLBACK_FUNCTION
