import logging

from db.storage import Storage
from schemas.positions import mapping
from services.exchange import Exchange

logger = logging.getLogger(__name__)


class NotifyHandler:

    def __init__(self, currency, operation, session):
        self.currency = currency
        self.operation = operation
        self.storage = Storage(session)
        self.exchange = Exchange()
        self.exchange.connect()

    async def handle(self):
        logging.info('Начало обработки операции {} для пары {}'.format(self.operation, self.currency))
        await self.storage.add_history(self.currency, self.operation)
        try:
            if self.operation in ('1L', '2L', '3L'):
                res = await self.storage.check_operation(self.currency)
                if not res and self.operation == '1L':
                    await self.storage.add_operation(currency=self.currency,
                                                     operation=self.operation,
                                                     buy=mapping[self.currency]['Buy'],
                                                     initial_sell=mapping[self.currency]['Sell'],
                                                     sell=mapping[self.currency]['Sell'],
                                                     amount=mapping[self.currency]['Buy'])
                    self.exchange.buy(self.currency, mapping[self.currency]['Buy'])
                elif res and res.operation != self.operation:
                    amount = float(res.amount) + float(res.buy)
                    sell = float(res.sell) + float(res.initial_sell)
                    await self.storage.add_operation(currency=self.currency,
                                                     operation=self.operation,
                                                     buy=res.buy,
                                                     initial_sell=res.initial_sell,
                                                     sell=str(sell),
                                                     amount=str(amount))
                    self.exchange.buy(self.currency, res.buy)
            elif self.operation in ('LTP1', 'LTP2', 'LTP3', 'LTP4'):
                res = await self.storage.check_operation(self.currency)
                if not res:
                    size = self.exchange.get_position_size(self.currency)
                    if size:
                        if float(size) > float(mapping[self.currency]['Sell']):
                            amount = float(size) - float(mapping[self.currency]['Sell'])
                            await self.storage.add_operation(currency=self.currency,
                                                             operation=self.operation,
                                                             buy=size,
                                                             initial_sell=mapping[self.currency]['Sell'],
                                                             sell=mapping[self.currency]['Sell'],
                                                             amount=str(amount))
                elif res and res.operation != self.operation and self.operation:
                    amount = float(res.amount) - float(res.sell)
                    await self.storage.add_operation(currency=self.currency,
                                                     operation=self.operation,
                                                     buy=res.buy,
                                                     initial_sell=res.initial_sell,
                                                     sell=res.sell,
                                                     amount=str(amount))
                    self.exchange.sell(self.currency, res.sell)
            elif self.operation in ('LSL', 'LTP5'):
                size = self.exchange.get_position_size(self.currency)
                if size:
                    self.exchange.sell(self.currency, size)
                await self.storage.delete_operation(self.currency)
            elif self.operation in ('1S', '2S', '3S'):
                res = await self.storage.check_operation(self.currency)
                if not res and self.operation == '1S':
                    await self.storage.add_operation(currency=self.currency,
                                                     operation=self.operation,
                                                     buy=mapping[self.currency]['Buy'],
                                                     initial_sell=mapping[self.currency]['Sell'],
                                                     sell=mapping[self.currency]['Sell'],
                                                     amount=mapping[self.currency]['Buy'])
                    self.exchange.sell(self.currency, mapping[self.currency]['Buy'])
                elif res and res.operation != self.operation:
                    amount = float(res.amount) + float(res.buy)
                    sell = float(res.sell) + float(res.initial_sell)
                    await self.storage.add_operation(currency=self.currency,
                                                     operation=self.operation,
                                                     buy=res.buy,
                                                     initial_sell=res.initial_sell,
                                                     sell=str(sell),
                                                     amount=str(amount))
                    self.exchange.sell(self.currency, res.buy)
            elif self.operation in ('STP1', 'STP2', 'STP3', 'STP4'):
                res = await self.storage.check_operation(self.currency)
                if not res:
                    size = self.exchange.get_position_size(self.currency)
                    if size:
                        if float(size) > float(mapping[self.currency]['Sell']):
                            amount = float(size) - float(mapping[self.currency]['Sell'])
                            await self.storage.add_operation(currency=self.currency,
                                                             operation=self.operation,
                                                             buy=size,
                                                             initial_sell=mapping[self.currency]['Sell'],
                                                             sell=mapping[self.currency]['Sell'],
                                                             amount=str(amount))
                elif res and res.operation != self.operation and self.operation:
                    amount = float(res.amount) - float(res.sell)
                    await self.storage.add_operation(currency=self.currency,
                                                     operation=self.operation,
                                                     buy=res.buy,
                                                     initial_sell=res.initial_sell,
                                                     sell=res.sell,
                                                     amount=str(amount))
                    self.exchange.buy(self.currency, res.sell)
            elif self.operation in ('SSL', 'STP5'):
                size = self.exchange.get_position_size(self.currency)
                if size:
                    self.exchange.buy(self.currency, size)
        except Exception as e:
            logging.error('Ошибка обработки операции {} для пары {}:'.format(self.operation, self.currency))
            logging.error('{}\n{}'.format(type(e), e))
            raise e
