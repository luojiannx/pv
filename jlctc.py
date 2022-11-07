import csv
import math
import numpy as np

month=(1,2,3,4,5,6,7,8,9,10,11,12)
days=(31,28,31,30,31,30,31,31,30,31,30,31)
sharp_months=(1,7,8,9,12)
sharp_hours=(18,19,20,21)
leap_hours=(11,12,13,18,19,20,21,22)
flat_hours=(7,8,9,10,14,15,16,17)
valley_hours=(0,1,2,3,4,5,6,23)
sharp_electrovalence=1.43451
leap_electrovalence=1.20313
flat_electrovalence=0.76930
valley_electrovalence=0.33547
solar_altitude_deg=5
solar_azimuth_deg=190
solar_efficiency=0.21
row=[]
changdu_power=21
#jiulongcang_power=3.7
jlc=[]
cd=[]

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


def get_solar_price(month,hour,solar_power):
    a=get_electrovalence(month,hour)
    return a*solar_power

with open('./jiulongcang.csv',encoding='utf-8') as f:
    cw=csv.reader(f)
    for row in cw:
        for cell in range(96):
            jlc.append(row[6+cell])

with open('./changdu.csv',encoding='utf-8') as f:
    cw= csv.reader(f)
    for row in cw:
        for cell in range(96):
            cd.append(row[6+cell])

with open('./testjlc.c','w',encoding='utf-8') as f:
    f.write("jlcdata={\n")
    for i in jlc:
        f.write(str(i))
        f.write(",\n")
    f.write("}\n")
