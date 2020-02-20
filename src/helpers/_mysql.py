from sqlalchemy import create_engine, inspect
import pymysql.cursors
import pandas as pd
from settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

def df_insert_to_db(table_name, df, check_value_column_name, check_value):
    engine = create_engine(
        'mysql+pymysql://%s:%s@%s:%s' % (DB_USER, DB_PASS, DB_HOST, DB_PORT), encoding = 'utf-8', echo=True)
    engine.execute('''
        CREATE DATABASE IF NOT EXISTS %s;
    ''' % (DB_NAME))
    engine.execute('''
        use %s;
    ''' % (DB_NAME))
    is_table_exist = engine.execute('''
        SHOW TABLES LIKE '%s';
    ''' % (table_name)).fetchone()

    if not is_table_exist:
        df.to_sql(table_name, con=engine, if_exists='append', index_label='id')
        result = engine.execute("SELECT * FROM %s" % table_name).fetchall()
    else:
        is_duplicated = engine.execute(
            'SELECT * FROM %s WHERE %s="%s"' % (table_name, check_value_column_name, check_value)).fetchone()

        print(is_duplicated)

        if not is_duplicated:
            df.to_sql(table_name, con=engine, if_exists='append', index_label='id')
            result = engine.execute("SELECT * FROM %s" % table_name).fetchall()
        else:
            print('Data exist %s' % check_value)

def run_query(query):
    connection = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER,
                                 password=DB_PASS, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(query)
    finally:
        connection.close()

def check_value_exist(search_query):
    connection = pymysql.connect(host=DB_HOST, port=int(DB_PORT), user=DB_USER,
                                 password=DB_PASS, db=DB_NAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(search_query)
            result = cursor.fetchone()

            return bool(result)
    finally:
        connection.close()
