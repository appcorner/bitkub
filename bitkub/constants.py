ENDPOINTS = {
    "API_ROOT": "https://api.bitkub.com",
    "STATUS_PATH": "/api/status",
    "SERVERTIME_PATH": "/api/v3/servertime",
    "MARKET_SYMBOLS_PATH": "/api/v3/market/symbols",
    "MARKET_TICKER_PATH": "/api/v3/market/ticker?sym={sym}",
    "MARKET_TRADES_PATH": "/api/v3/market/trades?sym={sym}&lmt={lmt}",
    "MARKET_BIDS_PATH": "/api/v3/market/bids?sym={sym}&lmt={lmt}",
    "MARKET_ASKS_PATH": "/api/v3/market/asks?sym={sym}&lmt={lmt}",
    "MARKET_TRADING_VIEW_PATH": "/tradingview/history?symbol={sym}&resolution={resolution}&from={frm}&to={to}",
    "MARKET_DEPTH_PATH": "/api/v3/market/depth?sym={sym}&lmt={lmt}",

    # "MARKET_BOOKS_PATH": "/api/market/books?sym={sym}&lmt={lmt}",

    "MARKET_WALLET": "/api/v3/market/wallet",
    "MARKET_PLACE_BID": "/api/v3/market/place-bid",
    "MARKET_PLACE_ASK": "/api/v3/market/place-ask",
    "MARKET_CANCEL_ORDER": "/api/v3/market/cancel-order",
    "MARKET_BALANCES": "/api/v3/market/balances",
    "MARKET_MY_OPEN_ORDERS": "/api/v3/market/my-open-orders?sym={sym}",
    "MARKET_MY_ORDER_HISTORY": "/api/v3/market/my-order-history?sym={sym}&p={p}&lmt={lmt}",
    "MARKET_MY_ORDER_HISTORY_STARTEND": "/api/v3/market/my-order-history?sym={sym}&p={p}&lmt={lmt}&start={start}&end={end}",
    "MARKET_ORDER_INFO": "/api/v3/market/order-info?sym={sym}&id={id}&sd={sd}&hash={hash}",
    "MARKET_WSTOKEN": "/api/v3/market/wstoken",
    
    "CRYPTO_ADDRESSES": "/api/v4/crypto/addresses",
    "CRYPTO_WITHDRAW": "/api/v3/crypto/withdraw",
    "CRYPTO_DEPOSIT_HISTORY": "/api/v4/crypto/deposits",
    "CRYPTO_WITHDRAW_HISTORY": "/api/v4/crypto/withdraws",
    "CRYPTO_GENERATE_ADDRESS": "/api/v4/crypto/addresses",

    "FIAT_ACCOUNTS": "/api/v3/fiat/accounts",
    "FIAT_WITHDRAW": "/api/v3/fiat/withdraw",
    "FIAT_DEPOSIT_HISTORY": "/api/v3/fiat/deposit-history",
    "FIAT_WITHDRAW_HISTORY": "/api/v3/fiat/withdraw-history",

    "USER_TRADING_CREDITS": "/api/v3/user/trading-credits",
    "USER_LIMITS": "/api/v3/user/limits",
}
