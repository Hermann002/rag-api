import logging

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Configuration du logger
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
