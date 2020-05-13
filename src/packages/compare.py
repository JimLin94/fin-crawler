import re
import sys
from helpers._mysql import PyMysql
from datetime import datetime

def compare_hl(today_hl, fetch_sql_table_name, today, save_to_table_name):
    try:
        db_con_inst = PyMysql()
        ''' 52 Week Range Compare'''
        db_con_inst.cursur.execute('''
            CREATE TABLE IF NOT EXISTS %s (
                new_low INT,
                new_high INT,
                date DATE
            ) CHARACTER SET utf8 ENGINE=INNODB;
        ''' % save_to_table_name)

        db_con_inst.cursur.execute('''
            SELECT date FROM %s ORDER BY date DESC LIMIT 1
        ''' % fetch_sql_table_name)

        latest_date = db_con_inst.cursur.fetchone()

        # print('dd %s' % (today.date() > latest_date['date']))

        # if (today.date() > latest_date['date']):
        #     print('The date is already compared %s' % today.date())
        #     return

        db_con_inst.cursur.execute('''
            SELECT * FROM %s WHERE DATE(date)='%s'
        ''' % (fetch_sql_table_name, str(latest_date['date'])))

        data = list(db_con_inst.cursur.fetchall())
        yesterday_hl_map = {}

        for item in data:
            yesterday_hl_map[item['company_code']] = item

        new_low = 0
        new_high = 0

        for hl in today_hl:
            if float(yesterday_hl_map[hl[0]]['52_week_range_low']) > float(hl[1]):
                new_low += 1
            if float(yesterday_hl_map[hl[0]]['52_week_range_high']) < float(hl[2]):
                new_high += 1

        query = 'INSERT INTO ' + save_to_table_name + ' (`new_low`, `new_high`, `date`) VALUES (%s, %s, %s)'

        db_con_inst.cursur.executemany(query, [[new_low, new_high, today.strftime('%Y/%m/%d')]])
        db_con_inst.connection.commit()
    except Exception as inst:
        print('Error occurs %s' % inst)
