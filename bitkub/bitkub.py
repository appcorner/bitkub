"""
A library that provides a python interface to Bitkub API
"""
import hashlib
import hmac
import json
import time

from .constants import ENDPOINTS
from .decorators import check_in_attributes
from .request import basic_request

from datetime import datetime

class Bitkub:
    def __init__(self, api_key=None, api_secret=None, v2_compatable=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.v2_compatable = v2_compatable
        self.API_ROOT = ENDPOINTS["API_ROOT"]

    def _get_api_secret(self):
        return self.api_secret.encode()

    def _get_path(self, path_name, **kwargs):
        """
        Get full endpoint for a specific path.
        """
        return self.API_ROOT + ENDPOINTS[path_name].format(**kwargs)

    def _json_encode(self, payload):
        return json.dumps(payload, separators=(',', ':'), sort_keys=True)

    def _get_headers(self, ts='', sig=''):
        headers = {
            "ACCEPT": "application/json",
            "CONTENT-TYPE": "application/json",
            "X-BTK-TIMESTAMP": "{0}".format(ts),
            "X-BTK-APIKEY": "{0}".format(self.api_key),
            "X-BTK-SIGN": "{0}".format(sig)
        }

        return headers
    
    def _get_signature(self, method, ts, url, payload=''):
        url_path = url.replace(self.API_ROOT, '')
        message = f"{ts}{method}{url_path}" + payload
        signature = hmac.new(self._get_api_secret(), msg=message.encode(), digestmod=hashlib.sha256).hexdigest()

        return signature

    def _get_timestamp(self):
        timestamp = int(time.time())

        return timestamp

    def _get_payload(self, **kwargs):
        payload = {}
        # payload = {"ts": self._get_timestamp()}
        # payload = {"ts": self.servertime()}
        payload.update(kwargs)
        # payload["sig"] = self._get_signature(payload)
        payload = self._json_encode(payload)

        return payload
    
    def _get_swap_sym(self, sym, is_base_quote=True):
        sym_swap = sym.split('_')
        
        if is_base_quote:
            if sym_swap[0] == 'THB':
                sym = f'{sym_swap[1]}_{sym_swap[0]}'
        else:
            if sym_swap[0] != 'THB':
                sym = f'{sym_swap[1]}_{sym_swap[0]}'

        return sym

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_api_secret(self, api_secret):
        self.api_secret = api_secret

    def latest_bitkub_official_api(self):
        self.v2_compatable = False

    def status(self):
        url = self._get_path("STATUS_PATH")

        return basic_request('GET', url)

    def servertime(self):
        url = self._get_path("SERVERTIME_PATH")

        return basic_request('GET', url)

    def transform_market_info(self, data):
        if not self.v2_compatable:
            return data
        
        result = {
            'error': data['error'],
            'result': []
        }
        
        for item in data['result']:
            # สลับตำแหน่ง symbol จาก BTC_THB เป็น THB_BTC
            base, quote = item['symbol'].split('_')
            new_symbol = f"{quote}_{base}"
            
            transformed_item = {
                'id': item['pairing_id'],
                'info': item['description'],
                'symbol': new_symbol
            }
            
            result['result'].append(transformed_item)
        
        return result
    def symbols(self):
        url = self._get_path("MARKET_SYMBOLS_PATH")

        return self.transform_market_info(basic_request('GET', url))

    # ฟังก์ชันแปลงรูปแบบ
    def transform_ticker(self, data):
        if not self.v2_compatable:
            return data
        
        result = {}
        
        for idx, item in enumerate(data, start=1):
            # สลับตำแหน่ง symbol จาก ADA_THB เป็น THB_ADA
            base, quote = item["symbol"].split("_")
            new_symbol = f"{quote}_{base}"
            
            # แปลงเป็นรูปแบบใหม่
            result[new_symbol] = {
                'id': idx,
                'last': float(item["last"]),
                'lowestAsk': float(item["lowest_ask"]),
                'highestBid': float(item["highest_bid"]),
                'percentChange': float(item["percent_change"]),
                'baseVolume': float(item["base_volume"]),
                'quoteVolume': float(item["quote_volume"]),
                'isFrozen': 0,
                'high24hr': float(item["high_24_hr"]),
                'low24hr': float(item["low_24_hr"]),
                'change': 0,  # ไม่มีข้อมูลในต้นฉบับ
                'prevClose': 0,  # ไม่มีข้อมูลในต้นฉบับ
                'prevOpen': 0  # ไม่มีข้อมูลในต้นฉบับ
            }
        
        return result
    def ticker(self, sym=''):
        url = self._get_path("MARKET_TICKER_PATH", sym=self._get_swap_sym(sym))

        return self.transform_ticker(basic_request('GET', url))

    def trades(self, sym='', lmt=1):
        url = self._get_path("MARKET_TRADES_PATH", sym=sym, lmt=lmt)

        return basic_request('GET', url)

    def bids(self, sym='', lmt=1):
        url = self._get_path("MARKET_BIDS_PATH", sym=sym, lmt=lmt)

        return basic_request('GET', url)

    def asks(self, sym='', lmt=1):
        url = self._get_path("MARKET_ASKS_PATH", sym=sym, lmt=lmt)

        return basic_request('GET', url)

    def books(self, sym='', lmt=1):

        raise NotImplementedError("The 'books' method is deprecated.")

    def tradingview(self, sym='', resolution=1, frm='', to=''):
        # frm = str(int(int(frm)/1000)) if int(frm) > 9999999999 else str(int(frm))
        # to = str(int(int(to)/1000)) if int(to) > 9999999999 else str(int(to))
        # if frm length > 10 cut last 3 digits
        frm = frm[:-3] if len(frm) > 10 else frm
        to = to[:-3] if len(to) > 10 else to
        url = self._get_path("MARKET_TRADING_VIEW_PATH", sym=self._get_swap_sym(sym), resolution=resolution, frm=frm, to=to)

        return basic_request('GET', url)

    def depth(self, sym='', lmt=1):
        url = self._get_path("MARKET_DEPTH_PATH", sym=sym, lmt=lmt)

        return basic_request('GET', url)

    @check_in_attributes(["api_key", "api_secret"])
    def wallet(self):
        url = self._get_path("MARKET_WALLET")
        payload = self._get_payload()
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)

        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def balances(self):
        url = self._get_path("MARKET_BALANCES")
        payload = self._get_payload()
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)

        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def place_bid(self, sym='', amt=1, rat=1, typ='limit', client_id=''):
        url = self._get_path("MARKET_PLACE_BID")
        payload = self._get_payload(sym=self._get_swap_sym(sym), amt=amt, rat=rat, typ=typ, client_id=client_id)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    # 2023-11-29 Deprecated
    def place_bid_test(self, sym='', amt=1, rat=1, typ='limit', client_id=''):

        raise NotImplementedError("The 'books' method is deprecated.")

    @check_in_attributes(["api_key", "api_secret"])
    def place_ask(self, sym='', amt=1, rat=1, typ='limit', client_id=''):
        url = self._get_path("MARKET_PLACE_ASK")
        payload = self._get_payload(sym=self._get_swap_sym(sym), amt=amt, rat=rat, typ=typ, client_id=client_id)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    # 2023-11-29 Deprecated
    def place_ask_test(self, sym='', amt=1, rat=1, typ='limit', client_id=''):

        raise NotImplementedError("The 'books' method is deprecated.")

    # 2023-03-27 Deprecated
    # mapping function form place_ask_by_fiat to place_ask
    @check_in_attributes(["api_key", "api_secret"])
    def place_ask_by_fiat(self, sym='', amt=1, rat=1, typ='limit', client_id=''):
        coin_amt = amt/rat if rat > 0 else amt
        return self.place_ask(sym=sym, amt=coin_amt, rat=rat, typ=typ, client_id=client_id)

    @check_in_attributes(["api_key", "api_secret"])
    def cancel_order(self, sym='', id='', sd='buy', hash=''):
        url = self._get_path("MARKET_CANCEL_ORDER")
        payload = self._get_payload(sym=sym, id=id, sd=sd, hash=hash)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def my_open_orders(self, sym=''):
        url = self._get_path("MARKET_MY_OPEN_ORDERS", sym=self._get_swap_sym(sym))
        ts = self.servertime()
        sig = self._get_signature('GET', ts, url)
        
        return basic_request('GET', url, headers=self._get_headers(ts, sig))

    @check_in_attributes(["api_key", "api_secret"])
    def my_open_history(self, sym='', p=1, lmt=10, start=None, end=None):
        if start is None or end is None:
            url = self._get_path("MARKET_MY_ORDER_HISTORY", sym=self._get_swap_sym(sym), p=p, lmt=lmt)
        else:
            url = self._get_path("MARKET_MY_ORDER_HISTORY_STARTEND", sym=self._get_swap_sym(sym), p=p, lmt=lmt, start=start, end=end)
        ts = self.servertime()
        sig = self._get_signature('GET', ts, url)
        
        return basic_request('GET', url, headers=self._get_headers(ts, sig))

    @check_in_attributes(["api_key", "api_secret"])
    def order_info(self, sym='', id=None, sd='buy', hash=''):
        url = self._get_path("MARKET_ORDER_INFO", sym=self._get_swap_sym(sym), id=id, sd=sd, hash=hash)
        ts = self.servertime()
        sig = self._get_signature('GET', ts, url)
        
        return basic_request('GET', url, headers=self._get_headers(ts, sig))

    def transform_crypto_address(self, data):
        if not self.v2_compatable:
            return data
        
        result = {
            'error': int(data['code']),
            'result': [],
            'pagination': {
                'page': data['data']['page'],
                'last': data['data']['total_page']
            }
        }
        
        # แปลง items
        for item in data['data']['items']:
            # แปลง ISO datetime เป็น Unix timestamp
            dt = datetime.fromisoformat(item['create_at'].replace('Z', '+00:00'))
            timestamp = int(dt.timestamp())
            
            transformed_item = {
                'currency': item['symbol'],
                'address': item['address'],
                'tag': int(item['memo']) if item.get('memo') else 0,
                'time': timestamp
            }
            
            result['result'].append(transformed_item)
        
        return result
    @check_in_attributes(["api_key", "api_secret"])
    def crypto_address(self, p=1, lmt=10):
        url = self._get_path("CRYPTO_ADDRESSES")
        payload = self._get_payload(p=p, lmt=lmt)
        ts = self.servertime()
        sig = self._get_signature('GET', ts, url, payload)
        
        return self.transform_crypto_address(basic_request('GET', url, headers=self._get_headers(ts, sig), payload=payload))

    def transform_crypto_withdraw(self, data):
        if not self.v2_compatable:
            return data
        
        item = data['data']
    
        # แปลง ISO datetime เป็น Unix timestamp
        dt = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
        timestamp = int(dt.timestamp())
        
        result = {
            'error': int(data['code']),
            'result': {
                'txn': item['txn_id'],
                'adr': item['address'],
                'mem': item['memo'],
                'cur': item['symbol'],
                'amt': float(item['amount']),
                'fee': float(item['fee']),
                'ts': timestamp
            }
        }
        
        return result
    @check_in_attributes(["api_key", "api_secret"])
    def crypto_withdraw(self, cur='', amt=0, adr='', mem='', network=''):
        url = self._get_path("CRYPTO_WITHDRAW")
        payload = self._get_payload(symbol=cur, amount=amt, address=adr, memo=mem, network=network)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return self.transform_crypto_withdraw(basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload))

    # 2025-12-03 Deprecated
    def crypto_internal_withdraw(self, cur='', amt=0, adr='', mem=''):
        
        raise NotImplementedError("The 'books' method is deprecated.")

    def transform_deposit_history(self, data):
        if not self.v2_compatable:
            return data
        
        result = {
            'error': int(data['code']),
            'result': [],
            'pagination': {
                'page': data['data']['page'],
                'last': data['data']['total_page']
            }
        }
        
        # แปลง items
        for item in data['data']['items']:
            # แปลง ISO datetime เป็น Unix timestamp
            dt = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
            timestamp = int(dt.timestamp())
            
            transformed_item = {
                'hash': item['hash'],
                'currency': item['symbol'],
                'amount': float(item['amount']),
                'from_address': item['from_address'],
                'to_address': item['to_address'],
                'confirmations': item['confirmations'],
                'status': item['status'],
                'time': timestamp
            }
            
            result['result'].append(transformed_item)
        
        return result
    @check_in_attributes(["api_key", "api_secret"])
    def crypto_deposit_history(self, p=1, lmt=10):
        url = self._get_path("CRYPTO_DEPOSIT_HISTORY")
        payload = self._get_payload(p=p, lmt=lmt)
        ts = self.servertime()
        sig = self._get_signature('GET', ts, url, payload)
        
        return self.transform_deposit_history(basic_request('GET', url, headers=self._get_headers(ts, sig), payload=payload))

    def transform_withdraw_history(self, data):
        if not self.v2_compatable:
            return data
        
        result = {
            'error': int(data['code']),
            'result': [],
            'pagination': {
                'page': data['data']['page'],
                'last': data['data']['total_page']
            }
        }
        
        # แปลง items
        for item in data['data']['items']:
            # แปลง ISO datetime เป็น Unix timestamp
            dt = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
            timestamp = int(dt.timestamp())
            
            transformed_item = {
                'txn_id': item['txn_id'],
                'hash': item['hash'],
                'currency': item['symbol'],
                'amount': float(item['amount']),
                'fee': item['fee'],
                'address': item['address'],
                'status': item['status'],
                'time': timestamp
            }
            
            result['result'].append(transformed_item)
        
        return result
    @check_in_attributes(["api_key", "api_secret"])
    def crypto_withdraw_history(self, p=1, lmt=10):
        url = self._get_path("CRYPTO_WITHDRAW_HISTORY")
        payload = self._get_payload(p=p, lmt=lmt)
        ts = self.servertime()
        sig = self._get_signature('GET', ts, url, payload)
        
        return self.transform_withdraw_history(basic_request('GET', url, headers=self._get_headers(ts, sig), payload=payload))

    @check_in_attributes(["api_key", "api_secret"])
    def crypto_generate_address(self, sym='', network=''):
        url = self._get_path("CRYPTO_GENERATE_ADDRESS")
        if network == '':
            network = sym
        payload = self._get_payload(symbol=sym, network=network)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def fiat_accounts(self, p=1, lmt=10):
        url = self._get_path("FIAT_ACCOUNTS")
        payload = self._get_payload(p=p, lmt=lmt)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def fiat_withdraw(self, id='', amt=0):
        url = self._get_path("FIAT_WITHDRAW")
        payload = self._get_payload(id=id, amt=amt)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def fiat_deposit_history(self, p=1, lmt=10):
        url = self._get_path("FIAT_DEPOSIT_HISTORY")
        payload = self._get_payload(p=p, lmt=lmt)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def fiat_withdraw_history(self, p=1, lmt=10):
        url = self._get_path("FIAT_WITHDRAW_HISTORY")
        payload = self._get_payload(p=p, lmt=lmt)
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def market_wstoken(self):
        url = self._get_path("MARKET_WSTOKEN")
        payload = self._get_payload()
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def user_limits(self):
        url = self._get_path("USER_LIMITS")
        payload = self._get_payload()
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)

    @check_in_attributes(["api_key", "api_secret"])
    def user_trading_credits(self):
        url = self._get_path("USER_TRADING_CREDITS")
        payload = self._get_payload()
        ts = self.servertime()
        sig = self._get_signature('POST', ts, url, payload)
        
        return basic_request('POST', url, headers=self._get_headers(ts, sig), payload=payload)
