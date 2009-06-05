#!/usr/bin/env python

'''
Skip Montanaro's FSM (from http://wiki.python.org/moin/FiniteStateMachine)
'''

# Imports

# Local Variables
# Global Variables

# Class Declarations
class FSM:
   '''
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
      '''Add a transition to the FSM.
      '''
      self.states[(state, input)] = (newstate, action)

   def execute(self, input):
      '''Perform a transition and execute action.
      '''
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

      if action != None:
         action(self.state, input)

      self.state = newstate

   def start(self, state):
      '''Define the start state.
   
      Actually, this just resets the current state.
      '''
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
