#!/usr/bin/env python
'''Finite State Machine abstractions generic and Expat-related

Required: Python 2.4 or later
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

# Local Variables
# Global Variables

# Class Declarations
class FSM:
   '''Skip Montanaro's FSM (from http://wiki.python.org/moin/FiniteStateMachine)

   Finite state machine, featuring transition actions.

   The class stores a dictionary of (state, input) keys, and (state, action) values.

   When a (state, input) search is performed: * an exact match is checked first, * (state, None) is checked next.

   The action is of the following form: * function(current_state, input)
   ''' 

   def __init__(self):
      self.states = {}
      self.state = None
      self.dbg = None

   def add(self, state, input, newstate, action):
      '''Add a transition to the FSM.'''
      self.states[(state, input)] = (newstate, action)

   def execute(self, input):
      '''Perform a transition and execute action.'''
      si = (self.state, input)
      sn = (self.state, None)

      # exact state match?
      if self.states.has_key(si):
         newstate, action = self.states[si]
      # no, how about a None (catch-all) match?
      elif self.states.has_key(sn):
         newstate, action = self.states[sn]

      if self.dbg != None:
         self.dbg.write('State: %s / Input: %s /'
                        'Next State: %s / Action: %s\n' %
                        (self.state, input, newstate, action))

      # crc: Seemed strange to manually change state when no associated action
      # so add this check to Skip's implementation
      if action != None:
         action(self.state, input)

      self.state = newstate

   def start(self, state):
      '''Define the start state.
      Actually, this just resets the current state.'''
      self.state = state
   
   def debug(self, out):
      '''Assign a writable file to log transitions.'''
      self.dbg = out

# Global Function Declarations
def test():
   import utils.fsmunit

# "main" body
if __name__ == '__main__':
    test()
