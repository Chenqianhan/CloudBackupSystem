import os
import hashlib
import time
import DAO


class Scanner:
    def __init__(self, path, db):
        # Create a table id, which is also version_id
        table_id = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # father_path=os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+".")
        global data
        data = dict()

        #Check version
        if os.path.exists(os.getcwd()+"/version"):
            txt = open(os.getcwd()+"/version", 'r')
            last_version = txt.readline()
            txt.close()
            try:
                fobj = open(os.getcwd()+"/version", 'w')
                fobj.write(table_id)
                fobj.close()
            except IOError:
                print('*** version file open error:')
        else:
            try:
                fobj = open(os.getcwd()+"/version", 'w')
                fobj.write(table_id)
                fobj.close()
                last_version = "null"
            except IOError:
                print('*** version file open error:')

        dao = DAO.DAO(db)
        # dao.create_table(table_id)

        # Don't care the warning on last_version, that's bullshit
        # Whether is the first time
        if last_version is "null":
            print(last_version)
        else:
            res=dao.request_data(last_version)
            if len(res) < 1:
                return
            else:
                for row in res:
                    md = row[0]
                    filename_serverpath=[row[1], row[2]]
                    data[md] = filename_serverpath
            file_scanner(path, "")



def file_scanner(path, prefix):
    if not os.path.exists(path):
        raise FileNotFoundError('Path %s not exist' % path)

    if os.path.isfile(path):
        file_md5 = calMD5ForFile(path)
        if file_md5 in data:
            temp=data[file_md5]
            if os.path.basename(path) == temp[0]:
                # Working on it ..................................................................
        # Check
        # print(prefix+file_md5)
        # print(prefix+os.path.abspath(path))
        # print(os.path.basename(path))
        # file_extractor(os.path.abspath(path))
    elif os.path.isdir(path):
        # Check
        # print(prefix+os.path.abspath(path))
        folder_operation(path)
        for it in os.scandir(path):
            file_scanner(it, '---'+prefix)

# Dir cannot be input md5


# One function that judge whether the whole path is changed using md5
def file_operation(path):
    file_path = path
    file_name = os.path.basename(path)
    file_size= os.path.getsize(path)
    type = 'File'
    #print(file_name)
    #print(file_size)


def folder_operation(path):
    folder_path=path
    folder_name=os.path.basename(path)
    folder_size=os.path.getsize(path)
    type='Folder'
    #print(folder_name)
    #print(folder_size)


def calMD5ForFile(path):
    statinfo = os.stat(path)
    if int(statinfo.st_size)/(1024*1024) >= 1000 :
        print ("File size > 1000, move to big file...")
        return calMD5ForBigFile(path)
    m = hashlib.md5()
    f = open(path, 'rb')
    m.update(f.read())
    f.close()
    return m.hexdigest()


def calMD5ForBigFile(path):
    m = hashlib.md5()
    f = open(path, 'rb')
    buffer = 8192    # why is 8192 | 8192 is fast than 2048
    while 1:
        chunk = f.read(buffer)
        if not chunk : break
        m.update(chunk)
    f.close()
    return m.hexdigest()

