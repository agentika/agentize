import os
import sys
from typing import Final

from loguru import logger

from .lazy import lazy_run
from .lazy import lazy_run_sync
from .model import get_openai_client
from .model import get_openai_model
from .model import get_openai_model_settings

LOGURU_LEVEL: Final[str] = os.getenv("LOGURU_LEVEL", "INFO")
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGURU_LEVEL}])
