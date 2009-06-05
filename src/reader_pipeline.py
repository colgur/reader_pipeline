#!/usr/bin/env python

'''
NLTK pipeline based on Google Reader feed(s)
'''

# Imports
import logging
import sys, nltk, re, pprint
from feeds.google.reader import *

# Global Variables

# Class Declarations

# Function Declarations
def getcontent(tokens):
   ''' Use NLTK to drive off stopwords '''
   stopwords = nltk.corpus.stopwords.words('english')
   content = [w for w in tokens if w.lower() not in unicode(stopwords)]
   longcontent = [w for w in content if len(w) > 3]

   return longcontent

def topcontent(tokens):
   ''' Use NLTK to discover the top ten most frequent terms '''
   content = getcontent(tokens)

   fdist = nltk.FreqDist(content)
   vocab = fdist.keys()

   return vocab[:50]

def contentfraction(tokens):
   ''' Sample function from NLTK section 2.4.1 '''
   from decimal import Decimal

   content = getcontent(tokens)
   return Decimal(len(content)) / Decimal(len(tokens))

def tokenize(feedset):
   ''' Use NLTK to tokenize titles from Feed Set '''
   titletokens = []
   for (title, link) in feedset:
      tokens = nltk.word_tokenize(title)
      titletokens.extend(tokens)

   return titletokens

def create_feedset(subscriptions):
   ''' Call on Google Reader with subscription request
   and create a set of (title, link) pairs: a Feed Set '''
   try:
      import feedparser
   except ImportError:
      logging.critical("Require feedparser module")
      # TODO: Error path
      return

   feedset = []
   subs_rss = atomapi.get_unread(subscriptions)

   pipe_feed = feedparser.parse(subs_rss)
   for entry in pipe_feed.entries:
      feedset.append((entry.title, entry.link))

   return feedset

def main():
   ''' Program entry point '''
   # TODO: Parse login (feed title?) from options
   feed_titles = ('Programming')

   access.login('colgur@gmail.com', 'madU64pa')

   response = listapi.request(listapi.SUBSCRIPTIONS)
   subs = listapi.Subscriptions(response)
   programming_sub = subs.get_feed(feed_titles[0])

   feedset = create_feedset(programming_sub)

   tokens = tokenize(feedset)
   fraction = contentfraction(tokens)
   mostfrequent = topcontent(tokens)

   print 'content fraction: ' + str(fraction)
   print 'top ten: '
   pprint.pprint(mostfrequent)

# "main" body
if __name__ == '__main__':
   main()
