import Database


def autoComplete():
    Database.dataBaseSetUp()

    command_select_table = ('''SELECT   Name, 
                                        CustomName
                                FROM items''')

    Database.cursor.execute(command_select_table)
    autodata = Database.cursor.fetchall()

    return autodata
