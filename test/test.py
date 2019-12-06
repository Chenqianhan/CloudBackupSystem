import DAO

dao = DAO.DAO('test')
dao.upload_data('20191205163717', 'file_path_client', 'file_path_server', 'file_size',
                'file_type', 'filename', 'md5_code', 'False')
print("insert successfully")