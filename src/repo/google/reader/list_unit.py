#!/usr/bin/env python

''' Unit test code '''

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

import repo.google.reader.list
from repo.google.reader.list import Subscription

import xml.sax.saxutils
import unittest

class Test(unittest.TestCase):

   def setUp(self):
      self.SCOOBIE_TITLE = 'Scoobie Subscription'
      self.SCOOBIE_ID = 'feed/http://www.scoobie.com&amp;_render=rss'
      self.SCOOBIE_COUNT = '1000'

      self.SNACKS_TITLE = 'Snacks Subscription'
      self.SNACKS_ID = 'feed/http://www.snacks.com'
      self.SNACKS_COUNT = '1000'

      self.THEGANG_TITLE = 'The Gang Subscription'
      self.THEGANG_ID = 'feed/http://www.thegang.com'
      self.THEGANG_COUNT = '1500'

      self.SHAGGY_TITLE = 'Shaggy Subscription'
      self.SHAGGY_ID = 'feed/http://www.shaggy.com'
      self.SHAGGY_COUNT = '250'

   def tearDown(self):
      pass

   def validate(self, xml_test, attribs):
      '''Common functionality'''

   def testSubscriptions(self):
      attribs = [Subscription.ID, Subscription.TITLE]
      scoobie_sub = Subscription({attribs[0]:self.SCOOBIE_ID, attribs[1]:self.SCOOBIE_TITLE})
      snacks_sub = Subscription({attribs[0]:self.SNACKS_ID, attribs[1]:self.SNACKS_TITLE})

      test_element = []
      expected_subs = [scoobie_sub, snacks_sub]
      for eachsub in expected_subs:
         for eachattrib in attribs:
            element = '<string name="%s">%s</string>' % (eachattrib, getattr(eachsub, eachattrib))
            test_element.append(element)

      xml_test = """
      <object>
         <list name="subscriptions">
            <object>
               %s
               %s
               <list name="categories"/>
               <string name="sortid">707AA16C</string>
               <number name="firstitemmsec">1237751512927</number>
            </object>
            <object>
               %s
               %s
               <list name="categories"/>
               <string name="sortid">707AA16C</string>
               <number name="firstitemmsec">1237751512927</number>
            </object>
         </list>
      </object>""" % (test_element[0], test_element[1],\
                     test_element[2], test_element[3])

      subs = repo.google.reader.list.subscriptions(xml_test)

      elements = len(subs)
      self.assertEquals(elements, 2, 'Number of elements = %i' % elements)

      scoobie_sub.id = xml.sax.saxutils.unescape(scoobie_sub.id)
      subs_iter = iter(subs)

      for expected in expected_subs:
         actual = subs_iter.next()
         self.assertTrue(expected == actual)

   def testUnread(self):
      attribs = [Subscription.ID, Subscription.COUNT]
      scoobie_sub = Subscription({attribs[0]:self.SCOOBIE_ID, attribs[1]:self.SCOOBIE_COUNT})
      snacks_sub = Subscription({attribs[0]:self.SNACKS_ID, attribs[1]:self.SNACKS_COUNT})

      test_element = []
      expected_subs = [scoobie_sub, snacks_sub]
      for eachsub in expected_subs:
         for eachattrib in attribs:
            element = '<string name="%s">%s</string>' % (eachattrib, getattr(eachsub, eachattrib))
            test_element.append(element)

      xml_test = """
      <object>
         <number name="max">1000</number>
         <list name="unreadcounts">
            <object>
               %s
               %s
               <number name="newestItemTimestampUsec">1243356412327019</number>
            </object>
            <object>
               %s
               %s
               <number name="newestItemTimestampUsec">1243329792089154</number>
            </object>
         </list>
      </object>""" % (test_element[0], test_element[1],\
                     test_element[2], test_element[3])

      subs = repo.google.reader.list.unread(xml_test)

      elements = len(subs)
      self.assertEquals(elements, 2, 'Number of elements = %i' % elements)

      scoobie_sub.id = xml.sax.saxutils.unescape(scoobie_sub.id)
      subs_iter = iter(subs)

      for expected in expected_subs:
         actual = subs_iter.next()
         self.assertTrue(expected == actual)

   def testMerge(self):
      sub_attribs = [Subscription.ID, Subscription.TITLE]
      unread_attribs = [Subscription.ID, Subscription.COUNT]

      scoobie_sub = Subscription({sub_attribs[0]:self.SCOOBIE_ID, sub_attribs[1]:self.SCOOBIE_TITLE})
      snacks_sub = Subscription({sub_attribs[0]:self.SNACKS_ID, sub_attribs[1]:self.SNACKS_TITLE})
      subs = [scoobie_sub, snacks_sub]

      scoobie_unread = Subscription({sub_attribs[0]:self.SCOOBIE_ID, sub_attribs[1]:self.SCOOBIE_COUNT})
      snacks_unread = Subscription({sub_attribs[0]:self.SNACKS_ID, sub_attribs[1]:self.SNACKS_COUNT})
      unread = [scoobie_unread, snacks_unread]

      merged = repo.google.reader.list.merge(subs, unread)

      scoobie_unread.title = scoobie_sub.title
      snacks_unread.title = snacks_sub.title

      merged_iter = iter(merged)
      self.assertTrue(merged_iter.next() == scoobie_unread)
      self.assertTrue(merged_iter.next() == snacks_unread)

suite = unittest.TestLoader().loadTestsFromTestCase(Test)
unittest.TextTestRunner().run(suite)
