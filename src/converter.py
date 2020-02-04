from helpers._mysql import df_insert_to_db
import pandas as pd
import os

from configs.url import N225
from configs.path import DB_PATH

file_path = os.path.join(os.getcwd(), DB_PATH)

def convert_csv_to_sql():
    files = [f for f in os.listdir(file_path) if '.xlsx' in f]
    df = pd.DataFrame()

    for csv in files:
        d = pd.read_excel(file_path + '/' + csv)
        print('File name %s' % csv)
        print(d)
        df = df.append(d, ignore_index=True)

    db = df.drop(['Timestamp'], axis=1)
    # df_insert_to_db('n225', db, '')
    print(db)

if __name__ == '__main__':
    convert_csv_to_sql()
