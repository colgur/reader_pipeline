'''
Created on May 28, 2009

@author: crc
'''
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
