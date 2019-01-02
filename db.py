def listDifference(big, small):
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


def searchTable(pool, table, colsNamesInJson, sortBy='', order='', search=''):
    datas = []
    data = {}
    m = len(colsNamesInJson)
    #    try:
    database2 = pool.connection()
    database2.ping(reconnect=True)
    cursor2 = database2.cursor()
    database = pool.connection()
    database.ping(reconnect=True)
    cursor = database.cursor()
    if sortBy != '':
        if order != '':
            if (search != None) and (search != ';;'):
                searchxthc = []
                searchxkmk = []
                if search.split(';')[0] != '':
                    searchxthc = search.split(';')[0].split(' ')
                if search.split(';')[1] != '':
                    searchxkmk = search.split(';')[1].split(' ')
                if len(searchxkmk) != 0:
                    exe2str = "select name,studentid from student where name like "
                    for i in range(len(searchxkmk)):
                        if i == 0:
                            exe2str += " \"%%%s%%\"" % (searchxkmk[i])
                        else:
                            exe2str += " or name like \"%%%s%%\""
                    exe2str += ";"
                    cursor2.execute(exe2str)
                    results2 = cursor2.fetchall()
                    cursor2.close()
                    database2.close()
                    for i in range(len(results2)):
                        searchxthc.append(results2[i][1])
                exestr = "select * from %s order by %s %s where studentid like" % (table, sortBy, order)
                for i in range(len(searchxthc)):
                    if i == 0:
                        exestr += " \"%%%s%%\"" % (searchxthc[i])
                    else:
                        exestr += " or studentid like \"%%%s%%\"" % (searchxthc[i])
                exestr += ";"
                cursor.execute(exestr)
            else:
                cursor.execute("select * from %s order by %s %s;" % (table, sortBy, order))
        else:
            if (search != None) and (search != ';;'):
                searchxthc = []
                searchxkmk = []
                if search.split(';')[0] != '':
                    searchxthc = search.split(';')[0].split(' ')
                if search.split(';')[1] != '':
                    searchxkmk = search.split(';')[1].split(' ')
                if len(searchxkmk) != 0:
                    exe2str = "select name,studentid from student where name like "
                    for i in range(len(searchxkmk)):
                        if i == 0:
                            exe2str += " \"%%%s%%\"" % (searchxkmk[i])
                        else:
                            exe2str += " or name like \"%%%s%%\""
                    exe2str += ";"
                    cursor2.execute(exe2str)
                    results2 = cursor2.fetchall()
                    cursor2.close()
                    database2.close()
                    for i in range(len(results2)):
                        searchxthc.append(results2[i][1])
                exestr = "select * from %s order by %s %s where studentid like" % (table, sortBy)
                for i in range(len(searchxthc)):
                    if i == 0:
                        exestr += " \"%%%s%%\"" % (searchxthc[i])
                    else:
                        exestr += " or studentid like \"%%%s%%\"" % (searchxthc[i])
                exestr += ";"
                cursor.execute(exestr)
            else:
                cursor.execute("select * from %s order by %s asc;" % (table, sortBy))
    else:
        if (search != None) and (search != ';;'):
            searchxthc = []
            searchxkmk = []
            if search.split(';')[0] != '':
                searchxthc = search.split(';')[0].split(' ')
            if search.split(';')[1] != '':
                searchxkmk = search.split(';')[1].split(' ')
            if len(searchxkmk) != 0:
                exe2str = "select name,studentid from student where name like "
                for i in range(len(searchxkmk)):
                    if i == 0:
                        exe2str += " \"%%%s%%\"" % (searchxkmk[i])
                    else:
                        exe2str += " or name like \"%%%s%%\""
                exe2str += ";"
                cursor2.execute(exe2str)
                results2 = cursor2.fetchall()
                cursor2.close()
                database2.close()
                for i in range(len(results2)):
                    searchxthc.append(results2[i][1])
            exestr = "select * from %s where studentid like" % (table)
            for i in range(len(searchxthc)):
                if i == 0:
                    exestr += " \"%%%s%%\"" % (searchxthc[i])
                else:
                    exestr += " or studentid like \"%%%s%%\"" % (searchxthc[i])
            exestr += ";"
            cursor.execute(exestr)
        else:
            cursor.execute("select * from %s ;" % (table))
    results = list(cursor.fetchall())
    cursor.close()
    database.close()
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
    # except:
    #   tt = []
    #   for i in range(m):
    #       tt.append('(>_<)')
    #   results.append(tuple(tt))
    #   for i in range(len(results)):
    #       for j in range(m):
    #           data[colsNamesInJson[j]] = results[i][j]
    #       datas.append(data.copy())
    #   return datas

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


def deletekeys(pool, tableName, keys, keystnjm):
    str = "delete from %s where %s=%s" % (tableName, keys, keystnjm)
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
