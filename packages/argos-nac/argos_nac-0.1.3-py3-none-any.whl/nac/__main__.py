import logging
from .main import run

console_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s]: %(message)s")
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

# Ensure logger logs to console
logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler],
    force=False,
    format="%(asctime)s (%(name)s) [%(levelname)s]: %(message)s",
)
