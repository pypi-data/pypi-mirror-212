"""
Enforce a graceful termination of the module's container. We strongly recommend calling this function at the start of your module.
"""

from sys import exit
from signal import signal, SIGTERM
from weeve_modules.logger import weeve_logger

# set up logging
log = weeve_logger("weeve_modules.add_graceful_termination")


def gracefully_terminate(*args):
    """
    Gracefully terminate the module script.
    """
    log.debug("Gracefully terminating the module...")
    del args
    exit(0)


def add_graceful_termination():
    """
    Add a flag for a graceful termination of the module.
    """
    # Docker by default sends a SIGTERM to a container and waits 10 seconds for it to stop before killing it with a SIGKILL
    signal(SIGTERM, gracefully_terminate)
