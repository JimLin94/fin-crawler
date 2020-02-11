import wget
import os

from helpers._selenium import ClientSideCrawler
from configs.url import TOPIX
from configs.path import DB_PATH
from helpers._pd import parse_xlsx_to_df

DATA_STORE_PATH = os.path.join(os.getcwd(), DB_PATH)

def topix_spider():
    try:
        browser = ClientSideCrawler(TOPIX, True)
        driver = browser.driver
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
            df = parse_xlsx_to_df(file_name)
            df['Issue to which the liquidity factor is applied'] = df[
                'Issue to which the liquidity factor is applied'].fillna(0)
            df['Issue to which the liquidity factor is applied'] = df[
                'Issue to which the liquidity factor is applied'].replace('○', 1)
            print('DF %s' % df)

        driver.close()
    except Exception as inst:
        print('Error occurs while running TOPIX %s' % inst)


if __name__ == '__main__':
    topix_spider()
