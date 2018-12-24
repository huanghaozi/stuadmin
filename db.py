def listDifference(big, small):
    k = ''
    ks = []
    for k in big:
        if not k in small:
            ks.append(k)
    return ks.copy()

def getTable(pool, table, colsNamesInJson, sortBy='', order='', search=''):
    datas = []
    data = {}
    results = []
    m = len(colsNamesInJson)
    try:
        database = pool.connection()
        database.ping(reconnect=True)
        cursor = database.cursor()
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
        if search != None:
            notinSearch = []
            for i in range(len(results)):
                counts = 0
                for j in range(len(results[i])):
                    if str(results[i][j]).find(search) == -1:
                        counts += 1
                    if counts == len(results[i]):
                        notinSearch.append(results[i])
            results = listDifference(results, notinSearch)
        if not results:
            tt = []
            for i in range(m):
                tt.append('╮(－_－)╭')
            results.append(tuple(tt))
        for i in range(len(results)):
            for j in range(m):
                data[colsNamesInJson[j]] = results[i][j]
            datas.append(data.copy())
        return datas
    except:
        tt = []
        for i in range(m):
            tt.append('(>_<)')
        results.append(tuple(tt))
        for i in range(len(results)):
            for j in range(m):
                data[colsNamesInJson[j]] = results[i][j]
            datas.append(data.copy())
        return datas

def insertTable(pool, tablesAndcols, values):
    str = "insert into %s value %s" % (tablesAndcols, values)
    try:
        database = pool.connection()
        database.ping(reconnect=True)
        cursor = database.cursor()
    except:
        return False
    try:
        cursor.execute(str)
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        database.rollback()
        return False


def modifyTable(pool, tableName, setDatas, pjdrtnjm):
    str = "update %s set %s where %s;" % (tableName, setDatas, pjdrtnjm)
    try:
        database = pool.connection()
        database.ping(reconnect=True)
        cursor = database.cursor()
    except:
        return False
    try:
        cursor.execute(str)
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        database.rollback()
        return False
