# 
# General mysql db client (abstract class)
#

import MySQLdb

DEFAULT_HOST = 'jamuna-prime.cs.dartmouth.edu'
DEFAULT_USER = 'ianw'
DEFAULT_PASS = 'uzpM03Eoi'
DEFAULT_DB = 'ianw'

class BaseDB:

    def __init__(self, host=DEFAULT_HOST, username=DEFAULT_USER, password=DEFAULT_PASS):
        self.host = host
        self.username = username
        self.password = password


    def connect(self, db=DEFAULT_DB):
        self.conn = MySQLdb.connect(host=self.host,
                                    user = self.username,
                                    passwd = self.password,
                                    db = db)
        self.cur = self.conn.cursor()
        print 'Connected to db @', self.host


    def close(self):
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()


    def create_table(self):
        pass
