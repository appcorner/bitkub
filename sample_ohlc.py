from bitkub import Bitkub

# v3
API_KEY = ""
API_SECRET = ""

bitkub = Bitkub()
bitkub.set_api_key(API_KEY)
bitkub.set_api_secret(API_SECRET)

coin_name = 'BTC'
symbol = f'THB_{coin_name}'

tf = 5  # time frame in minutes
bars = 10 # number of bars

bk_times = int(bitkub.servertime())
print("Bitkub server time:", bk_times)

time_from = (str(bk_times - (tf*60*1000)*bars))
time_to = (str(bk_times))

ohclv = bitkub.tradingview(symbol, tf, time_from, time_to)

print(f'OHCLV for {symbol} TF={tf}mins:')
print("from:", time_from, "to:", time_to)
print(ohclv)