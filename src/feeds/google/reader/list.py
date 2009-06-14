#!/usr/bin/env python

'''
Represent the 'List API' defined by pyrfeed (http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
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
class Subscription:
   '''Encapsulate for users of this module'''
   ID = 'id'
   TITLE = 'title'

   def __init__(self, tag_value_dict):
      #TODO: Is copy() necessary? How smart is the pointer?
      self._tag_value_dict = tag_value_dict.copy()

   def id(self):
      return self.__tagvalue('id')

   def title(self):
      return self.__tagvalue('title')

   def __tagvalue(self, tagname):
      value = ''

      try:
         value = self._tag_value_dict[tagname]
      except KeyError:
         #TODO: re-throw and log
         value = ''
         pass

      return value

class ExpatFsm:
   '''
   A (little) less generic FSM.
   Meant for internal use but might be relocate-able to utils package
   '''
   __ACQ_SIGNAL = 'start'
   __callback = None

   def __init__(self, tags, complete_cb):
      '''Initialize with tag list and proc'''
      # Parameterize Expat
      self.__parser_init()

      # (tag:value) mapping returned via callback/proc
      self._acquire = dict.fromkeys(tags)
      self._current_tag = self._acquire.iterkeys()

      self.__fsm_init()
      self.__callback = complete_cb

   def __parser_init(self):
      '''Help initialize Expat'''
      self._parser = xml.parsers.expat.ParserCreate('utf-8')
      self._parser.buffer_text = True
      self._parser.StartElementHandler = self.start_element
      self._parser.EndElementHandler = self.end_element
      self._parser.CharacterDataHandler = self.char_data

   def __fsm_init(self):
      '''Helper initialize FSM'''
      self._fsm = FSM()

      tagiter = self._acquire.iterkeys()
      init_tag = current_tag = tagiter.next()
      while True:
         try:
            # Create distinct state transitions
            acq_tag = '%s%s' % (current_tag, '_acq')

            # Don't do anything before being signaled
            self._fsm.add(current_tag, None, current_tag, None)
            self._fsm.add(current_tag, self.__ACQ_SIGNAL, acq_tag, None)

            try:
               # Next user-/tag-defined state
               current_tag = tagiter.next()
               self._fsm.add(acq_tag, None, current_tag, self.acquire)
            except StopIteration:
               # Or close the loop
               self._fsm.add(acq_tag, None, init_tag, self.last_action)
               break
         except StopIteration:
            # TODO: Log: this should never happen
            break

      self._fsm.start(init_tag)

   def parse(self, raw_xml):
      '''Direct call on Expat instance'''
      try:
         self._parser.Parse(raw_xml, 1)
      except xml.parsers.expat.ExpatError, err:
         # TODO: Error path/Exceptions 
         message = 'Expat Error: %s (%i, %i)' % (xml.parsers.expat.ErrorString(err.code),\
                                                 err.lineno,\
                                                 err.offset)

   def start_element(self, name, attrs):
      try:
         if self._acquire.has_key(attrs['name']):
            self._fsm.execute(self.__ACQ_SIGNAL)
      except KeyError:
         # No a problem: Don't Care tag
         pass

   def end_element(self, name):
      pass

   def char_data(self, data):
      self._fsm.execute(data)

   def acquire(self, state, input):
      try:
         current_key = self._current_tag.next()
      except StopIteration:
         # Reset Current Tag
         self._current_tag = self._acquire.iterkeys()
         current_key = self._current_tag.next()
         pass

      self._acquire[current_key] = input

   def last_action(self, state, input):
      self.acquire(state, input)
      self.__callback(self._acquire)

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
def subscriptions(sub_xml=None):
   '''Call the proc with List of Subscriptions.'''
   if sub_xml == None:
      sub_xml = request(SUBSCRIPTIONS)

   tags = ('id', 'title')
   subs = []

   # Closure instantiates Subscription upon ExpatFsm event
   def append(tag_dict):
      sub = Subscription(tag_dict)
      subs.append(sub)

   parser = ExpatFsm(tags, append)
   parser.parse(sub_xml)

   return subs

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
