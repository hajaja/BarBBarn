import tushare
import pandas as pd

# download stock name
strFileUserDictStockSymbol = 'userDictStockSymbol.txt'
dfBasic = tushare.get_stock_basics()
dfBasic.name.to_csv(strFileUserDictStockSymbol, header=None, encoding='utf-8', index=None, sep='\n')

