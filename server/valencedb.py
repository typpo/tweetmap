# 
# Talks to valence db
#

import MySQLdb

DEFAULT_HOST = 'jamuna-prime.cs.dartmouth.edu'
DEFAULT_USER = 'ianw'
DEFAULT_PASS = 'uzpM03Eoi'
DEFAULT_DB = 'ianw'

VALID_TYPES = ['valence', 'arousal', 'dominance']
VALID_SEXES = ['m', 'f', 'all']

class ValenceDB:
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
            

    def create_table(self):
        print 'Creating table structure'
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS anew (
           id INTEGER PRIMARY KEY AUTO_INCREMENT, 
           sexes varchar(30), 
           word varchar(30), 
           wdnum INTEGER, 
           valmn FLOAT,
           valsd FLOAT, 
           aromn FLOAT, 
           arosd FLOAT, 
           dommn FLOAT, 
           domsd FLOAT,
           freq INTEGER,

           UNIQUE (sexes, word)
       );
        """)
        self.conn.commit()

    def get_stat(self, word, sex='all', type='valence'):
        word = word.encode('utf-8')

        if sex not in VALID_SEXES:
            print 'no such sex option:', sex
            return -1
        if type not in VALID_TYPES:
            print 'no such type option:', type
            return -1

        if type == 'valence':
            type = 'valmn'
        elif type == 'arousal':
            type = 'aromn'
        else:
            type = 'dommn'

        query = 'select ' + type + ' from anew where sexes=%s and word=%s limit 1'
        queryargs = [sex, word]
        self.cur.execute(query, queryargs)
        results = self.cur.fetchall()
        if len(results) < 1:
            return -1
        return results[0][0]

if __name__ == '__main__':
    db = ValenceDB()
    db.connect()
    print 'Ready...'
