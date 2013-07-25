# coding=gbk

import DB
import sqlite3
import os
import osBase

path_to_watch = osBase.getDiskDriver()
print path_to_watch
#
#handle = DB.initDB()
#
#handle[1].execute("select * from filepath_1")
#print handle[1].fetchall()
#
#handle[1].execute("select * from filepath_2")
#print handle[1].fetchall()
#
#handle[1].execute("select * from filepath_3")
#print handle[1].fetchall()
#
#handle[1].execute("select * from filepath_4")
#print handle[1].fetchall()
#
#handle[1].execute("select * from filepath_5")
#print handle[1].fetchall()
#
#handle[1].execute("select * from filepath_6")
#print handle[1].fetchall()
#
#
##handle[1].execute("select PreviousId from filepath_3 where FileName = 'H:\\S2M-039 STAGE 2 MEDIA 強作再現 Encore Vol.39 宮瀬リコRiko~8頭身之極上淫尻初登場\\S2M-039.jpg'")
#
print DB.getFileTableCount()
#handle = sqlite3.connect("FileConf")
#c = handle.cursor()
#c.execute("select * from BackupTable")
#print c.fetchall()



