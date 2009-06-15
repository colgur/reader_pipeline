#!/usr/bin/env python

'''
Skip Montanaro's FSM (from http://wiki.python.org/moin/FiniteStateMachine)
'''

# Imports
import xml.parsers.expat

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

class ExpatFsm:
   '''
   A (little) less generic FSM.
   Meant for internal use but might be relocate-able to utils package
   '''
   __ACQ_SIGNAL = 'start'

   def __init__(self, tags, complete_cb):
      '''Initialize with tag list and proc'''
      # Parameterize Expat
      self.__parser_init()

      # (tag:value) mapping returned via callback/proc
      self._tagseq = tags
      self._acquire = dict.fromkeys(tags)
      self._current_tag = iter(tags)

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

      tagiter = iter(self._tagseq)
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
         self._current_tag = iter(self._tagseq)
         current_key = self._current_tag.next()
         pass

      self._acquire[current_key] = input

   def last_action(self, state, input):
      self.acquire(state, input)
      if self.__callback != None:
         self.__callback(self._acquire)

# Global Function Declarations
def test():
   import utils.fsmunit

# "main" body
if __name__ == '__main__':
    test()
