class Item:
    ID = None
    filePath_Client = None
    filePath_Server = None
    fileSize = None
    fileType = None
    fileName = None
    MD5 = None
    isExist_LastB = None
    isBp_Complete = None

    def __init__(self, ID, filePath_Client, filePath_Server, fileSize, fileType, fileName, MD5, isExist_LastB,
                 isBp_Complete):
        self.ID = ID
        self.filePath_Client = filePath_Client
        self.filePath_Server = filePath_Server
        self.fileSize = fileSize
        self.fileType = fileType
        self.fileName = fileName
        self.MD5 = MD5
        self.isExist_LastB = isExist_LastB
        self.isBp_Complete = isBp_Complete

    def print(obj):
        "打印对象的所有属性"
        print(obj.__dict__)

# fileA = Item("001", "/desktop", "/20191204220814/desktop/readme.txt", "1206", "txt", "readme.txt", "qwertyuiopasdfghjkl", False, True)
# fileA.print()
# folderA = Item("002", "/desktop", "/20191204220814/desktop/folderA", "25374", "folder", "folderA", "mnbvcxzlkjhgfdsa", False, True)
# folderA.print()


class User:
    self.userID = None
    self.userName = None
    self.passwordMD5 = None
    self.useRootPathAtServer = None
    self.userDatabaseName = None

    def __init__(self, userID, userName, passwordMD5, useRootPathAtServer, userDatabaseName):
        self.userID = userID
        self.userName = userName
        self.passwordMD5 = passwordMD5
        self.useRootPathAtServer = useRootPathAtServer
        self.userDatabaseName = userDatabaseName

# curr_user = User(1, "Alice", "aldskfj23lkhagd", "/home/dataspace/1", 1)


class Backup:
    self.backupID = None
    self.backupTime = None
    self.backupFolderName = None
    self.backupDBTableName = None

    def __init__(self, backupID, backupTime, backupFolderName, backupDBTableName):
        self.backupID = backupID
        self.backupTime = backupTime
        self.backupFolderName = backupFolderName
        self.backupDBTableName = backupDBTableName


class DatabaseController:
    def __init__(self):
        pass

    def connect_database(self):
        try:
            global connection
            connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE',
                                         db=curr_user.userDatabaseName, port=3306)
            cursor = connection.cursor()
        except:
            print("Fail to connect database")
        return cursor

    def disconnect_database(self):
        connection.close()







