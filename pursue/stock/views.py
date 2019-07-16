# -*- coding: utf-8 -*-

from flask import Blueprint,render_template
from pursue.user.views import login_required
from pyecharts.charts import Bar, Kline
from pyecharts import options as opts
from jinja2 import Markup
from pursue.for_future.predict import PredictFuture
from pursue.for_future.stock.stockdata import StockData
from datetime import datetime
import pandas as pd
import logging
from flask import request
import time
from pandas import to_datetime
import numpy as np

bpp = Blueprint("stock_for_page", __name__ ,url_prefix="/stock")




def kline_datazoom_slider(times,stock_data) -> Kline:
    c = (
        Kline()
        .add_xaxis(times)
        .add_yaxis("kline", stock_data)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts()],
            title_opts=opts.TitleOpts(title="未来5天股票走势"),
        )
    )
    return c

'''
动静分离模式
'''
@bpp.route("/")
def index():
    return render_template("stock/pyecharts.html")


@bpp.route("/predict", methods=["GET","POST"])
def predict():
    #页面用户输入股票代码、公司上市时间
    stockCode = request.form["stockCode"]
    startDate = request.form["startDate"]
    today = time.strftime("%Y-%m-%d", time.localtime())
    logging.info("the stock code: %s, IPO date: %s,predict date: %s",stockCode,startDate,today)
    obj = StockData(stockCode)  # 创建股票交易类对象
    # 获取股价变动的历史数据
    data = obj.history(start=startDate, end=today)
    times = data.date.values
    stock_data = data[['open','close','low','high']].values
   # 预测未来5天内收盘价 linear 模型
    closeValue = {'ds': data['date'], 'y': data['close']}
    #logistic 模型
    # closeValue = {'ds': data['date'], 'y': data['close'], 'cap': data['high'], 'floor': data['low'], 'low': data['low']}
    df_close_value = pd.DataFrame(closeValue)
    # 预测数据linear/logistic
    predict_close_future = PredictFuture(growth='linear', data_frame=df_close_value)
    predict_close_future.seeFuture(periods=1, freq='D', include_history=False)
    df_dt = to_datetime(predict_close_future._future.ds, format="%Y-%m-%d")
    df_dt_str = df_dt.apply(lambda x: datetime.strftime(x, "%Y-%m-%d"))
    forecast_trend = predict_close_future._forecast.trend
    forecast_yhat = predict_close_future._forecast.yhat
    forecast_yhat_lower = predict_close_future._forecast.yhat_lower
    forecast_yhat_upper = predict_close_future._forecast.yhat_upper
    forecast_trend_fmt = forecast_trend.apply(lambda x:('%.2f') % x)
    forecast_yhat_fmt = forecast_yhat.apply(lambda x: ('%.2f') % x)
    forecast_yhat_lower_fmt = forecast_yhat_lower.apply(lambda x: ('%.2f') % x)
    forecast_yhat_upper_fmt = forecast_yhat_upper.apply(lambda x: ('%.2f') % x)
    forecast_data_fmt = {'yhat':forecast_yhat_fmt.values.tolist(),'trend':forecast_trend_fmt.values.tolist(),'yhat_lower':forecast_yhat_lower_fmt.values.tolist(),'yhat_upper':forecast_yhat_upper_fmt.values.tolist()}
    times_list = times.tolist()
    stock_data_list = stock_data.tolist()
    times_list = times_list + df_dt_str.values.tolist()
    stock_data_list = stock_data_list + pd.DataFrame(forecast_data_fmt).values.tolist()
    c = kline_datazoom_slider(times_list,stock_data_list)
    return c.dump_options()