#!/usr/bin/env python

'''
Objects representing Google Reader Lists
'''

# Imports
import xml.parsers.expat

# Global Variables

# Class Declarations
class Subscriptions():
   ''' Convenient packaging of List API (XML) output
   '''
   SEEKING_ID = 0
   ACQ_ID = 1
   SEEKING_TITLE = 2
   ACQ_TITLE = 3

   STATE = ('id', 'idacq', 'title', 'titleacq')

   def __init__(self, raw_xml):
      ''' Process XML now or later
      '''
      self._parser = xml.parsers.expat.ParserCreate()

      self._parser.StartElementHandler = self.start_element
      self._parser.EndElementHandler = self.end_element
      self._parser.CharacterDataHandler = self.char_data

      # List of Subscriptions
      self._subs = []
      self._sub = {}
      self._state = self.SEEKING_ID

      try:
         self._parser.Parse(raw_xml, 1)
      except xml.parsers.expat.ExpatError, err:
         message = 'Expat Error: %s (%i, %i)' % (xml.parsers.expat.ErrorString(err.code),\
                                                 err.lineno,\
                                                 err.offset)
         return

   def start_element(self, name, attrs):
      print 'Start element:', name, attrs

   def end_element(self, name):
      print 'End element:', name

   def char_data(self, data):
      print 'Character data:', repr(data)

   def get_feed(self, title=None):
      ''' Get Feed by title or all Feeds
      '''
      if not self._subs or title == None:
         return self._subs

      matching = []
      for sub in self._subs:
         if title in sub['title']:
            matching.append(sub)

      return matching

# Function Declarations
def test():
   ''' Quick and dirty unit test
   '''
   scoobie = {'id':'feed/http://www.scoobie.com', 'title':'Scoobie Subscription'}
   snacks = {'id':'feed/http://www.snacks.com', 'title':'Snacks Subscription'}
   validate = [scoobie, snacks]

   testinput = """
   <object>
      <list name="subscriptions">
         <object>
            <string name="id">%s</string>
            <string name="title">%s</string>
            <list name="categories"/>
            <string name="sortid">707AA16C</string>
            <number name="firstitemmsec">1237751512927</number>
         </object>
         <object>
            <string name="id">%s</string>
            <string name="title">%s</string>
            <list name="categories"/>
            <string name="sortid">707AA16C</string>
            <number name="firstitemmsec">1237751512927</number>
         </object>
      </list>
   </object>""" % (scoobie['id'], scoobie['title'],\
                   snacks['id'], snacks['title'])

   subs = Subscriptions(testinput)

   sublist = subs.get_feed()

   elements = len(sublist)
   if elements != 2:
      message = 'Fail: Number of elements = %i' % elements
      print message

   for sub in sublist:
      if sub not in validate:
         message = 'Fail: Where is %s?' % sub
         print message

# "main" body
if __name__ == '__main__':
    test()
