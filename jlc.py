import csv
import math
import numpy as np

month=(1,2,3,4,5,6,7,8,9,10,11,12)
days=(31,28,31,30,31,30,31,31,30,31,30,31)
#湖南有尖的月份1，7，8，9，12
sharp_months=(1,7,8,9,12)
#尖时，对应时段为18，19，20，21时
sharp_hours=(18,19,20,21)
#峰时，在没有尖的月份，尖对应的时段成为峰
leap_hours=(11,12,13,18,19,20,21,22)
#平时
flat_hours=(7,8,9,10,14,15,16,17)
#谷时
valley_hours=(0,1,2,3,4,5,6,23)
#尖时电价
#sharp_electrovalence=1.43451
sharp_electrovalence=1.35733
#峰时电价
#leap_electrovalence=1.20313
leap_electrovalence=1.13881
#平时电价
#flat_electrovalence=0.76930
flat_electrovalence=0.72910
#谷时电价
#valley_electrovalence=0.33547
valley_electrovalence=0.31939
#csv每行数据的临时变量
row=[]
#昌都的装机量，准确数据是25.57，考虑是以往的小板，发电效率进行一定的折算
changdu_power=21
#给九龙仓的电价折扣率
discount_rate=0.95
#光伏上网电价
pv_grid_price=0.45
#存放九龙仓的8760*4负荷数据
jlc=[]
#存放昌都的8760*4发电数据
cd=[]

#根据月份和时段得到分时电价
def get_electrovalence(month,hour):
    if month in sharp_months:
        if hour in sharp_hours:
            return sharp_electrovalence
    if hour in leap_hours:
        return leap_electrovalence
    elif hour in flat_hours:
        return flat_electrovalence
    elif hour in valley_hours:
        return valley_electrovalence

#根据光伏出力大小以及时间段得到电价，及：出力大小*分时电价
def get_solar_price(month,hour,solar_power):
    a=get_electrovalence(month,hour)
    return a*solar_power

#取得用户（如：宁乡九龙仓时代奥特来斯）的全年的负荷数据，每15分钟一个点，总计（1+8760）*4个点，第一行为表头
with open('./huxuan.csv',encoding='utf-8') as f:
    cw=csv.reader(f)
    for row in cw:
        for cell in range(96):
            jlc.append(row[6+cell])

#取得宁乡双凫铺长度电站全年的发电数据，每15分钟一个点，总计（1+8760）*4个点，第一行为表头
with open('./changdu.csv',encoding='utf-8') as f:
    cw= csv.reader(f)
    for row in cw:
        for cell in range(96):
            cd.append(row[6+cell])

#根据不同的装机容量，以每15分钟一个点为单元，计算电量、电费、租金、电费单价、消纳比例
#jiulongcang_power:九龙仓光伏装机容量
#pricesum:电费积分，即湘有的纯收入（已扣除租金的部分）
#powersum:电量积分，即发电量
#rentsum:租金积分，湘有付给九龙仓的，按照：九龙仓消纳的光伏电量*分时电价*0.08
#netsum:上网电量积分，九龙仓没有消纳完的卖给国家电网的光伏电量
print("装机容量",end="")
print("\t发电量",end="")
print("\t\t电费",end="")
print("\t\t租金",end="")
print("\t\t上网电量",end="")
print("\t度电均价",end="")
print("\t消纳比例")
for jiulongcang_power in np.arange(0.05,0.4,0.05):
    pricesum=0
    powersum=0
    rentsum=0
    netsum=0
    td=0
    for m in month:
        for d in range(days[m-1]):
            for i in range(24):
                for j in range(4):
                    power1=float(cd[td+96])*jiulongcang_power/changdu_power
                    power2=float(jlc[td+96])
                    if power2>power1:
                        price=get_solar_price(m,i,power1)*discount_rate
                        rent=price/discount_rate*(1-discount_rate)
                        net=0
                    else:
                        price=get_solar_price(m,i,power2)*discount_rate+(power1-power2)*pv_grid_price
                        rent=get_solar_price(m,i,power2)*(1-discount_rate)
                        net=power1-power2
                    pricesum=pricesum+price*0.25
                    powersum=powersum+power1*0.25
                    rentsum=rentsum+rent*0.25
                    netsum=netsum+net*0.25
                    td=td+1
    print("{:.1f}".format(jiulongcang_power),end="")
    print("\t\t{:.0f}".format(powersum),end="")
    print("\t\t{:.0f}".format(pricesum),end="")
    print("\t\t{:.0f}".format(rentsum),end="")
    print("\t\t{:.0f}".format(netsum),end="")
    print("\t\t{:.4f}".format(pricesum/powersum),end="")
    print("\t\t{:.2f}%".format((1-netsum/powersum)*100))
