from helpers._mysql import PyMysql

def store_high_low(table_name, updated_time, source):
    try:
        print('Save %s at %s' % (table_name, updated_time))
        db_con_inst = PyMysql()
        ''' 52 Week Range '''
        db_con_inst.cursur.execute('''
            CREATE TABLE IF NOT EXISTS %s (
                company_code VARCHAR(255),
                52_week_range_low FLOAT,
                52_week_range_high FLOAT,
                date DATE
            ) CHARACTER SET utf8 ENGINE=INNODB;
        ''' % table_name)

        db_con_inst.cursur.execute('''
            SELECT * FROM %s WHERE date='%s'
        ''' % (table_name, updated_time))

        has_data_existed = db_con_inst.cursur.fetchone()

        if has_data_existed:
            print('Date is parsed already %s' % updated_time)
            return

        query = 'INSERT INTO ' + table_name + ' (`company_code`, `52_week_range_low`, `52_week_range_high`, `date`) VALUES (%s, %s, %s, %s)'
        print('Query %s' % query)
        db_con_inst.cursur.executemany(query, source)
        db_con_inst.connection.commit()
    except Exception as inst:
        print('Error occurs %s' % inst)
