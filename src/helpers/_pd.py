from configs.path import DB_PATH
import os
import pandas as pd

db_folder = os.path.dirname(os.getcwd() + DB_PATH)

def parse_html_to_excel(data_frame, file_name, tab_name):
    pds_df = pd.read_html(data_frame)
    target_file = db_folder + file_name + '.xlsx'

    print('DF %s' % pds_df)

    if not os.path.exists(target_file):
        with open(target_file, 'w'): pass

    with pd.ExcelWriter(target_file, mode='w', date_format='YYYY-MM-DD') as writer:
        pds_df.to_excel(writer, sheet_name=tab_name)
