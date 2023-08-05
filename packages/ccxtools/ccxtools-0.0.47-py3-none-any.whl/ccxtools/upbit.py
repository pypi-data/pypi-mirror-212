import ccxt
from ccxtools.exchange import CcxtExchange


class Upbit(CcxtExchange):

    def __init__(self, who, market, config):
        super().__init__(market)
        self.ccxt_inst = ccxt.upbit({
            'apiKey': config(f'UPBIT_API_KEY{who}'),
            'secret': config(f'UPBIT_SECRET_KEY{who}')
        })

    def get_mark_price(self, ticker):
        raise NotImplementedError

    def get_contract_sizes(self):
        raise NotImplementedError

    def post_market_order(self, ticker, side, open_close, amount):
        raise NotImplementedError

    def get_max_position_qtys(self):
        raise NotImplementedError
