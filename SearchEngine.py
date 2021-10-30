import Database


def querySearch(query):
    # query will be collect from search engine bar
    # Id, Name, CustomName, Quality, Description, ItemHeader, Class, WikiId, OwnerUrl, OwnerSteamId, IconId
    # ranking by bm25

    # command_select_table = (''' SELECT * FROM items WHERE items MATCH '%s' ORDER BY bm25(items)''' % query)
    # regular search regular ranking
    # command_select_table = (''' SELECT * FROM items WHERE items MATCH '%s' ORDER BY rank ''' % query)

    # SELECT * FROM fts WHERE fts MATCH ? ORDER BY bm25(fts)
    # Set up the ranking algorithm

    # command_select_table = ('''SELECT   highlight(items,0, '<b>', '</b>')Name,
    #                                     highlight(items,1, '<b>', '</b>')CustomName,
    #                                     highlight(items,2, '<b>', '</b><br>')Description,
    #                                     *
    #                             FROM items
    #                             WHERE items MATCH '%s'
    #                             ORDER BY rank)
    #                             ''' % query)

    Database.dataBaseSetUp()

    command_select_table = ('''SELECT   highlight(items,0, '<b>', '</b>')Name, 
                                        highlight(items,1, '<b>', '</b>')CustomName,
                                        highlight(items,2, '<b>', '</b>')Quality,
                                        highlight(items,3, '<b>', '</b>')Description, 
                                        highlight(items,4, '<b>', '</b>')ItemHeader, 
                                        highlight(items,5, '<b>', '</b><br>')Class,
                                        WikiId, OwnerUrl, OwnerSteamId, IconId 
                                FROM items
                                WHERE items MATCH '%s' 
                                ORDER BY bm25(items)
                                ''' % query)

    Database.cursor.execute(command_select_table)
    result = Database.cursor.fetchall()

    return result
