
# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

from .__version__ import (
    __author__,
    __author_email__,
    __build__,
    __copyright__,
    __description__,
    __hello__,
    __license__,
    __title__,
    __url__,
    __version__,
)

# logging formatting
# log_message_format = "[%(asctime)s.%(msecs)03d][%(levelname)8s][%(module)s] %(message)s"
# log_message_format = "%(module)s: %(message)s"
log_message_format = "%s: %%(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"

logging.getLogger(__name__).addHandler(NullHandler())


# colorizing terminal output
import colorama

colorama.init()
