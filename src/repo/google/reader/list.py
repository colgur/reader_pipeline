#!/usr/bin/env python

'''
Represent the 'List API' defined by pyrfeed (http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
'''

# Imports
import urllib

from repo.google.reader import access
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

   def __init__(self, tag_value_dict=None):
      try:
         self.id = tag_value_dict[self.ID]
      except KeyError:
         self.id = ''
         pass
      try:
         self.title = tag_value_dict[self.TITLE]
      except KeyError:
         self.title = ''
         pass
      try:
         self.count = tag_value_dict[self.COUNT]
      except KeyError:
         self.count = '0'
         pass

   def __eq__(self, inst):
      if self.id == inst.id and \
         self.title == inst.title and \
         self.count == inst.count:
         return True
      else:
         return False

   def __ne__(self, inst):
      if self.id != inst.id or \
         self.title != inst.title or \
         self.count != inst.count:
         return True
      else:
         return False

# Function Declarations
def subscriptions(sub_xml=None):
   '''Call the proc with List of Subscriptions.'''
   if sub_xml == None:
      sub_xml = request(SUBSCRIPTIONS)

   filter = (Subscription.ID,\
             Subscription.TITLE)
   subs = []

   # Closure instantiates Subscription upon ExpatFsm event
   def append(tag_dict):
      sub = Subscription(tag_dict)
      subs.append(sub)

   parser = ExpatFsm(filter, append)
   parser.parse(sub_xml)

   return subs

def unread(raw_xml=None):
   '''Call the proc with List of Subscriptions.'''
   if raw_xml == None:
      raw_xml = request(UNREAD_COUNT)

   filter = (Subscription.ID,\
             Subscription.COUNT)
   unread = []

   # Closure instantiates Subscription upon ExpatFsm event
   def append(tag_dict):
      anunread = Subscription(tag_dict)
      unread.append(anunread)

   parser = ExpatFsm(filter, append)
   parser.parse(raw_xml)

   return unread

def merge(sub_seq, unread_seq):
   '''Reconcile Subscription class with Reader List API'''
   merged_seq = []
   for eachunread in unread_seq:
      sub_iter = iter(sub_seq)
      while True:
         try:
            sub = sub_iter.next()
         except StopIteration:
            merged_seq.append(eachunread)
            break
         if sub.id == eachunread.id:
            eachunread.title = sub.title
            merged_seq.append(eachunread)
            break

   return merged_seq

def request(api_id):
   ''' Helper formats request'''
   parameters = urllib.urlencode({'output': 'xml'})
   function = '%s%s?%s' % (access.URI_API, api_id, parameters)

   response = access.request(function)
   return response

def test():
   ''' Unit test this little world '''
   import repo.google.reader.list_unit

# "main" body
if __name__ == '__main__':
   test()
