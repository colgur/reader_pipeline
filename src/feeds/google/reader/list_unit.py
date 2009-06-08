'''
Test Documentation
'''
from feeds.google.reader.list import Subscriptions
import unittest

class Test(unittest.TestCase):

   def setUp(self):
      pass

   def tearDown(self):
      pass

   def testSubscriptions(self):
      scoobie = {Subscriptions.ID:'feed/http://www.scoobie.com&amp;_render=rss',\
                 Subscriptions.TITLE:'Scoobie Subscription'}
      snacks = {Subscriptions.ID:'feed/http://www.snacks.com', \
                Subscriptions.TITLE:'Snacks Subscription'}

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
      </object>""" % (scoobie[Subscriptions.ID], scoobie[Subscriptions.TITLE],\
                      snacks[Subscriptions.ID], snacks[Subscriptions.TITLE])

      subs = Subscriptions(testinput)

      sublist = subs.get_feed()

      elements = len(sublist)
      self.assertEquals(elements, 2, 'Fail: Number of elements = %i' % elements)

      from xml.sax.saxutils import unescape
      validate = [scoobie, snacks]
      for sub in validate:
         sub[Subscriptions.ID] = unescape(sub[Subscriptions.ID])
         sub[Subscriptions.TITLE] = unescape(sub[Subscriptions.TITLE])

      for sub in sublist:
         self.failUnless(sub in validate, 'Fail: Where is %s?' % sub)

suite = unittest.TestLoader().loadTestsFromTestCase(Test)
unittest.TextTestRunner().run(suite)
