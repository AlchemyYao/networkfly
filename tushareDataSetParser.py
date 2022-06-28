import numpy as np
import pandas as pd
import tushare as ts
from pathlib2 import Path
import time

class TushareData():
    def __init__(self, tushare_token) -> None:
        self.token = tushare_token
        self.code_list = []
        self.tushareDataParser()

    def stockBasicParser(self, ts_code):
        ts.set_token(self.token)
        pro = ts.pro_api()
        for _ in range(60):
            try:
                df= ts.pro_bar(ts_code= ts_code, adj= "qfq")
            except:
                time.sleep(1)
            else:
                return df

    def tushareDataParser(self):
        ts.set_token(self.token)
        pro = ts.pro_api()
        df_stock_basic = pro.stock_basic(exchange='', list_status='L')
        stock_basic_path= Path.joinpath(Path(__file__).parent, "tushareDataSet", "stockBaisc.csv")
        df_stock_basic.to_csv(path_or_buf= stock_basic_path, sep= ",", index_label= "idx")
        self.code_list = df_stock_basic["ts_code"].to_list()
        for item in self.code_list:
            df = self.stockBasicParser(ts_code= item)
            stock_code_path= Path.joinpath(Path(__file__).parent, "tushareDataSet", item.replace(".", "") + ".csv")
            df.to_csv(path_or_buf= stock_code_path, sep= ",", index_label= "idx")

if __name__== "__main__":
    tushareData= TushareData(tushare_token= "d41c8f225d930f0ec3b17df7871bdfa5c74daf110c162435e0a8d0c4")