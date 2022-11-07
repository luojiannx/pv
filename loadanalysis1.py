import csv
import math
import re
import os
from typing import TypedDict
import numpy as np
import pymysql

file_path = os.getcwd()
changdu_mped = '8000000066852083'
mped_year = '2021'

discount_rate=0.92
pv_grid_price=0.45

month=(1,2,3,4,5,6,7,8,9,10,11,12)
days=(31,28,31,30,31,30,31,31,30,31,30,31)
sharp_months=(1,7,8,9,12)
sharp_hours=(18,19,20,21)
leap_hours=(11,12,13,18,19,20,21,22)
flat_hours=(7,8,9,10,14,15,16,17)
valley_hours=(0,1,2,3,4,5,6,23)
changdu_power=21

mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'root', password= '7904295z', db= 'rzdyce')

cd = []
cd_sql = '''
    SELECT * FROM fct_cst_emppowercurve_d 
    WHERE mped_id IN ('%s') 
    AND data_date LIKE '%s%%' 
    ORDER BY data_date
''' % (changdu_mped, mped_year)
try:
    with mysql_conn.cursor() as cur:
        cur.execute(cd_sql)
        res = cur.fetchall()
        for res_item in res:
            for cell in range(96):
                cd.append(res_item[2 + cell])
except Exception as e:
    print(e)

tg_dict = {} # 记录台区测量点用于获取数据库数据
sql = '''
    SELECT * FROM dim_cst_mp_tg_info 
    WHERE city_org_nm IN ('国网长沙供电公司','国网岳阳供电公司') 
    AND (prc_cd_dsc LIKE '%工业用电%' OR prc_cd_dsc LIKE '%商业用电%') 
    AND volt_dsc <> '交流380V' 
    ORDER BY city_org_nm, prc_cd_dsc, volt_dsc
'''
try:
    with mysql_conn.cursor() as cur:
        cur.execute(sql)
        res = cur.fetchall()
        for res_item in res:
            tg_nm = '%s_%s_%s_%s' % (res_item[30], res_item[26], re.sub('[^\u4e00-\u9fa5]+', '', res_item[23].replace('（主）','').replace('（备）','').replace('（主供）','').replace('（备供）','').replace('(主供)','').replace('(备供)','').replace('主供','').replace('备供','').replace('(备用电源）','')), res_item[20])
            tg_nm = tg_nm.replace('国网','').replace('供电公司','公司').replace('乡镇供电所','供电所').replace('供电服务站','服务站')
            if tg_nm not in tg_dict.keys():
                tg_dict[tg_nm] = []
            tg_dict[tg_nm].append(res_item[12])
except Exception as e:
    print(e)
print(len(tg_dict))

for k,v in tg_dict.items():
    tg_nm = k
    tg_mped = str(v).replace('[','').replace(']','')

    jlc = []

    if tg_nm:
        ## 长沙公司_宁乡市公司_长沙时代奥特莱斯商业有限公司_商业用电(1～10KV)
        ## 岳阳公司_新港供电服务中心_岳阳鸿盛建设有限公司_商业用电(110KV)
        print(tg_nm, tg_mped)
        sql = '''
            SELECT a.tg_org_no AS org_no, a.tg_org_nm AS org_nm, MIN(a.tg_no) AS tg_no, MIN(a.tg_nm) AS tg_nm, SUM(a.mp_cap) AS cap, b.data_date, SUM(b.p1) AS p1, SUM(b.p2) AS p2, SUM(b.p3) AS p3, SUM(b.p4) AS p4, SUM(b.p5) AS p5, SUM(b.p6) AS p6, SUM(b.p7) AS p7, SUM(b.p8) AS p8, SUM(b.p9) AS p9, SUM(b.p10) AS p10, SUM(b.p11) AS p11, SUM(b.p12) AS p12, SUM(b.p13) AS p13, SUM(b.p14) AS p14, SUM(b.p15) AS p15, SUM(b.p16) AS p16, SUM(b.p17) AS p17, SUM(b.p18) AS p18, SUM(b.p19) AS p19, SUM(b.p20) AS p20, SUM(b.p21) AS p21, SUM(b.p22) AS p22, SUM(b.p23) AS p23, SUM(b.p24) AS p24, SUM(b.p25) AS p25, SUM(b.p26) AS p26, SUM(b.p27) AS p27, SUM(b.p28) AS p28, SUM(b.p29) AS p29, SUM(b.p30) AS p30, SUM(b.p31) AS p31, SUM(b.p32) AS p32, SUM(b.p33) AS p33, SUM(b.p34) AS p34, SUM(b.p35) AS p35, SUM(b.p36) AS p36, SUM(b.p37) AS p37, SUM(b.p38) AS p38, SUM(b.p39) AS p39, SUM(b.p40) AS p40, SUM(b.p41) AS p41, SUM(b.p42) AS p42, SUM(b.p43) AS p43, SUM(b.p44) AS p44, SUM(b.p45) AS p45, SUM(b.p46) AS p46, SUM(b.p47) AS p47, SUM(b.p48) AS p48, SUM(b.p49) AS p49, SUM(b.p50) AS p50, SUM(b.p51) AS p51, SUM(b.p52) AS p52, SUM(b.p53) AS p53, SUM(b.p54) AS p54, SUM(b.p55) AS p55, SUM(b.p56) AS p56, SUM(b.p57) AS p57, SUM(b.p58) AS p58, SUM(b.p59) AS p59, SUM(b.p60) AS p60, SUM(b.p61) AS p61, SUM(b.p62) AS p62, SUM(b.p63) AS p63, SUM(b.p64) AS p64, SUM(b.p65) AS p65, SUM(b.p66) AS p66, SUM(b.p67) AS p67, SUM(b.p68) AS p68, SUM(b.p69) AS p69, SUM(b.p70) AS p70, SUM(b.p71) AS p71, SUM(b.p72) AS p72, SUM(b.p73) AS p73, SUM(b.p74) AS p74, SUM(b.p75) AS p75, SUM(b.p76) AS p76, SUM(b.p77) AS p77, SUM(b.p78) AS p78, SUM(b.p79) AS p79, SUM(b.p80) AS p80, SUM(b.p81) AS p81, SUM(b.p82) AS p82, SUM(b.p83) AS p83, SUM(b.p84) AS p84, SUM(b.p85) AS p85, SUM(b.p86) AS p86, SUM(b.p87) AS p87, SUM(b.p88) AS p88, SUM(b.p89) AS p89, SUM(b.p90) AS p90, SUM(b.p91) AS p91, SUM(b.p92) AS p92, SUM(b.p93) AS p93, SUM(b.p94) AS p94, SUM(b.p95) AS p95, SUM(b.p96) AS p96
            FROM dim_cst_mp_tg_info a 
            LEFT JOIN fct_cst_emppowercurve_d b ON a.mped_id = b.mped_id
            WHERE a.mped_id IN (%s) 
            AND b.data_date LIKE '%s%%'
            GROUP BY a.tg_org_no, a.tg_org_nm, b.data_date
            ORDER BY b.data_date
        ''' % (tg_mped, mped_year)
        try:
            with mysql_conn.cursor() as cur:
                cur.execute(sql)
                res = cur.fetchall()
                for res_item in res:
                    for cell in range(96):
                        jlc.append(res_item[6 + cell])
        except Exception as e:
            print(e)

        if len(jlc) > 0:
            try:
                loadsum = 0
                sharpsum = 0
                leapsum = 0
                flatsum = 0
                valleysum = 0
                loadfee = 0
                td = 0

                if '商业用电' in tg_nm:
                    # 商业
                    sharp_electrovalence=1.43451
                    leap_electrovalence=1.20313
                    flat_electrovalence=0.76930
                    valley_electrovalence=0.33547
                if '工业用电' in tg_nm:
                    # 工业
                    sharp_electrovalence=1.35733
                    leap_electrovalence=1.13881
                    flat_electrovalence=0.72910
                    valley_electrovalence=0.31939

                pr = []
                for m in month:
                    for d in range(days[m-1]):
                        for i in range(24):
                            for j in range(4):
                                if i in leap_hours:
                                    if m in sharp_months and i in sharp_hours:
                                        pr.append(sharp_electrovalence)
                                    else:
                                        pr.append(leap_electrovalence)
                                elif i in flat_hours:
                                    pr.append(flat_electrovalence)
                                elif i in valley_hours:
                                    pr.append(valley_electrovalence)
                                
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

                pv_info = ''
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
                    pv_info += "%.1f,%.0f,%.0f,%.0f,%.0f,%.4f,%.2f%%\r\n" % (jiulongcang_power, powersum, pricesum, rentsum, netsum, pricesum/powersum, (1-netsum/powersum)*100)

                with open('%s\\%s.csv' % (file_path, tg_nm), 'w', encoding='gbk', newline='') as csvfile:
                    csvfile.write("年总电量,%.0f,年总电费,%.0f\r\n月均电量,%.0f,月均电费,%.0f\r\n度电均价,%.4f\r\n\r\n尖电量,峰电量,平电量,谷电量\r\n%.0f,%.0f,%.0f,%.0f\r\n%.2f%%,%.2f%%,%.2f%%,%.2f%%\r\n\r\n装机容量,发电量,电费,租金,上网电量,度电均价,消纳比例\r\n%s" % (loadsum, loadfee, loadsum/12, loadfee/12, loadfee/loadsum, sharpsum, leapsum, flatsum, valleysum, sharpsum/loadsum*100, leapsum/loadsum*100, flatsum/loadsum*100, valleysum/loadsum*100, pv_info))

            except Exception as e:
                print(e)