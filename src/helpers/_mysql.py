from sqlalchemy import create_engine
import os

HOST = os.getenv('HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')


def insert_to_db(table_name, data):
    connection = pymysql.connect(host=HOST, user=DB_USER, password=DB_PASS,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursors() as cursor:
            sql = "INSERT INTO `%s` (``)"
