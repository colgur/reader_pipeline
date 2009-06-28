#!/usr/bin/env python
'''Unit Test Code'''

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

from utils.fsm import FSM
import unittest

class Test(unittest.TestCase):
   VALID_TEST_OUTPUT = 2
   START_TEST_OUTPUT = 1

   def setUp(self):
      self._primaryout = 0

   def tearDown(self):
      pass

   def primary_start(self, fsm, input):
      self._primaryout = input
      return True

   def primary_stop(self, fsm, input):
      self._primaryout = input
      return True

   def conditional_start(self, fsmstate, input):
      return False

   def testPrimary(self):
      fsm = FSM()

      fsm.add('start', None, 'final', self.primary_start)
      fsm.add('final', None, 'start', self.primary_stop)
      fsm.start('start')

      fsm.execute(self.START_TEST_OUTPUT)
      fsm.execute(self.VALID_TEST_OUTPUT)

      self.assertEqual(self._primaryout, self.VALID_TEST_OUTPUT)

suite = unittest.TestLoader().loadTestsFromTestCase(Test)
unittest.TextTestRunner().run(suite)
