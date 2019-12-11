import os
from mysql.connector import Error, errorcode
from db_connection.db_connection import ConnectionPool
from configparser import ConfigParser


class DBInitService:

    OPTION = """
    CHARACTER SET 'UTF8'
    FIELDS TERMINATED by ','
    LINES TERMINATED by '\r\n'
    """
    source_dir = "/home/n9646/PycharmProjects/coffee_setting/data/"

    def __init__(self):
        self._db = DBInitService.read_ddl_file()

    @classmethod
    def read_ddl_file(cls, filename="database_setting/coffee_ddl.ini"):
        parser = ConfigParser()
        parser.read(filename, encoding='UTF8')

        db = {}
        for sec in parser.sections():
            items = parser.items(sec)
            if sec == 'name':
                for key, value in items:
                    db[key] = value
            if sec == 'sql':
                sql = {}
                for key, value in items:
                    sql[key] = " ".join(value.splitlines())
                db['sql'] = sql
            if sec == 'user':
                for key, value in items:
                    db[key] = value

        return db

    def __create_database(self):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self._db['database_name']))
            print("CREATE DATABASE {}".format(self._db['database_name']))
        except Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                cursor.execute("DROP DATABASE {}".format(self._db['database_name']))
                print("DROP DATABASE {}".format(self._db['database_name']))
                cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self._db['database_name']))
                print("CREATE DATABASE {}".format(self._db['database_name']))
            else:
                print(err.msg)
        finally:
            cursor.close()
            conn.close()

    def __create_table(self):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute("USE {}".format(self._db['database_name']))
            for table_name, table_sql in self._db['sql'].items():
                try:
                    print("Creating TABLE {}: ".format(table_name), end='')
                    cursor.execute(table_sql)
                except Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                    else:
                        print(err.msg)
                else:
                    print('OK.')
        except Error as err:
            print(err.msg)
        finally:
            cursor.close()
            conn.close()

    def __create_user(self):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            print("Creating USER: ", end='')
            cursor.execute(self._db['user_sql'])
            print("OK.")
        except Error as err:
            print(err.msg)
        finally:
            cursor.close()
            conn.close()

    def data_backup(self, table_name):
        filename = table_name + '.txt'
        print(filename)
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            source_path = self.source_dir + filename
            cursor.execute("USE coffee")
            print('use coffee')
            if os.path.exists(source_path):
                os.remove(source_path)
            backup_sql = "SELECT * FROM {} INTO OUTFILE '{}' {}".format(table_name, source_path, DBInitService.OPTION)
            cursor.execute(backup_sql)

            if not os.path.exists(self.source_dir):
                os.makedirs(os.path.join('data'))
            print(table_name, "backup complete!")
        except Error as err:
            print(err)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def data_restore(self, table_name):
        filename = table_name + '.txt'
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            data_path = self.source_dir + filename
            cursor.execute("USE coffee")
            if os.path.exists(data_path):
                re_sql = "LOAD DATA INFILE '{}' INTO TABLE {} {}".format(data_path, table_name, DBInitService.OPTION)
                cursor.execute(re_sql)
                print(table_name, "restore complete!")
                conn.commit()
        except Error as err:
            print(err)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def database_init_service(self):
        self.__create_database()
        self.__create_table()
        self.__create_user()