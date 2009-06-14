#!/usr/bin/env python

'''
Module Documentation
'''

# Imports
from feeds.google.reader import access

# Global Variables

# Class Declarations
class Feed:
   '''Highest level of access'''

   def __init__(self):
      name = ''
      link = ''
      reading_list = ''

# Function Declarations
def feeds(username, password):
   '''Highest level entry point'''
   access.login(username, password)

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
   from feeds.google.reader import access

   function = build_url(feed_id, count)
   response = access.request(function)

   return response

def get_unread(subscriptions):
   ''' Access Reader to retrieve all unread items of subscriptions'''
   from feeds.google.reader.listapi import Subscriptions

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
