# 
# Talks to tweet storage db
#

import MySQLdb
import time

DEFAULT_HOST = ''
DEFAULT_USER = ''
DEFAULT_PASS = ''
DEFAULT_DB = ''

class StoreDB:
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

    
    # Records a tweet
    def add_tweet(self, tweet, valence):
        query = """
INSERT INTO tweets (author,text,time,location,valence) VALUES (
    %s,%s,%s,GeomFromText('Point(%s %s)'),%s
);
         """
        ts = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        formatted = time.strftime('%Y-%m-%d %H:%M:%S', ts)
        queryargs = [tweet['user']['screen_name'].encode('utf-8'),
            tweet['text'].encode('utf-8')[:140],
            formatted,
            float(tweet['geo']['coordinates'][0]),
            float(tweet['geo']['coordinates'][1]),
            float(valence)]

        #print queryargs
        self.cur.execute(query, queryargs)


    def create_table(self):
        print 'Creating table structure'
        self.cur.execute("""
CREATE TABLE IF NOT EXISTS tweets (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    author VARCHAR(16) NOT NULL,
    text VARCHAR(160) NOT NULL,
    time DATETIME NOT NULL,
    location POINT NOT NULL,
    valence FLOAT
       );

CREATE INDEX tweets_location_index ON tweets(location);
CREATE INDEX tweets_time_index ON tweets(time);
CREATE INDEX tweets_valence_index ON tweets(valence);
        """)


if __name__ == '__main__':
    print 'Initializing db connection'
    db = StoreDB()
    db.connect()
    print 'Ready'
