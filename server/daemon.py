#!/usr/bin/env python
#
# Collects twitter data and stores it to database
# 

import time
import tweetstream
import string
import sys
from storedb import StoreDB
from twitter_config import TWITTER_USER, TWITTER_PASS
from basicanalyzer import BasicAnalyzer

# Runs listener to Twitter stream
# TODO add command line flag for log path, follow/track
class StreamListener:

    def __init__(self, log_path=str(int(time.time()))+'.log', log_loud=True):
        self.log_path = log_path
        self.store_db = StoreDB()
        self.stream = None

        self.log_loud = log_loud
        self.log_file = open(log_path, "a")

        self.analyzer = BasicAnalyzer(self.store_db, logfunc=self.log)


    # Starts a listening thread
    def start(self, filter=False):
        self._dbconnect()

        while True:
            self.stream = tweetstream.TweetStream(TWITTER_USER, TWITTER_PASS)

            for tweet in self.stream:
                if not 'geo' in tweet or not tweet['geo']:
                    continue
                self.analyzer.analyze_tweet(tweet)



    def _dbconnect(self):
        print 'Connecting to databases...'
        self.store_db.connect()


    def stop(self):
        self.store_db.close()
        self.analyzer.stop()

    def log(self, msg):
        self.log_file.write(msg)
        if self.log_loud:
            print msg



s = None 

def main():
    s = StreamListener()
    s.start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Shutting down...'
        if s:
            s.stop()
