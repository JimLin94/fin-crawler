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

            data_arr = list([(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for index, row in df.iterrows()])
            print(data_arr)
            db_con_inst.cursur.executemany('INSERT INTO topix (`date`, `issue`, `code`, `sector`, `component_weight`, `new_index_series_code`, `issue_to_which_the_liquidity_factor_is_applied`) VALUE (%s)', data_arr)
            db_con_inst.commit()

        browser.tear_down()
    except Exception as inst:
        print('Error occurs while running TOPIX')
        print(inst)
        browser.tear_down()

if __name__ == '__main__':
    topix_spider()
