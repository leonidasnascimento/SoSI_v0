import mysql.connector
from mysql.connector import Error

class DbCommand:
    def Save(self, strCommand):
        try:
            conn = mysql.connector.connect(host='127.0.0.1',
                                       database='sys',
                                       user='sosi',
                                       password='sosidb')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(strCommand)
                
                conn.commit()
                
                return True
        except Error as e:
            print(e)
            pass
        finally:
            cursor.close()
            conn.close()
            pass
    
    def Update(self, strCommand):
        return True
    
    def Select(self, strCommand):
        return object
