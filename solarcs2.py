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
solar_azimuth_deg=110
solar_efficiency=0.21

def get_electrovalence(month,hour):
    if month in sharp_months:
        if hour in sharp_hours:
            return sharp_electrovalence
        elif hour in leap_hours:
            return leap_electrovalence
        elif hour in flat_hours:
            return flat_electrovalence
        elif hour in valley_hours:
            return valley_electrovalence
    else:
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
        a=math.cos(solar_altitude_deg/180*math.pi)
        b=math.sin(sun_altitude_deg/180*math.pi)
        c=math.sin(solar_altitude_deg/180*math.pi)
        d=math.cos((sun_azimuth_deg - solar_azimuth_deg)/180*math.pi) 
        e=sun_power*(a*b+c*d)
        if e>1:
            return e
        else:
            return 0

def get_solar_price(month,hour,solar_power):
    a=get_electrovalence(month,hour)
    return a*solar_power

with open('./data4.csv','w',encoding='utf-8') as f:
    cw= csv.writer(f)
    row=["日期","倾斜负5度光伏电价","倾斜0度光伏电价","倾斜5度光伏电价","倾斜10度光伏电价","倾斜15度光伏电价","倾斜20度光伏电价"]
    cw.writerow(row)
    for m in month:
        for d in range(days[m-1]):
            a1=0
            a2=0
            a3=0
            a4=0
            a5=0
            a6=0
            for i in range(24):
                for j in range(4):
                    date = datetime.datetime(2023, m, d+1, i, j*15, 10,tzinfo=timezone('Asia/Chongqing'))
                    ymd="2023-"+str(m)+"-"+str(d+1)
                    hs=str(i)+":"+str(j*15)
                    sun_altitude_deg = get_altitude(latitude, longitude, date)
                    sun_azimuth_deg  = get_azimuth(latitude, longitude, date)
                    sun_power=radiation.get_radiation_direct(date, sun_altitude_deg)
                    solar_power1=get_solar_power(sun_power,sun_altitude_deg,sun_azimuth_deg,-5,solar_azimuth_deg)
                    solar_price1=get_solar_price(m,i,solar_power1)*0.25
                    a1=a1+solar_price1
                    solar_power2=get_solar_power(sun_power,sun_altitude_deg,sun_azimuth_deg,0,solar_azimuth_deg)
                    solar_price2=get_solar_price(m,i,solar_power2)*0.25
                    a2=a2+solar_price2
                    solar_power3=get_solar_power(sun_power,sun_altitude_deg,sun_azimuth_deg,5,solar_azimuth_deg)
                    solar_price3=get_solar_price(m,i,solar_power3)*0.25
                    a3=a3+solar_price3
                    solar_power4=get_solar_power(sun_power,sun_altitude_deg,sun_azimuth_deg,10,solar_azimuth_deg)
                    solar_price4=get_solar_price(m,i,solar_power4)*0.25
                    a4=a4+solar_price4
                    solar_power5=get_solar_power(sun_power,sun_altitude_deg,sun_azimuth_deg,15,solar_azimuth_deg)
                    solar_price5=get_solar_price(m,i,solar_power5)*0.25
                    a5=a5+solar_price5
                    solar_power6=get_solar_power(sun_power,sun_altitude_deg,sun_azimuth_deg,20,solar_azimuth_deg)
                    solar_price6=get_solar_price(m,i,solar_power6)*0.25
                    a6=a6+solar_price6
            row=[ymd,a1,a2,a3,a4,a5,a6]
            cw.writerow(row)
