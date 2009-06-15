#!/usr/bin/env python

'''
Represent the 'List API' defined by pyrfeed (http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
'''

# Imports
import urllib

from feeds.google.reader import access
from utils.fsm import ExpatFsm

# Global Variables

# Local Variables
PREFERENCES = 'preference/list'
SUBSCRIPTIONS = 'subscription/list'
TAGS = 'tag/list'
UNREAD_COUNT = 'unread-count'

# Class Declarations
class Subscription:
   '''Encapsulate for users of this module'''
   ID = 'id'
   TITLE = 'title'
   COUNT = 'count'

   def __init__(self, tag_value_dict):
      #TODO: Is copy() necessary? How smart is the pointer?
      self._tag_value_dict = tag_value_dict.copy()

   def id(self):
      return self.__tagvalue(self.ID)

   def title(self):
      return self.__tagvalue(self.TITLE)

   def count(self):
      return self.__tagvalue(self.COUNT)

   def __tagvalue(self, tagname):
      try:
         value = self._tag_value_dict[tagname]
      except KeyError:
         #TODO: re-throw and log
         value = ''
         pass

      return value

# Function Declarations
def subscriptions(sub_xml=None):
   '''Call the proc with List of Subscriptions.'''
   if sub_xml == None:
      sub_xml = request(SUBSCRIPTIONS)

   tags = (Subscription.ID,\
           Subscription.TITLE)
   subs = []

   # Closure instantiates Subscription upon ExpatFsm event
   def append(tag_dict):
      sub = Subscription(tag_dict)
      subs.append(sub)

   parser = ExpatFsm(tags, append)
   parser.parse(sub_xml)

   return subs

def unread(raw_xml=None):
   '''Call the proc with List of Subscriptions.'''
   if raw_xml == None:
      raw_xml = request(UNREAD_COUNT)

   tags = (Subscription.ID,\
           Subscription.COUNT)
   unread = []

   # Closure instantiates Subscription upon ExpatFsm event
   def append(tag_dict):
      anunread = Subscription(tag_dict)
      unread.append(anunread)

   parser = ExpatFsm(tags, append)
   parser.parse(raw_xml)

   return unread

def request(api_id):
   ''' Helper formats request'''
   parameters = urllib.urlencode({'output': 'xml'})
   function = '%s%s?%s' % (access.URI_API, api_id, parameters)

   response = access.request(function)
   return response

def test():
   ''' Unit test this little world '''
   import feeds.google.reader.list_unit

# "main" body
if __name__ == '__main__':
   test()
