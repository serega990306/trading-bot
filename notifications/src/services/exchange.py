import logging
from pybit.unified_trading import HTTP

from ..core.config import settings

logger = logging.getLogger(__name__)


class Exchange:
    session = None

    def connect(self):
        self.session = HTTP(
            testnet=True,
            api_key=settings.api_key,
            api_secret=settings.api_secret,
        )