import logging
from typing import Optional
from pybit.unified_trading import HTTP

from core.config import settings

logger = logging.getLogger(__name__)


class Exchange:
    session = None

    def connect(self):
        self.session = HTTP(
            testnet=False,
            api_key=settings.api_key,
            api_secret=settings.api_secret,
        )

    def buy(self, currency, qty):
        logger.info("Покупка актива {}".format(currency))
        logger.info(self.session.place_order(
            category="linear",
            symbol=currency,
            side="Buy",
            orderType="Market",
            qty=qty
        ))

    def sell(self, currency, qty):
        logger.info("Продажа актива {}".format(currency))
        logger.info(self.session.place_order(
            category="linear",
            symbol=currency,
            side="Sell",
            orderType="Market",
            qty=qty
        ))

    def get_position(self, currency) -> dict:
        logger.info("Получение позиции актива {}".format(currency))
        return self.session.get_positions(
            category="linear",
            symbol=currency,
        )

    def get_position_size(self, currency) -> Optional[str]:
        d = self.get_position(currency)
        if d.get('result') \
                and d['result'].get('list') \
                and len(d['result']['list']) > 0 \
                and d['result']['list'][0]['size'] not in ('', '0'):
            return d['result']['list'][0]['size']
        return None
