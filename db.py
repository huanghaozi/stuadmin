def getTable(pool, table, colsNamesInJson, sortBy='', order=''):
    try:
        database = pool.connection()
        database.ping(reconnect=True)
        cursor = database.cursor()
        datas = []
        data = {}
        m = len(colsNamesInJson)
        if sortBy != '':
            if order != '':
                cursor.execute("select * from %s order by %s %s;" % (table, sortBy, order))
            else:
                cursor.execute("select * from %s order by %s asc;" % (table, sortBy))
        else:
            cursor.execute("select * from %s;" % (table))
        results = cursor.fetchall()
        cursor.close()
        database.close()
        if not results:
            return {'Empty': True}
        for i in range(len(results)):
            for j in range(m):
                data[colsNamesInJson[j]] = results[i][j]
            datas.append(data.copy())
        return datas
    except:
        return [{'Error': True}]


def insertTable(pool, tablesAndcols, values):
    try:
        database = pool.connection()
        database.ping(reconnect=True)
        cursor = database.cursor()
        cursor.execute("insert into %s value %s" % (tablesAndcols, values))
        cursor.close()
        database.close()
        return True
    except:
        return False
