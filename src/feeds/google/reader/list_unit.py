'''
Test Documentation
'''
import feeds.google.reader.list
from feeds.google.reader.list import Subscription

import xml.sax.saxutils
import unittest

class Test(unittest.TestCase):

   def unescape(self):
       validate = [self.scoobie, self.snacks]
       for sub in validate:
           sub[Subscription.ID] = xml.sax.saxutils.unescape(sub[Subscription.ID])
           sub[Subscription.TITLE] = xml.sax.saxutils.unescape(sub[Subscription.TITLE])

       return validate

   def setUp(self):
      self.scoobie = {Subscription.ID:'feed/http://www.scoobie.com&amp;_render=rss',\
                 Subscription.TITLE:'Scoobie Subscription',\
                 Subscription.COUNT:'1000'}
      self.snacks = {Subscription.ID:'feed/http://www.snacks.com', \
                Subscription.TITLE:'Snacks Subscription',\
                Subscription.COUNT:'500'}

      self.sub_xml = """
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
      </object>""" % (self.scoobie[Subscription.ID], self.scoobie[Subscription.TITLE],\
                      self.snacks[Subscription.ID], self.snacks[Subscription.TITLE])

      self.unread_xml = """
      <object>
         <number name="max">1000</number>
         <list name="unreadcounts">
            <object>
               <string name="id">%s</string>
               <number name="count">%s</number>
               <number name="newestItemTimestampUsec">1243356412327019</number>
            </object>
            <object>
               <string name="id">%s</string>
               <number name="count">%s</number>
               <number name="newestItemTimestampUsec">1243329792089154</number>
            </object>
         </list>
      </object>""" % (self.scoobie[Subscription.ID], self.scoobie[Subscription.COUNT],\
                            self.snacks[Subscription.ID], self.snacks[Subscription.COUNT])

   def tearDown(self):
      pass

   def testSubscriptions(self):
      subs = feeds.google.reader.list.subscriptions(self.sub_xml)

      elements = len(subs)
      self.assertEquals(elements, 2, 'Number of elements = %i' % elements)

      validate = self.unescape()
      validiter = iter(validate)
      for eachsub in subs:
         valid = validiter.next()
         self.assertEquals(eachsub.id(), valid[Subscription.ID], 'Calculated ID = %s' % eachsub.id())
         self.assertEquals(eachsub.title(), valid[Subscription.TITLE], 'Calculated TITLE = %s' % eachsub.title())

   def testUnread(self):
      subs = feeds.google.reader.list.unread(self.unread_xml)

      elements = len(subs)
      self.assertEquals(elements, 2, 'Number of elements = %i' % elements)

      validate = self.unescape()
      validiter = iter(validate)
      for eachsub in subs:
         valid = validiter.next()
         self.assertEquals(eachsub.id(), valid[Subscription.ID], 'Calculated ID = %s' % eachsub.id())
         self.assertEquals(eachsub.count(), valid[Subscription.COUNT], 'Calculated COUNT = %s' % eachsub.count())

suite = unittest.TestLoader().loadTestsFromTestCase(Test)
unittest.TextTestRunner().run(suite)
