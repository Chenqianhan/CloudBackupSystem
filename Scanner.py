import os
import hashlib
import time
import DAO


class Scanner:
    def __init__(self, path, db):
        global dao
        global table_id
        # Create a table id, which is also version_id
        # If not convert table_id into string, it's gonna export error
        id = time.strftime("%Y%m%d%H%M%S", time.localtime())
        table_id = '%s' % id
        # father_path=os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+".")
        # data -> 'md5',[filename, server_path]
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
        dao.create_table(table_id)

        # Don't care the warning on last_version, that's bullshit
        # Whether is the first time
        dao.execute_sql('Begin')
        if last_version is "null":
            print('Start scanning')
            file_scanner_initial(path, "")
            print('Scanner completed')
        else:
            res = dao.request_data(last_version, db)
            if len(res) < 1:
                print('Start scanning')
                file_scanner_initial(path, "")
                print('Scanner completed')
            else:
                for row in res:
                    md = row[0]
                    filename_serverpath=[row[1], row[2]]
                    data[md] = filename_serverpath
                print('Start scanning')
                file_scanner(path, "", data)
                print('Scanner completed')

        dao.execute_sql('Commit')
        dao.disconnect()


def file_scanner(path, prefix, data):
    if not os.path.exists(path):
        raise FileNotFoundError('Path %s not exist' % path)
    if os.path.isfile(path):
        file_md5 = calMD5ForFile(path)
        if file_md5 in data:
            temp = data[file_md5]
            # If exists
            if os.path.basename(path) == temp[0]:
                # Working on it ..................................................................
                dao.upload_data(table_id, path, temp[1], os.path.getsize(path), 'File',
                                os.path.basename(path), file_md5, 'True')
            # If names don't match but md5 match, it's probably md5 coincidence, or mostly name modification
            else:
                # server path generator()
                dao.upload_data(table_id, path, 'path depends', os.path.getsize(path), 'File',
                                os.path.basename(path), file_md5, 'False')
                # FTP operation(), upload file
                # Then update this by isBp_completed = True
        else:
            # When it's a new or modified file
            # server path generator()
            dao.upload_data(table_id, path, 'path depends', os.path.getsize(path), 'File',
                            os.path.basename(path), file_md5, 'False')
            # FTP operation(), upload file
            # Then update this by isBp_completed = True

        # Check
        # print(prefix+file_md5)
        # print(prefix+os.path.abspath(path))
        # print(os.path.basename(path))
        # file_extractor(os.path.abspath(path))
    elif os.path.isdir(path):
        # Check gen
        # server path generator
        dao.upload_data(table_id, path, 'path depends', os.path.getsize(path), 'Folder',
                        os.path.basename(path), 'null', 'False')
        # FTP operation(), if not exist: create a folder on server.
        # Then update this by isBp_completed
        for it in os.scandir(path):
            file_scanner(it, '---'+prefix, data)


def file_scanner_initial(path, prefix):
    if not os.path.exists(path):
        raise FileNotFoundError('Path %s not exist' % path)
    if os.path.isfile(path):
        file_md5 = calMD5ForFile(path)
        # server path generator
        dao.upload_data(table_id, path, 'path_depends', os.path.getsize(path), 'File',
                        os.path.basename(path), file_md5, 'False')
        # FTP operation()
        # Update is
    elif os.path.isdir(path):
        # server path generator
        dao.upload_data(table_id, path, 'path_depends', os.path.getsize(path), 'Folder',
                        os.path.basename(path), 'null', 'False')
        # FTP operation(), if not exist: create a folder on server.
        # Then update this by isBp_completed
        for it in os.scandir(path):
            file_scanner_initial(it, '---'+prefix)

# Dir cannot be input md5


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

