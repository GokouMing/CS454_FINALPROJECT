import sqlite3
import sys
import pandas as pd


# Id,Name,CustomName,Quality,Description,ItemHeader,Class,WikiId,OwnerUrl,OwnerSteamId,IconId
def main():
    connection = sqlite3.connect('mainitem.db')

    cursor = connection.cursor()

    cursor.execute('''DROP TABLE IF EXISTS items''')

    command_create_table = '''CREATE VIRTUAL TABLE items USING fts5(Id, Name, CustomName, Quality, Description, 
                                ItemHeader, Class, WikiId, OwnerUrl, OwnerSteamId, IconId)'''

    cursor.execute(command_create_table)

    df = pd.read_csv('formattedDataset.csv')

    column = ['Id', 'Name', 'CustomName', 'Quality', 'Description', 'ItemHeader',
              'Class', 'WikiId', 'OwnerUrl', 'OwnerSteamId', 'IconId']

    # clean the data each column
    df.drop(df.query('Id.isnull() | CustomName.isnull() | Quality.isnull() |ItemHeader.isnull()'
                     '|Class.isnull() | WikiId.isnull() | OwnerUrl.isnull() | OwnerSteamId.isnull()'
                     '|IconId.isnull() | Name.isnull()').index, inplace=True)

    df_row_data = df[column]
    rows_data = df_row_data.values.tolist()

    command_insert_data = ''' INSERT INTO items ('Id', 'Name', 'CustomName', 'Quality', 'Description', 'ItemHeader',
              'Class', 'WikiId', 'OwnerUrl', 'OwnerSteamId', 'IconId') VALUES (?,?,?,?,?,?,?,?,?,?,?)'''

    # print(rows_data[0])
    # cursor.execute(command_insert_data, rows_data[0])
    # cursor.execute(command_insert_data, rows_data[1])
    # cursor.execute(command_insert_data, rows_data[2])
    # cursor.execute(command_insert_data, rows_data[3])
    # cursor.execute(command_insert_data, rows_data[4])
    # cursor.execute(command_insert_data, rows_data[5])

    for row_data in rows_data:
        try:
            cursor.execute(command_insert_data, row_data)
            print('Successfully Insert')
        except:
            e = sys.exc_info()[0]
            print('Insert error %s (in %s)' % (e, row_data))
            continue

    command_select_table = ''' SELECT * FROM items '''
    # SELECT * FROM fts WHERE fts MATCH ? ORDER BY bm25(fts)
    # Set up the ranking algorithm
    # SELECT item(Id, 2, '<b>', '</b>') FROM email WHERE email MATCH 'fts5'
    cursor.execute(command_select_table)
    result = cursor.fetchall()
    for re in result:
        print(re)


if __name__ == '__main__':
    main()

