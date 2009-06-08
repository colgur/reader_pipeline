#!/usr/bin/env python

'''
Module representing List API of pyrfeed (http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
'''

# Imports
import urllib
import xml.parsers.expat

from feeds.google.reader import access
from utils.fsm import FSM

# Global Variables

# Local Variables
PREFERENCES = 'preference/list'
SUBSCRIPTIONS = 'subscription/list'
TAGS = 'tag/list'
UNREAD_COUNT = 'unread-count'

# Class Declarations
class Subscriptions():
   ''' Convenient packaging of List API (XML) output
   '''
   ID = 'id'
   TITLE = 'title'
   ACQUIRE = {'id' : 0, 'title' : 1}
   ACQ_SIGNAL = 'start'

   def __init__(self, raw_xml):
      ''' Process XML now or later
      '''
      self._parser = xml.parsers.expat.ParserCreate('utf-8')
      self._parser.buffer_text = True

      self._parser.StartElementHandler = self.start_element
      self._parser.EndElementHandler = self.end_element
      self._parser.CharacterDataHandler = self.char_data

      self._fsm = FSM()

      self._fsm.add(self.ID, None, self.ID, None)
      self._fsm.add(self.ID, self.ACQ_SIGNAL, self.ACQUIRE[self.ID], self.add_sub)
      self._fsm.add(self.ACQUIRE[self.ID], None, self.TITLE, self.acquire_id)

      self._fsm.add(self.TITLE, None, self.TITLE, None)
      self._fsm.add(self.TITLE, self.ACQ_SIGNAL, self.ACQUIRE[self.TITLE], None)
      self._fsm.add(self.ACQUIRE[self.TITLE], None, self.ID, self.acquire_title)

      self._fsm.start(self.ID)

      # List of Subscriptions
      self._subs = []

      try:
         self._parser.Parse(raw_xml, 1)
      except xml.parsers.expat.ExpatError, err:
         message = 'Expat Error: %s (%i, %i)' % (xml.parsers.expat.ErrorString(err.code),\
                                                 err.lineno,\
                                                 err.offset)
         # TODO: Error path/Exceptions 
         return

   def start_element(self, name, attrs):
      attrs_vals = attrs.values()
      if (self.ID in attrs_vals) or (self.TITLE in attrs_vals):
         self._fsm.execute(self.ACQ_SIGNAL)

   def end_element(self, name):
      pass

   def char_data(self, data):
      self._fsm.execute(data)

   def default_char_data(self, data):
      ''' Default Character Data handler'''
      self._fsm.execute(data)

   def get_feed(self, title=None):
      ''' Get Feed by title or all Feeds
      '''
      if not self._subs or title == None:
         return self._subs

      matching = []
      for sub in self._subs:
         if title in sub[self.TITLE]:
            matching.append(sub)

      return matching

   def acquire_id(self, state, input):
      ''' Populate Subscription List '''
      sub = self._subs.pop()
      sub[self.ID] = input
      self._subs.append(sub)

   def acquire_title(self, state, input):
      ''' Populate Subscription List '''
      sub = self._subs.pop()
      sub[self.TITLE] = input
      self._subs.append(sub)

   def add_sub(self, state, input):
      ''' Append to subscription list '''
      sub = {self.ID : None, self.TITLE : None}
      self._subs.append(sub)

# Function Declarations
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
