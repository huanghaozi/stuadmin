def gettable(database, table, colsNamesInJson):
    try:
        database.ping(reconnect=True)
        cursor = database.cursor()
        datas = []
        data = {}
        m = len(colsNamesInJson)
        cursor.execute("select * from %s;" % (table))
        results = cursor.fetchall()
        cursor.close()
        if not results:
            return {'Empty': True}
        for i in range(len(results)):
            for j in range(m):
                data[colsNamesInJson[j]] = results[i][j]
            datas.append(data)
        return datas
    except:
        return [{'Error': True}]


def settable(database, table, coldname, value):
