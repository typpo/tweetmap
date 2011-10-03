#!/usr/bin/env python
#
# Naive Bayesian classifier wrapper
#

import sys
import os
import anyjson
from bayes.reverend import Bayes

DEFAULT_STATE_FILE = '/net/tahoe3/ianw/thesis/output/bayes_state.dat'

b = Bayes()
if os.path.exists(DEFAULT_STATE_FILE):
    b.load(fname=DEFAULT_STATE_FILE)

def train(group, text):
    print 'Training...'
    b.train(group, text)
    print 'Saving to %s...' % (DEFAULT_STATE_FILE)
    b.save(fname=DEFAULT_STATE_FILE)


def classify(text):
    results = b.guess(text)
    print anyjson.serialize(results)


def usage():
    print 'learner (classify text | train group text)'


if __name__ == '__main__':

    if len(sys.argv) == 3:
        if sys.argv[1] == 'classify':
            # classify
            classify(sys.argv[2])
            sys.exit(0)

    elif len(sys.argv) == 4:
        if sys.argv[1] == 'train':
            # train
            train(sys.argv[2], sys.argv[3])
            sys.exit(0)
    
    usage()
