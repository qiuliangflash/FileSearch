

import os 

import win32file 
import win32con
import DB
from threading import Thread  

import osBase

class DiskNotify(Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, disk):
        Thread.__init__(self)
        self.disk = disk
        self.flag = True
 
    def run(self): #Overwrite run() method, put what you want the thread do here
        self.fileNotifyForDisk()
            
    def stop(self):
        self.flag = False
    
    def fileNotifyForDisk(self):
        hDir= win32file.CreateFile ( 
                                self.disk, 
                                FILE_LIST_DIRECTORY, 
                                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, 
                                None, 
                                win32con.OPEN_EXISTING, 
                                win32con.FILE_FLAG_BACKUP_SEMANTICS, 
                                None 
                                 )  
        while self.flag: 
            results = win32file.ReadDirectoryChangesW (hDir, 65536, True, 
                                               win32con.FILE_NOTIFY_CHANGE_FILE_NAME | 
                                               win32con.FILE_NOTIFY_CHANGE_DIR_NAME ,
                                               None, None) 
            print self.disk
            for action, file in results: 
                full_filename = os.path.join (self.disk, file)
                print full_filename + "%%%%%%" + str(action)
            
        
def storeToFileTable(DBhandle, memStore):
    for i in range(len(memStore)):
        dbAction(DBhandle, memStore[i][0], memStore[i][1])
    DB.operatorCommit(DBhandle[0])
    
def dbAction(DBhandle, filename, action):
    splitFile = filename.split("\\")
    if splitFile[-1] == "\\":
        tableCount = len(splitFile) - 1
    else:
        tableCount = len(splitFile)
        
    if action == CREATED or action == RENAMED_TO_SOMETHING:
        DB.insertAbsolutePathToFileTable(DBhandle[1], tableCount, filename)
    if action == DELETED or action == RENAMED_FROM_SOMETHING:
        DB.deleteAbsolutePathFromFileTable(DBhandle[1], tableCount, filename)
                
FILE_LIST_DIRECTORY = 0x0001 
CREATED = 0x1
DELETED = 0x2
RENAMED_FROM_SOMETHING = 0x4
RENAMED_TO_SOMETHING = 0x5

#logIndex = 0
#names = locals()
#names["memStore_1"] = []

diskStore = []
#logger = DB.initLog(logIndex)
DBhandle = DB.initDB()      

path_to_watch = osBase.getDiskDriver()

for path in path_to_watch:
    if os.path.exists(path):
        diskNotify = DiskNotify(path)
        diskNotify.start()


#thread.start_new_thread(storeToFileTable, (DBhandle[1], names["memStore_%d" % (logIndex-1)]))

    #logIndex = 1
     #logger = DB.initLog(logIndex)
     #thread.start_new_thread(storeToFileTable, (DBhandle[1], names["memStore_%d" % (logIndex-1)]))
#                print full_filename + "%%%%%%" + str(action)
#     names["memStore_1"].append((full_filename,str(action)))
#     logger.info((full_filename,str(action)))
        
        #storeAction = [(full_filename, action)]
        #storeToFileTable(DBhandle,storeAction )