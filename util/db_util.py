from typing import List, Dict, Tuple
from getpass import getpass
import MySQLdb as sql


class DatabaseHandle:
    connection: sql.connections.Connection = None
    cursor: sql.cursors.BaseCursor = None
    user: str = None
    host: str = None
    db: str = None

    def __init__(self, params: Dict[str, str] = None,
                 handle: DatabaseHandle = None):
        if isinstance(handle, DatabaseHandle):
            self = handle

        if isinstance(params, dict):
            self.connection = sql.connect(user=params['user'],
                                          password=params['password'],
                                          db=params['db'], host=params['host'])
            self.cursor = self.connection.cursor()
            self.user = params['user']
            self.host = params['host']
            self.db = params['db']

    def create_meta(self):
        pass
