import mysql.connector
from mysql.connector import Error
from sshtunnel import SSHTunnelForwarder


class DbCommand:
    # SSH VARIABLES
    ssh_host = '35.192.36.86'
    ssh_username = 'root'
    ssh_psw = 'Yt2G9d4aGMrRgwhm'
    localhost = '127.0.0.1'
    port = 3306

    # Define whether a ssh conn must be estabilished or it'll run over a non-ssh environment
    # For 'non-ssh' env, set it to 'False'
    run_ssh = True

    # PRD SERVER
    config = {
        'user': 'root',
        'password': 'sosidb',
        'host': localhost,
        'port': 3306,
        'database': 'sys',
        'raise_on_warnings': True  # Can't touch this
    }

    # LOCAL DB
    # config = {
    #     'user': 'sosi',
    #     'password': 'sosidb',
    #     'host': '127.0.0.1',
    #     'port': 3306
    #     'database': 'sys',
    #     'raise_on_warnings': True # Can't touch this
    # }

    def __getSSHConnection(self):
        with SSHTunnelForwarder(
            (self.ssh_host, 22),
            ssh_username=self.ssh_username,
            ssh_password=self.ssh_psw,
            remote_bind_address=(self.localhost, self.port)
        ) as server:
            return server

    def __getConnection(self):
        ssh_server = None

        if self.run_ssh:
            ssh_server = self.__getSSHConnection()

        if ('port' in self.config) and (ssh_server is not None) and (ssh_server.is_active) and (ssh_server.is_alive):
            self.config['port'] = ssh_server.local_bind_port
        else:
            self.config['port'] = 3306

        return mysql.connector.connect(**self.config)

    def Commit(self, strCommand):
        try:
            conn = self.__getConnection()
            if conn.is_connected():
                cursor = conn.cursor()
                rowsAffected = cursor.execute(strCommand)

                conn.commit()
        except Error as e:
            print(e + ' - ' + strCommand)
        finally:
            cursor.close()
            conn.close()
            return True

    def CallProcedure(self, strCommand, args):
        try:
            conn = self.__getConnection()

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.callproc(strCommand, args)

                return True
            return False
        except Error as e:
            print(e)
            pass
        finally:
            cursor.close()
            conn.close()
            pass

    def Query(self, strCommand):
        try:
            returnObj = tuple
            conn = self.__getConnection()

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(strCommand)
                returnObj = cursor.fetchone()
        except Error as e:
            print(e)
            pass
        finally:
            cursor.close()
            conn.close()

            return returnObj
