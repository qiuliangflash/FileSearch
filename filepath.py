import sqlite3
import os
import DB
import osBase
from threading import Thread  


class DiskFileStore(Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, disk):
        Thread.__init__(self)
        self.disk = disk
 
    def run(self): #Overwrite run() method, put what you want the thread do here
        fileDirectory = []
        fileDirectory.append((self.disk, 1,0)) 
        handle = DB.initDB(self.disk[0:1])
        maxCount = self.getSubfolder(handle, fileDirectory)
        print maxCount
        DB.setFileTableCount(self.disk[0:1], maxCount)
        DB.closeDB(handle)
    
    def getSubfolder(self, handle, fileDirectory):               
        conn = handle[0]
        DBhandle = handle[1]
        number = 0
        count = 0  
        maxCount = 1
        #backupCount = 0
        #backupTableHandle = DB.initBackupDB()
    
        while len(fileDirectory) > 0:
            if os.path.exists(fileDirectory[0][0]) == False:
                fileDirectory.pop(0)
                continue
            if fileDirectory[0][1] != count:
                if fileDirectory[0][1] > maxCount:
                    maxCount = fileDirectory[0][1]
                number = 0
                tableName = "filepath_%d" % fileDirectory[0][1]
                DBhandle.execute('''create table if not exists %s (CurrentId INTEGER, PreviousId INTEGER, FileName text)''' % tableName)
                count = fileDirectory[0][1]
            folder = fileDirectory[0][0]
            if folder[-1] == "\\":
                baseName = folder.split("\\")[0]
            else:
                baseName = os.path.basename(folder)
            number += 1
            DB.insertFileTable (DBhandle, tableName, number, fileDirectory[0][2], baseName)
            #if backupCount%5000 == 0 and backupCount != 0:
            #    DB.insertBackupTable(backupTableHandle[1],backupCount/5000, folder)
            #backupCount += 1
            #DB.operatorCommit(backupTableHandle[0])
            DB.operatorCommit(conn)
            if os.path.isdir(folder):
                try:
                    for subFolder in os.listdir(folder):
                        if folder[-1] != '\\':
                            fileDirectory.append((folder + '\\' + subFolder, fileDirectory[0][1]+1, number))
                        else:
                            fileDirectory.append((folder + subFolder, fileDirectory[0][1]+1, number))
                except Exception as e:
                    pass
            fileDirectory.pop(0)
        #DB.closeDB(backupTableHandle)    
        return maxCount
            
     
              
diskList = ["F:\\","G:\\","H:\\"]

for disk in diskList:
    if os.path.exists(disk) == True:       
        diskFileStore = DiskFileStore(disk)
        diskFileStore.start()
# rec = c.execute('''select * from %s''' % table_name)
# conn.text_factory = str
# 
# print c.fetchall()
