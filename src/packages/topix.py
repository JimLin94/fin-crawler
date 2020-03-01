import wget
import os

from helpers._selenium import ClientSideCrawler
from configs.url import TOPIX
from configs.path import DB_PATH
from helpers._pd import parse_xlsx_to_df
from helpers._mysql import df_insert_to_db, PyMysql
import pandas as pd

DATA_STORE_PATH = os.path.join(os.getcwd(), DB_PATH)

TABLE_NAME = 'topix'

def topix_spider():
    browser = ClientSideCrawler(TOPIX, True)
    driver = browser.driver

    try:
        href = driver.execute_script('''
            var sections = document.querySelectorAll('.component-file');
            var targetIdx = -1;

            if (sections) {
                for (var i = 0; i < sections.length; i++) {
                    if (sections[i].innerText.search(/TOPIX Component Stocks Weight/) > -1) {
                        targetIdx = i;
                    }
                }
            }

            if (targetIdx > -1) {
                var href = sections[targetIdx].querySelector('a').href;

                return href;
            }
            ''')
        if href:
            file_name = wget.download(href, DATA_STORE_PATH)
            print('The file is downloaded as %s' % file_name)
            df = parse_xlsx_to_df(file_name, 7)
            df['Issue to which the liquidity factor is applied'] = df[
                'Issue to which the liquidity factor is applied'].fillna(0)
            df['Issue to which the liquidity factor is applied']= df['Issue to which the liquidity factor is applied'].apply(lambda x: 1 if x!=0 else 0)
            # df['Issue to which the liquidity factor is applied'] = df[
            #     'Issue to which the liquidity factor is applied'].notna().replace('○', 1)
            current_date = df['Date'].iloc[0]
            df['Date'] = df['Date'].iloc[0]

            db_con_inst = PyMysql()

            db_con_inst.cursur.execute('''
                CREATE TABLE IF NOT EXISTS %s (
                    date DATE,
                    issue VARCHAR(255),
                    code SMALLINT,
                    sector VARCHAR(255),
                    component_weight VARCHAR(255),
                    new_index_series_code VARCHAR(255),
                    issue_to_which_the_liquidity_factor_is_applied TINYINT
                ) CHARACTER SET utf8 COLLATE utf8_unicode_ci ENGINE=INNODB;
            ''' % TABLE_NAME)

            db_con_inst.cursur.execute('''
                SELECT * FROM %s WHERE date='%s'
            ''' % (TABLE_NAME, df['Date'].iloc[0]))

            has_data_existed = db_con_inst.cursur.fetchone()

            if has_data_existed:
                print('Data exists %s', df['Date'].iloc[0])
                browser.tear_down()
                return

            data_arr = list()

            for index, row in df.iterrows():
                updated_row_date = str(row[0]) if row[0] else None
                updated_row_issue = str(row[1]) if row[1] else None
                updated_row_code = str(row[2]) if row[2] else None
                updated_row_sector = str(row[3]) if row[3] else None
                updated_row_component = str(row[4]) if row[4] else None
                updated_row_new_index = str(row[5]) if row[5] else None
                updated_row_issue_to = str(row[6]) if row[6] else 0

                data_arr.append(
                    [updated_row_date, updated_row_issue, updated_row_code, updated_row_sector, updated_row_component, updated_row_new_index, updated_row_issue_to])
                query = 'INSERT INTO topix (`date`, `issue`, `code`, `sector`, `component_weight`, `new_index_series_code`, `issue_to_which_the_liquidity_factor_is_applied`) VALUES (%s, %s, %s, %s, %s, %s, %s)'

            db_con_inst.cursur.executemany(query, data_arr)
            db_con_inst.connection.commit()

        browser.tear_down()
    except Exception as inst:
        print('Error occurs while running TOPIX')
        print(inst)
        browser.tear_down()

if __name__ == '__main__':
    topix_spider()
