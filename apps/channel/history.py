import logging
import json

import ccxt

from apps.channel.aws import aws_client

logger = logging.getLogger(__name__)
#logging.getLogger("ccxt.base.exchange").setLevel(logging.INFO)

# timestamp
# open
# high
# low
# close
# volume
# origin
# exchange
def history_record(timestamp, close, volume, open=None, high=None, low=None, origin=None):
    "timestamp must be datetime object"
    record = {
    #    'timestamp': timestamp.isoformat(), # timestamp datetime object
        'timestamp': timestamp,
        'close': close,
        'volume': volume,
    }
    if open is not None:
        record['open'] = open
    if high is not None:
        record['high'] = high
    if low is not None:
        record['low'] = low
    if origin is not None:
        record['origin'] = origin

    return record
    

class History:
    def __init__(self, stream_name='itf-data-stage-historical', origin='da'):
        self.firehose_client = aws_client('firehose')
        self.origin = origin
        self.stream_name = stream_name
        self.data = []

    def add(self, record):
        self.data.append(record)
    
    # def send_batch(self):
    #     for record in records:





# class Tickers:

#     def __init__(self, exchange, usdt_rates=None, minimum_volume_in_usd=None):
#         self.exchange = exchange
#         self.minimum_volume_in_usd = minimum_volume_in_usd
#         self.usdt_rates = usdt_rates

#         self.tickers = None
#         self.symbols_info = None
    
#     def run(self):
#         if self.tickers is None:
#             self._fetch_from_exchange()
#         self._process_tickers_to_standart_format()

#     def tickers_has_symbol(self, symbol):
#         try:
#             return symbol in self.tickers.keys()
#         except:
#             return False

#     def symbols_info_has_symbol(self, symbol, category='price'):
#         try:
#             return bool([item for item in self.symbols_info if item['symbol'] == symbol and item['category'] == category])
#         except:
#             return False

#     def _fetch_from_exchange(self):
#         ccxt_exchange = getattr(ccxt, self.exchange)()
#         self.tickers = ccxt_exchange.fetch_tickers()
#         return self.tickers

#     def _process_tickers_to_standart_format(self):
#         # * Standart Format
#         # symbols_info = [
#         #     {   'source': 'poloniex',
#         #         'category': 'price', # or 'volume'
#         #         'symbol': 'BTC/USDT' # LTC/BTC
#         #         'value': 12345678,
#         #         'timestamp': 1522066118.23
#         #     }, ...
#         # ]
#         symbols_info = list()

#         logger.info(f'Processing currencies for {self.exchange}')
#         count_added = 0

#         for symbol, symbol_info in self.tickers.items(): # symbol: DASH/BTC, BCH/USDT, REP/BTC
#             #logger.debug(f'{symbol}')
#             try:
#                 (transaction_currency, counter_currency) = symbol.split('/') # check format
#             except ValueError:
#                 logger.debug(f'Skipping symbol: {symbol}')
#                 continue # skip malformed currency pairs


#             # FIXME add filtering by volume symbol_allowed()
#             #if counter_currency in ('BTC', 'USDT', 'ETH'): # and enough_volume(symbol_info): # filtering
#             if self._symbol_allowed(symbol_info=symbol_info, usdt_rates=self.usdt_rates, minimum_volume_in_usd=self.minimum_volume_in_usd):
#                 # For debug
#                 # if transaction_currency in ('BTC', 'ETH', 'DASH'):
#                 #     logger.debug(f'+Adding {symbol} (testing coins from this list: BTC,ETH,DASH)\nInfo: {symbol_info}')
#                 # For debug end

#                 count_added += 1
#                 if 'last' in symbol_info: # last_price
#                     symbols_info.append(standard_format_item(
#                         source=self.exchange, category='price',
#                         value=symbol_info['last'],
#                         symbol_info=symbol_info))
#                 if 'quoteVolume' in symbol_info: # quote_volume, mean volume in counter_currrency
#                     symbols_info.append(standard_format_item(
#                         source=self.exchange, category='volume',
#                         value=symbol_info['quoteVolume'],
#                         symbol_info=symbol_info))
#             else:
#                 logger.debug(f'>> Filtered from {self.exchange}: {symbol}')

#         #logger.debug(f'Symbols info: {symbols_info}')
#         logger.info(f'>>> Processed {self.exchange}: added {count_added} coins from {len(self.tickers)}')
#         self.symbols_info = symbols_info
#         return self.symbols_info

#     @classmethod
#     def _symbol_allowed(cls, symbol_info, usdt_rates=None, minimum_volume_in_usd=None):
#         (transaction_currency, counter_currency) = symbol_info['symbol'].split('/')

#         if counter_currency not in ('BTC', 'USDT', 'ETH'):
#             return False
#         elif len(transaction_currency) >= 6: # Filter out Bitmark from Poloniex
#             return False
#         elif None in (minimum_volume_in_usd, usdt_rates):
#             return True

#         quote_volume_in_usdt = symbol_info['quoteVolume']*usdt_rates[counter_currency]
#         #print(f">>>>{symbol_info['symbol']} : qV {symbol_info['quoteVolume']}, USD {quote_volume_in_usdt}")
#         if quote_volume_in_usdt <= minimum_volume_in_usd:
#             return False
#         return True


# ## Helpers
# def get_usdt_rates_for(*coins):
#     """
#     Get usdt price from coinmarket for coins: BTC, USDT, ETH 
#     Return {'BTC': 6864.22, 'ETH': 416.851, 'USDT': 1}
#     """
#     usdt_rates = {'USDT': 1.0}

#     ccap = ccxt.coinmarketcap()
#     ccap.load_markets()
#     for coin in coins:
#         if coin != 'USDT':
#             usdt_rates[coin] = float(ccap.market(f'{coin}/USD')['info']['price_usd']) #ccap.fetch_ticker(f'{coin}/USD')['close']
#     return usdt_rates

# def standard_format_item(source, category, value, symbol_info):
#     return {
#         'source': source,
#         'category': category, # 'price' or 'volume'
#         'symbol': symbol_info['symbol'],
#         'value': float(value),
#         'timestamp': symbol_info['timestamp']/1000 # timestamp in miliseconds
#     }