from pysolar.solar import *
import datetime
from pytz import timezone
import csv

latitude = 28.2694
longitude = 112.689
row=[]
month=(1,2,3,4,5,6,7,8,9,10,11,12)
days=(31,28,31,30,31,30,31,31,30,31,30,31)
deltaDD=[]
deltaMD=[]

with open('./data.csv','w',encoding='utf-8') as f:
    cw= csv.writer(f)
    with open('./day.csv','w',encoding='utf-8') as g:
        dw= csv.writer(g)
        with open('./month.csv','w',encoding='utf-8') as h:
            ew= csv.writer(h)
            for m in month:
                isum=0
                dsum=0
                for d in range(days[m-1]):
                    jsum=0
                    for i in range(24):
                        for j in range(4):
                            date = datetime.datetime(2022, m, d+1, i, j*15+1, 10,tzinfo=timezone('Asia/Chongqing'))
                            ymd="2022-"+str(m)+"-"+str(d+1)
                            altitude_deg = get_altitude(latitude, longitude, date)
                            azimuth_deg  = get_azimuth(latitude, longitude, date)
                            r=radiation.get_radiation_direct(date, altitude_deg)
                            row=[ymd,altitude_deg,azimuth_deg,r]
                            cw.writerow(row)
                            jsum=jsum+r*0.25
                    deltaDD=[ymd,jsum]
                    dw.writerow(deltaDD)
                    dsum=dsum+jsum
                isum=isum+dsum
                ym="2022-"+str(m)
                deltaMD=[ym,isum]
                ew.writerow(deltaMD)

