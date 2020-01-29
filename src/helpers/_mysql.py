from sqlalchemy import create_engine
import pymysql.cursors
import pandas as pd
from settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

def df_insert_to_db(table_name, df):
    engine = create_engine(
        'mysql+pymysql://%s:%s@%s:%s' % (DB_USER, DB_PASS, DB_HOST, DB_PORT), echo=True)
    engine.execute('''
        CREATE DATABASE IF NOT EXISTS %s;
    ''' % (DB_NAME))
    engine.execute('''
        use %s;
    ''' % (DB_NAME))

    df.to_sql(table_name, con=engine, if_exists='append', index_label='id')
    result = engine.execute("SELECT * FROM %s" % table_name).fetchall()

    print(result)

def check_value_exist(search_query):
    connection = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER,
                                 password=DB_PASS, db=DB_NAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(search_query)
            result = cursor.fetchone()

            print('Result %s', result)

            return bool(result)
    finally:
        connection.close()
