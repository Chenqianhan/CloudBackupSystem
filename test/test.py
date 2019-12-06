import DAO
import os
dao = DAO.DAO('test')
table_id='20191206020726'
#table_id = '%s' % id
#dao.test_sql('Begin')
#dao.upload_data(table_id, 'file_path_client', 'file_path_server000', 'file_size1111',
 #               'file_type', 'filename1', 'md5_code', 'False')
#path = "/home/parallels/Pictures"

#dao.upload_data(table_id, path, 'path_depends111111', os.path.getsize(path), 'Folder',
 #               os.path.basename(path), 'null', 'False')
#dao.test_sql('Commit')
#print("insert successfully")
res = dao.request_data('20191206020726', 'test')
print(res)