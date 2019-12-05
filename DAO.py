import pymysql


class DAO:
    def __init__(self, db):
        try:
            conn = pymysql.connect(host='35.223.248.16', user='cqh', passwd='CAMRYLOVESEDGE', db=db, port=3306)
            cur = conn.cursor()
        except:
            print("Fail to connect database")
        global cur

        #sql = "select * from test.20191204220814"
        #cur.execute(sql)
        # rows = cur.fetchall()
        # print(rows)

    def disconnect(self):
        cur.close()

    def create_table(self, table_id):
        sql = "CREATE TABLE test."+table_id+\
              "(ID INT PRIMARY KEY AUTO_INCREMENT, " \
              "filePath_Client VARCHAR(100), " \
              "filePath_Server VARCHAR(100), " \
              "fileSize VARCHAR(50), " \
              "fileType VARCHAR(30), " \
              "fileName VARCHAR(100), " \
              "MD5 VARCHAR(200), " \
              "isExist_LastB boolean, " \
              "isBp_Complete boolean )"

        # print(sql)
        try:
            cur.execute(sql)
        except:
            print("Couldn't create a new version")

        print("Create table successfully")

    def request_data(self, last_version):
        try:
            sql = "select MD5, fileName, filePath_Server from test."+last_version
            cur.execute(sql)
            res = cur.fetchall()
        except:
            print("Couldn't request record from server")
            return

        return res

    def upload_data(self, table_id, file_path_client, file_path_server, file_size, file_type, filename, md5_code, is_exist):
        sql="INSERT INTO "
        # Working on it .........................................
