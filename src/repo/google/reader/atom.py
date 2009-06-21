#!/usr/bin/env python

'''
Module Documentation
'''

# Imports
import logging
try:
   import feedparser
except ImportError:
   logging.critical("feedparser module is missing")
   pass

import repo.google.reader.list
from repo.google.reader import access

# Global Variables

# Class Declarations
class Feed:
   '''Highest level of access'''

   def __init__(self, subscription):
      self.sub = subscription
      self.reading_list = ''

   def refresh(self):
      '''Pick-up Reading List based on Subscription data'''
      feed_id = self.sub.id
      unread_count = int(self.sub.count)
      self.reading_list = repo.google.reader.atom.request(feed_id, unread_count)

   def parse(self):
      '''Invoke Feed Parser'''
      parse_tree = feedparser.parse(self.reading_list)
      return parse_tree

# Function Declarations
def feeds(username, password):
   '''Highest level entry point'''
   access.login(username, password)

   subs = repo.google.reader.list.subscriptions()
   unread = repo.google.reader.list.unread()
   merged = repo.google.reader.list.merge(subs, unread)

   userfeeds = []
   for eachsub in merged:
      feed = Feed(eachsub)
      userfeeds.append(feed)

   return userfeeds

def build_url(feed_id, count):
   '''Helper formats request'''
   import urllib, time

   # TODO: customize number of unread 'n'
   ck = int(time.time())
   parameters = urllib.urlencode({'n': count, \
                                  'ck':ck, \
                                  'xt':'user/-/state/com.google/read'}, True)

   quoted_feed_id = urllib.quote(feed_id)

   request_url = '%s%s?%s' % (access.URI_ATOM, quoted_feed_id, parameters)
   return request_url

def request(feed_id, count=20):
   ''' Helper formats request'''
   from repo.google.reader import access

   function = build_url(feed_id, count)
   response = access.request(function)

   return response

def get_unread(subscriptions):
   ''' Access Reader to retrieve all unread items of subscriptions'''
   from repo.google.reader.listapi import Subscriptions

   feedid = []
   for sub in subscriptions:
      feedid.append(sub[Subscriptions.ID])

   #TODO: Iterate over all feeds for all subscriptions
   sub_rss = request(feedid[0])

   return sub_rss

def test():
   ''' Unit test this little world '''
   pass

# "main" body
if __name__ == '__main__':
   test()
