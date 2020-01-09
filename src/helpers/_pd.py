from configs.path import DB_PATH
import os
import pandas as pd

db_folder = os.path.join(os.getcwd(), DB_PATH)

def parse_html_to_excel(source, file_name, tab_name, is_source_not_df = False):
    is_multiple_df = len(source) > 1;
    pds_df = source[0]

    print('source %s' % source)
    if is_source_not_df:
        pds_df = pd.read_html(source)

    target_file = db_folder + file_name

    print('DF %s is saved to %s' % (pds_df, target_file))

    if not os.path.exists(target_file):
        with open(target_file, 'w'): pass

    with pd.ExcelWriter(target_file, mode='w', date_format='YYYY-MM-DD') as writer:
        pds_df.to_excel(writer, sheet_name=tab_name, index=False)
