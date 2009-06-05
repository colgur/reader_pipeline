#!/usr/bin/env python

'''
Module Documentation
'''

# Imports

# Global Variables

# Class Declarations

# Function Declarations
def request(feed_id):
   ''' Helper formats request'''
   import urllib, time
   from feeds.google.reader import access

   # TODO: customize number of unread 'n'
   ck = int(time.time())
   parameters = urllib.urlencode({'n': '20', \
                                  'ck':ck, \
                                  'xt':'user/-/state/com.google/read'}, True)

   quoted_feed_id = urllib.quote(feed_id)

   function = '%s%s?%s' % (access.URI_ATOM, quoted_feed_id, parameters)
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
   import feeds.google.reader.atomapi_unit

# "main" body
if __name__ == '__main__':
   test()
