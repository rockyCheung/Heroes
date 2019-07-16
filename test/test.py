# -*- coding: utf-8 -*-

from pyecharts.charts import Bar
import time

# bar = Bar()
# bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
# bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# # 也可以传入路径参数，如 bar.render("mycharts.html")
# bar.render()
ipoDate = '2019-7-7'
predictDate = '2019-7-13'
# 格式化成2016-03-20 11:45:39形式

today = time.strftime("%Y-%m-%d", time.localtime())

print(today)

# 将格式字符串转换为时间戳
print(time.mktime(time.strptime(predictDate, "%Y-%m-%d"))>time.mktime(time.strptime(today, "%Y-%m-%d")))
print(time.strptime(today, "%Y-%m-%d"))