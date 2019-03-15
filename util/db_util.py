from typing import List, Dict, Tuple
from warnings import warn
from getpass import getpass
import MySQLdb as sql
import MySQLdb.connections as connections


class DatabaseHandle:
    connection = connections.Connection
    cursor = connections.cursors.Cursor
    user: str = None
    host: str = None
    db: str = None
    meta_table: str = None

    def __init__(self, params: Dict[str, str] = None, handle=None):
        if isinstance(handle, self.__class__):
            self = handle

        if isinstance(params, dict):
            try:
                self.connection = sql.connect(user=params['user'],
                                              password=params['password'],
                                              db=params['db'], host=params['host'])
                self.cursor = self.connection.cursor()
                self.user = params['user']
                self.host = params['host']
                self.db = params['db']
            except sql._exceptions.DatabaseError:
                # Creating the database that didn't exist, if that was the error above
                connection: sql.connections.Connection
                connection = sql.connect(user=params['user'],
                                         password=params['password'],
                                         db='mysql', host=params['host'])
                cursor = connection.cursor()
                cursor.execute(f'CREATE DATABASE {params["db"]}')
                cursor.commit()
                cursor.close()
                connection.close()
                self.connection = sql.connect(user=params['user'],
                                              password=params['password'],
                                              db=params['db'], host=params['host'])
                self.cursor = self.connection.cursor()
                self.user = params['user']
                self.host = params['host']
                self.db = params['db']
            self.meta_table = None

    def create_meta_table(self, table='meta', drop=False):
        self.cursor.execute('show tables')
        tables = [table[0] for table in self.cursor.fetchall()]
        if table in tables:
            if not drop:
                warn(f'Table {table} existed on databse {self.db},' +
                     f'and was not dropped. No new metadata added')
                return
            self.cursor.execute(f'DROP TABLE {table}')
            self.connection.commit()
        self.cursor.execute(f'''CREATE TABLE {table}
                            (
                                record_id MEDIUMINT UNSIGNED PRIMARY KEY,
                                record_type VARCHAR(25),
                                department VARCHAR(20),
                                main_concept VARCHAR(100),
                                main_concept_code VARCHAR(15),
                                aux_concept_codes VARCHAR(250),
                                year SMALLINT UNSIGNED)''')
        self.connection.commit()
        self.meta_table = table

    def populate_meta(self, data: List[Tuple]):
        exec_str = f''' INSERT INTO {self.meta_table}
                            (record_id, record_type, department,
                            main_concept, main_concept_code, 
                            aux_concept_codes, year)
                        VALUES
                            (%s,%s,%s,%s,%s,%s,%s) '''
        self.cursor.executemany(exec_str, data)
        self.connection.commit()
