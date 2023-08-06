import logging

from .ana import ANA


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.NullHandler(),
    ]
)
logger = logging.getLogger(__name__)
