import json
import config
from binance.client import Client
from binance.enums import *
import math 
from binance.helpers import round_step_size
import Constant

#Create Binance Connection through API

client = Client(config.API_KEY,config.API_SECRET,tld= 'com')

btc_quantity = Constant.BTC_QUANTITY

# Target: the rate of profit with the associated percentage of quantity you want to trade

targets = [{'target': 1.15 , 'percentage' : 0.5 },
			{'target': 1.24 , 'percentage' : 1.0 }]

# Parameter to check that stop loss trigger and stop loss price are not too close. 

stop_loss_trigger = 0.93
stop_loss = 0.90

pair = 'BTC'
print('Select the token: ')
SYMBOL = input()

TRADE_SYMBOL  = (SYMBOL+pair).upper()
# make MARKET BUY ORDER
order = client.order_market_buy( symbol= TRADE_SYMBOL, quoteOrderQty=btc_quantity)

# Retrieve step and tick size of the symbol

symbol_info =  client.get_symbol_info(TRADE_SYMBOL)
step_size = 1.0/float(json.loads(json.dumps(symbol_info))['filters'][2]['stepSize'])
tick_size = float(json.loads(json.dumps(symbol_info))['filters'][0]['tickSize'])


price_bought = float(order['fills'][0]['price']) 

#Formatting the stop price trigger and stop price limit 
stop_price_trigger = str(round_step_size( price_bought*stop_loss_trigger, tick_size))
stop_price_limit = str(round_step_size( price_bought*stop_loss, tick_size))

TRADE_QUANTITY = float(client.get_asset_balance(asset= SYMBOL)['free'])

# Fill  OCO ORDERS 

for el in targets:
	price_target = str(round_step_size( price_bought*el['target'], tick_size))
	quantity_target = math.floor(TRADE_QUANTITY*el['percentage']*step_size)/step_size
	
	order = client.create_oco_order(
    symbol=TRADE_SYMBOL,
    side=SIDE_SELL,
    price = price_target, 
    quantity= quantity_target,
    stopPrice = stop_price_trigger,
    stopLimitPrice = stop_price_limit,
    stopLimitTimeInForce = TIME_IN_FORCE_GTC
    )
	TRADE_QUANTITY = TRADE_QUANTITY - quantity_target
	print(order)
print('END')	


