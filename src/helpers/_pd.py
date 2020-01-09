from configs.path import DB_PATH
import os
import pandas as pd
from openpyxl import load_workbook

db_folder = os.path.join(os.getcwd(), DB_PATH)

def parse_html_to_excel(source, file_name, tab_name, is_source_not_df = False):
    pds_df = source

    # print('source %s' % pds_df)
    if is_source_not_df:
        pds_df = pd.read_html(source)

    target_file = db_folder + '/' + file_name

    # print('DF %s is saved to %s' % (pds_df, target_file))

    # Create the {file_name} if not exists.
    if not os.path.exists(target_file):
        with open(target_file, 'w'): pass

    book = load_workbook(target_file)
    writer = pd.ExcelWriter(target_file, engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    print('writer %s' % writer.sheets)
    pds_df.to_excel(writer, tab_name, index=False)

    writer.save()

    # Write the data to the {file_name} with the tab name {tab_name}.
    # with pd.ExcelWriter(target_file, date_format='YYYY-MM-DD', engine = 'openpyxl') as writer:
    #     pds_df.to_excel(writer, sheet_name=tab_name, index=False)

