#
# ANEW text analytics for tweets
#

import stemmer
import time
import string
from baseanalyzer import BaseAnalyzer
from valencedb import ValenceDB

class BasicAnalyzer(BaseAnalyzer):

    def __init__(self, storedb, logfunc=None):
        print 'Initializing ANEW module'

        self.store_db = storedb
        self.valence_db = ValenceDB()
        self.stemmer = stemmer.PorterStemmer()
        self.logfunc = logfunc
        self.total_count = 0

        # Connect to ANEW database
        self.valence_db.connect()

    def analyze_tweet(self, tweet):
        try:
            self.log('%s Received geolocated tweet (%d)' % (time.ctime(), self.total_count))

            splits = [word.strip(string.punctuation) for word in tweet['text'].split()]
            if len(splits) < 3:
                self.log('\ttoo short')
                return

            self.log('\tanalyzing...')

            count = 0 
            total = 0
            f = 0.0
            for split in splits:
                tmp = self.valence_db.get_stat(split)
                if tmp == -1:
                    # Word not found, so try stemming
                    tmp = self.valence_db.get_stat(self.stemmer.stem(split))
                total +=1
                if tmp != -1:
                    # Nothing found
                    count += 1
                    f += tmp
            if count > 0:
                avg = f/count
                self.log('\t'+str(avg))
            else:
                avg = -1
                self.log('\tCouldn\'t score')

            # save tweet text, author, time, location, valence to DB
            self.store_db.add_tweet(tweet, avg)
            self.total_count += 1
        except:
            pass

    def stop(self):
        self.valence_db.close()

    def log(self, msg):
        if self.logfunc:
            self.logfunc(msg)
        else:
            print msg


