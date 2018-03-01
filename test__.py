# !/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql
import csv


conn = pymysql.connect(host='127.0.0.1', port=3306, user='liyufeng', password='liyufeng', db='dbdb', charset='utf8')
cursor = conn.cursor()
info = """
create table doubanMovie (
电影 varchar(500),
产地 VARCHAR(500),
类型 varchar(500),
主旨 varchar(500),
评分 VARCHAR(500),
日期 VARCHAR(500),
url varchar(200)
);
"""
cursor.execute(info)

with open('doubanMovie_TOP250.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    for num, line in enumerate(reader):
        if num > 0:
            row = """insert into doubanMovie values(%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(row, (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))

conn.commit()
cursor.close()
conn.close()