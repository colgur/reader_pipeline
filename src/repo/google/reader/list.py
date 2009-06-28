#!/usr/bin/env python

''' Represent the 'List API' defined by pyrfeed 
(http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
'''

__license__ = '''Copyright (c) 2009 Chad Colgur

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.'''

# Imports
import urllib, xml.parsers.expat

from repo.google.reader import access
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

class AttributeFilter:
   '''Filter Expat processing'''
   __ACQ_SIGNAL = 'start'

   def __init__(self, filter, complete_cb):
      '''Initialize with tag list and proc'''
      # Parameterize Expat
      self.__parser_init()

      # (tag:value) mapping returned via callback/proc
      self._filter = filter
      self._acquire = dict.fromkeys(filter)
      self._current_tag = iter(filter)

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

      tagiter = iter(self._filter)
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
         self._current_tag = iter(self._filter)
         current_key = self._current_tag.next()
         pass

      self._acquire[current_key] = input

   def last_action(self, state, input):
      self.acquire(state, input)
      if self.__callback != None:
         self.__callback(self._acquire)

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

   parser = AttributeFilter(filter, append)
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

   parser = AttributeFilter(filter, append)
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
