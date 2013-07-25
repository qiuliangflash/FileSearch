import os
import sqlite3
import osBase
def initLog(count):
    import logging
    import sys
    logger = logging.getLogger()
    formatter = logging.Formatter('%(message)s')
    file_handler = logging.FileHandler("fileNotify_%d.log" % count)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.NOTSET)
    return logger
   
def initDB(disk):
    conn = sqlite3.connect('FilePathTree_%s' % disk)
    conn.text_factory = str  
    DBhandle = conn.cursor()
    return [conn, DBhandle]

def insertFileTable(DBhandle, tableName, currentId, previousId, fileName):
    if '\'' in fileName:
        DBhandle.execute("insert into %s values(%s, %s,\"%s\")" % (tableName, currentId, previousId, fileName ))
    else:
        DBhandle.execute("insert into %s values(%s, %s,'%s')" % (tableName, currentId, previousId, fileName ))

def deleteFileTable(DBhandle, tableName, fileName):
    if '\'' in fileName:
        DBhandle.execute("delete from %s where FileName = \"%s\"" % (tableName, fileName))
    else:
        DBhandle.execute("delete from %s where FileName = '%s'" % (tableName, fileName))

def insertAbsolutePathToFileTable(DBhandle, tableCount, filePath):
    dirName = osBase.getDirName(filePath)
    globalTableCount = getFileTableCount(filePath[0])

    if globalTableCount < tableCount:
        setFileTableCount(tableCount)
        DBhandle.execute("create table %s (CurrentId INTEGER, PreviousId INTEGER, FileName text)" % "filepath_"+str(tableCount))
        storeCurrentId = 1
    else:
        DBhandle.execute("select max(CurrentId) from %s" % "filepath_"+str(tableCount))
        result =DBhandle.fetchall()
        storeCurrentId = result[0][0] + 1
    
    baseName = osBase.getBaseName(dirName)
    
    if '\'' in baseName:
        DBhandle.execute("select * from %s where FileName = \"%s\"" % ("filepath_"+str(tableCount-1), baseName))
    else:
        DBhandle.execute("select * from %s where FileName = '%s'" % ("filepath_"+str(tableCount-1), baseName))
    result = DBhandle.fetchall()
    if len(result) == 0:
        return
    if tableCount == 2:
        return insertFileTable(DBhandle, "filepath_"+str(tableCount),storeCurrentId, result[0][0], osBase.getBaseName(filePath))
    
    dirName = osBase.getDirName(dirName)
    for i in range(len(result)):
        count = 0
        previousId = result[i][0]
        tableList = range(tableCount -1)
        tableList.reverse()
        for j in tableList:
            DBhandle.execute("select * from % s where CurrentId = %d" % ("filepath_"+str(j+1), result[i][0]))
            newResult = DBhandle.fetchall()
            if newResult[0][2] != osBase.getBaseName(dirName):
                break
            else:
                count += 1
                previousId = newResult[0][1]
                dirName = osBase.getDirName(dirName)
        if count == tableCount - 1:
            previousId = result[i][0]
            break
    insertFileTable(DBhandle, "filepath_"+str(tableCount), storeCurrentId, previousId, os.path.basename(filePath) )
            
            
def deleteAbsolutePathFromFileTable(DBhandle, tableCount, fileName):
    baseName = osBase.getBaseName(fileName)
    dirName = osBase.getDirName(fileName)
    if '\'' in fileName:
        DBhandle.execute("select * from %s where FileName = \"%s\"" % ("filepath_"+str(tableCount), baseName))
    else:
        DBhandle.execute("select * from %s where FileName = '%s'" % ("filepath_"+str(tableCount), baseName))
    result = DBhandle.fetchall()
    if len(result) == 0:
        return

    for i in range(len(result)):
        matchCount = 0
        previousId = result[i][1]
        list = range(tableCount - 1)
        list.reverse()
        for j in list:
            DBhandle.execute("select * from %s where CurrentId = %d" % ("filepath_" + str(j+1), previousId))
            searchResult = DBhandle.fetchall()
            if len(searchResult) > 0 and osBase.getBaseName(dirName) == searchResult[0][2]:
                matchCount += 1
                previousId = searchResult[0][1]
                dirName = osBase.getDirName(dirName)
            else:
                break
        if matchCount == tableCount - 1:
            DBhandle.execute("delete from %s where CurrentId = '%s'" % ("filepath_"+str(tableCount), result[i][0]))
            break
            
   
def operatorCommit(conn):
    conn.commit()
    
def getFileTableCount(disk):
    conn = sqlite3.connect("FileConf")
    conn.text_factory = str
    DBhandle = conn.cursor()
    DBhandle.execute(" select * from sqlite_master where type ='table' and name = 'fileTableCount'")
    result =DBhandle.fetchall()
    if len(result) == 0:
        closeDB([conn,DBhandle])
        return None
    DBhandle.execute("select count from fileTableCount where disk = '%s'" % disk)
    result = DBhandle.fetchall()
    closeDB([conn,DBhandle])
    if len(result) > 0:
        return result[0][0]
    return None
    
def setFileTableCount(disk, count):
    conn = sqlite3.connect("FileConf")
    DBhandle = conn.cursor()
    DBhandle.execute("create table if not exists fileTableCount (disk text, count INTEGER)")
    DBhandle.execute("insert into fileTableCount values('%s', %d)" % (disk, count))
    conn.commit()
    closeDB([conn,DBhandle])

def insertBackupTable(handle, id, folder):
    if '\'' in folder:
        handle.execute("insert into BackupTable values(%d, \"%s\")" % (id, folder))
    else:
        handle.execute("insert into BackupTable values(%d, '%s')" % (id, folder))
    
def getLastBackupFolder(handle):
    handle.execute("select max(id) from BackupTable")
    result = handle.fetchall()
    
    if len(result) > 0:
        return result[0][0]
    else:
        return None

def initBackupDB():
    conn = sqlite3.connect("FileConf")
    conn.text_factory = str  
    DBhandle = conn.cursor()
    DBhandle.execute("create table BackupTable (id INTEGER, folder text)")
    return [conn, DBhandle]

def closeDB(handle):
    handle[1].close()
    handle[0].close()
    
#file table is "filepath_%d"
def getFileFromDBUsingFileName(dirText, fileName):
    count = getFileTableCount(dirText)
    handle = initDB(dirText)
    listCount = range(count)
    listCount.reverse()
    filePath = []
    for i in listCount:
        handle[1].execute("select * from %s where FileName like '%%%s%%'" % ("filepath_"+str(i+1), fileName))
        result = handle[1].fetchall()
        for j in range(len(result)):
            path = getFileFromDBUsingPreviousId(result[j][1], i, result[j][2], handle)
            if path != None:
                filePath.append((result[j][2], path))
    closeDB(handle)
    return filePath

def getFileFromDBUsingPreviousId(currentId, tableIndex, fileName, handle):
    if tableIndex == 0:
        return fileName[2] + "\\"
    listCount = range(tableIndex)
    listCount.reverse()
    for i in listCount:
        handle[1].execute("select * from %s where CurrentId = %d" % ("filepath_"+str(i+1), currentId))
        result = handle[1].fetchall()
        path = result[0][2] +"\\" + fileName
        currentId = result[0][1]
        fileName = path        
    return path
    