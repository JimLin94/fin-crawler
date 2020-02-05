from helpers._mysql import df_insert_to_db
import pandas as pd
import re
from datetime import datetime
import os

from configs.url import N225
from configs.path import DB_PATH

file_path = os.path.join(os.getcwd(), DB_PATH)

def convert_csv_to_sql():
    files = [f for f in os.listdir(file_path) if '.xlsx' in f]
    df = pd.DataFrame()

    for csv in files:
        file_created_date = re.match(r'^2020(\d+)', csv)
        date_format = datetime.strptime(file_created_date.group(), '%Y%m%d')
        db_format_date = date_format.strftime('%Y/%m/%d')
        d = pd.read_excel(file_path + '/' + csv)
        print('File date %s' % db_format_date)

        if 'Date' not in d:
            d['Date'] = db_format_date
        if d['Date'].astype('str').str.contains(db_format_date) > 0:
            print("Data has been added %s" % db_format_date)

        print(d)
        df = df.append(d, ignore_index=True)

    db = df.drop(['Timestamp'], axis=1)
    # df_insert_to_db('n225', db, '')
    print(db)

if __name__ == '__main__':
    convert_csv_to_sql()
