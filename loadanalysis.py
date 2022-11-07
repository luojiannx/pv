import csv
import math
from typing import TypedDict
import numpy as np

pricemode=2
discount_rate=0.8
pv_grid_price=0.45

month=(1,2,3,4,5,6,7,8,9,10,11,12)
days=(31,28,31,30,31,30,31,31,30,31,30,31)
sharp_months=(1,7,8,9,12)
sharp_hours=(18,19,20,21)
leap_hours=(11,12,13,18,19,20,21,22)
flat_hours=(7,8,9,10,14,15,16,17)
valley_hours=(0,1,2,3,4,5,6,23)
changdu_power=21
row=[]
jlc=[]
cd=[]
pr=[]
loadsum=0
sharpsum=0
leapsum=0
flatsum=0
valleysum=0
loadfee=0

if pricemode==1:
    sharp_electrovalence=1.43451
    leap_electrovalence=1.20313
    flat_electrovalence=0.76930
    valley_electrovalence=0.33547
if pricemode==2:
    sharp_electrovalence=1.35733
    leap_electrovalence=1.13881
    flat_electrovalence=0.72910
    valley_electrovalence=0.31939
    
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
     
def get_price_list():
    global pr
    for m in month:
        for d in range(days[m-1]):
            for i in range(24):
                for j in range(4):
                    pr.append(get_electrovalence(m,i))

def get_userload_list():
    global jlc
    with open('./changdu.csv','r') as f:
        cw=csv.reader(f)
        for row in cw:
            for cell in range(96):
                jlc.append(row[6+cell])
    for i in range(96):
        del jlc[0]

def get_pv_list():
    global cd
    with open('./changdu.csv','r') as f:
        cw=csv.reader(f)
        for row in cw:
            for cell in range(96):
                cd.append(row[6+cell])
    for i in range(96):
        del cd[0]

def analysis_userload():
    global loadsum,sharpsum,leapsum,flatsum,valleysum,loadfee,jlc,pr
    td=0
    for i in jlc:
        dpr=float(pr[td])
        dload=float(i)*0.25      
        if dpr==sharp_electrovalence:
            sharpsum=sharpsum+dload
        elif dpr==leap_electrovalence:
            leapsum=leapsum+dload
        elif dpr==flat_electrovalence:
            flatsum=flatsum+dload
        elif dpr==valley_electrovalence:
            valleysum=valleysum+dload
        td=td+1
    loadsum=sharpsum+leapsum+flatsum+valleysum
    loadfee=sharpsum*sharp_electrovalence+leapsum*leap_electrovalence+flatsum*flat_electrovalence+valleysum*valley_electrovalence

def print_userload_info():
    print("年总电量：{:.0f}度".format(loadsum))
    print("月平均电量：{:.0f}度".format(loadsum/12))
    print("年总电费：{:.0f}元".format(loadfee))
    print("月平均电费：{:.0f}元".format(loadfee/12))
    print("度电均价：{:.4f}元".format(loadfee/loadsum))
    print("尖电量\t:\t",end="")
    print("峰电量\t:\t",end="")
    print("平电量\t:\t",end="")
    print("谷电量")
    print("{:.0f}\t:\t".format(sharpsum),end="")
    print("{:.0f}\t:\t".format(leapsum),end="")
    print("{:.0f}\t:\t".format(flatsum),end="")
    print("{:.0f}".format(valleysum))
    print("{:.0f}%\t:\t".format(sharpsum/loadsum*100),end="")
    print("{:.0f}%\t:\t".format(leapsum/loadsum*100),end="")
    print("{:.0f}%\t:\t".format(flatsum/loadsum*100),end="")
    print("{:.0f}%".format(valleysum/loadsum*100))
    
    
def analysis_pv():
    print("装机容量",end="")
    print("\t发电量",end="")
    print("\t\t电费",end="")
    print("\t\t租金",end="")
    print("\t\t上网电量",end="")
    print("\t度电均价",end="")
    print("\t消纳比例")
    for jiulongcang_power in np.arange(0.1,8.1,0.1):
        td=0
        pricesum=0
        powersum=0
        rentsum=0
        netsum=0
        for i in jlc:
            power1=float(cd[td])*jiulongcang_power/changdu_power
            power2=float(jlc[td])
            dpr=float(pr[td])
            if power2>power1:
                price=power1*dpr*discount_rate
                rent=price/discount_rate*(1-discount_rate)
                net=0
            else:
                price=power2*dpr*discount_rate+(power1-power2)*pv_grid_price
                rent=power2*dpr*(1-discount_rate)
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

get_price_list()
get_userload_list()
get_pv_list()
analysis_userload()
print_userload_info()
analysis_pv()   

