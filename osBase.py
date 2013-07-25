import os
import win32file

def getDirName(fileName):
    if fileName[-1] == ":" and "\\" not in fileName:
        return ""
    result = os.path.dirname(fileName)
    if result[-1] == "\\":
        return result[:-1]
    return result
    
def getBaseName(fileName):
    result =os.path.basename(fileName)
    if result == "":
        return fileName
    return result
        
def getDiskDriver():
    drives=[]
    sign=win32file.GetLogicalDrives()
    drive_all=["A:\\","B:\\","C:\\","D:\\","E:\\","F:\\","G:\\","H:\\","I:\\","J:\\","K:\\","L:\\","M:\\","N:\\","O:\\","P:\\","Q:\\","R:\\","S:\\","T:\\","U:\\","V:\\","W:\\","X:\\","Y:\\","Z:\\"]
    for i in range(25):
        if (sign & 1<<i):
            drives.append(drive_all[i])
    return drives