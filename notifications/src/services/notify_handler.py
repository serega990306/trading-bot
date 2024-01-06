from db.storage import Storage


class NotifyHandler:

    def __init__(self, currency, operation, session):
        self.currency = currency
        self.operation = operation
        self.storage = Storage(session)

    def handle(self):
        if self.operation in ('1L', '2L', '3L'):
            res = self.storage.check_operation(self.currency)
            if res != self.operation:
                self.storage.add_operation(self.currency, self.operation)
                # TODO add on bybit
        elif self.operation in ('LTP1', 'LTP2', 'LTP3', 'LTP4', 'LTP5'):
            pass
        elif self.operation == 'LSL':
            pass
        elif self.operation in ('1S', '2S', '3S'):
            pass
        elif self.operation in ('STP1', 'STP2', 'STP3', 'STP4', 'STP5'):
            pass
        elif self.operation == 'SSL':
            pass
