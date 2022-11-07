import sys
import pandas as pd
import matplotlib.pyplot as plt
print (sys.argv)
# 设置font字典为 SimSun（宋体），大小为12（默认为10）
font = {'family' : 'SimSun',
        'size'  : '12'}
# 设置 字体
plt.rc('font', **font)
# 解决中文字体下坐标轴负数的负号显示问题
plt.rc('axes', unicode_minus=False)
a=pd.read_csv(sys.argv[1])
b=a.iloc[0:365,6:102]
b.boxplot()
plt.show()
