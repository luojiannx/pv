from pysolar.solar import *
import datetime
from pytz import timezone
import csv
import math

latitude = 28.2694
longitude = 112.689
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
test_solar_altitude_deg=(-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90)
row=[]

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

def get_solar_power(sun_power,sun_altitude_deg,sun_azimuth_deg,solar_altitude_deg,solar_azimuth_deg):
    if sun_power<1:
        return 0
    else:
        a=math.cos(sun_altitude_deg/180*math.pi)
        b=math.sin(solar_altitude_deg/180*math.pi)
        c=math.sin(sun_altitude_deg/180*math.pi)
        d=math.cos(solar_altitude_deg/180*math.pi)
        e=math.cos((solar_azimuth_deg - sun_azimuth_deg)/180*math.pi) 
        f=sun_power*(a*b*e+c*d)
        if f>1:
            return f
        else:
            return 0

def get_solar_price(month,hour,solar_power):
    a=get_electrovalence(month,hour)
    return a*solar_power

with open('./timeoutlets8.csv','w',encoding='utf-8') as f:
    cw= csv.writer(f)
    for m in month:
        for d in range(days[m-1]):
            for i in range(24):
                for j in range(4):
                    date = datetime.datetime(2023, m, d+1, i, j*15, 10,tzinfo=timezone('Asia/Chongqing'))
                    ymd="2023-"+str(m)+"-"+str(d+1)
                    hs=str(i)+":"+str(j*15)
                    sun_altitude_deg = get_altitude(latitude, longitude, date)
                    sun_azimuth_deg  = get_azimuth(latitude, longitude, date)
                    sun_power=radiation.get_radiation_direct(date, sun_altitude_deg)
                    row=[ymd,hs,sun_altitude_deg,sun_azimuth_deg,sun_power]
                    for solar_altitude_deg in test_solar_altitude_deg:
                        solar_power=get_solar_power(sun_power,sun_altitude_deg,sun_azimuth_deg,solar_altitude_deg,solar_azimuth_deg)
                        solar_price=get_solar_price(m,i,solar_power)
                        row.append(solar_price)
                    cw.writerow(row)
