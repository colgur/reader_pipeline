#!/usr/bin/env python

''' Interfaces with Google Reader database
- based on accepted answer in StackOverflow article 52880
- references from GoogleReaderAPI (http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
'''

# Imports
import logging

# Global Variables

# Class Declarations
# Function Declarations
def dump(filename, content):
   ''' Common save of Reader Content to file for post-processing
   '''
   try:
      contentfile = open(filename, 'w')
      contentfile.write(content)
      contentfile.close()
   except IOError, reason:
      reasonstr = str(reason)
      msg = ' '.join(['Failed to store Reading List:', reasonstr])
      logging.critical(msg)

def main():
   try:
      from GoogleReader.reader import GoogleReader
   except ImportError, reason:
      message = 'Import failed: %s' % str(reason)
      print message
      return

   reader = GoogleReader('colgur@gmail.com', 'madU64pa')
   reader.login()

   preferences = reader.get_preferences()
   dump('/home/crc/builds/Apollo/Preferences.xml', preferences)

   subscriptions = reader.get_subscriptions()
   dump('/home/crc/builds/Apollo/Subscriptions.xml', subscriptions)

   unread = reader.get_unreadcount()
   dump('/home/crc/builds/Apollo/UnreadCount.xml', unread)

   reading = reader.get_readinglist(100)
   dump('/home/crc/builds/Apollo/ReadingList.xml', reading)

# "main" body
if __name__ == '__main__':
    main()
