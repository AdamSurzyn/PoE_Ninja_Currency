import logging
import os
import sys

def setup_logger():
    handler = logging.StreamHandler(stream=sys.stdout)
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    handler.setFormatter(logging.Formatter(fmt))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    root.setLevel(level)