'''
Test Documentation
'''
from feeds.google.reader.list import Subscriptions
from feeds.google.reader.list import Subscription

import xml.sax.saxutils
import unittest

class Test(unittest.TestCase):

   def unescape(self):
       validate = [self.scoobie, self.snacks]
       for sub in validate:
           sub[Subscriptions.ID] = xml.sax.saxutils.unescape(sub[Subscriptions.ID])
           sub[Subscriptions.TITLE] = xml.sax.saxutils.unescape(sub[Subscriptions.TITLE])

       return validate

   def setUp(self):
      self.scoobie = {Subscriptions.ID:'feed/http://www.scoobie.com&amp;_render=rss',\
                 Subscriptions.TITLE:'Scoobie Subscription'}
      self.snacks = {Subscriptions.ID:'feed/http://www.snacks.com', \
                Subscriptions.TITLE:'Snacks Subscription'}

      self.testinput = """
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
      </object>""" % (self.scoobie[Subscriptions.ID], self.scoobie[Subscriptions.TITLE],\
                      self.snacks[Subscriptions.ID], self.snacks[Subscriptions.TITLE])

   def tearDown(self):
      pass

   def testSubscriptions(self):
      subs = Subscriptions(self.testinput)

      sublist = subs.get_feed()

      elements = len(sublist)
      self.assertEquals(elements, 2, 'Fail: Number of elements = %i' % elements)

      validate = self.unescape()
      for sub in sublist:
         self.failUnless(sub in validate, 'Fail: Where is %s?' % sub)

   def testExpatFsm(self):
      import feeds.google.reader.list
      subs = feeds.google.reader.list.subscriptions(self.testinput)

      elements = len(subs)
      self.assertEquals(elements, 2, 'Number of elements = %i' % elements)

      validate = self.unescape()
      validiter = iter(validate)
      for eachsub in subs:
         valid = validiter.next()
         self.assertEquals(eachsub.id(), valid[Subscription.ID], 'Calculated ID = %s' % eachsub.id())
         self.assertEquals(eachsub.title(), valid[Subscription.TITLE], 'Calculated TITLE = %s' % eachsub.title())

suite = unittest.TestLoader().loadTestsFromTestCase(Test)
unittest.TextTestRunner().run(suite)
