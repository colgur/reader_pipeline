#!/usr/bin/env python

'''
Module Documentation
'''

# Imports
import sys

# Global Variables

# Class Declarations

# Function Declarations
def createdir(root_dir):
   '''
   Create directory name based on current time and root directory name
   '''
   import time
   import os
   import errno

   # build the Save Directory name from the current time + root
   utcsec = time.time()
   utc = time.gmtime(utcsec)
   dir_name = time.strftime("%Y%m%d_%H%M", utc)
   save_dir = root_dir + '/' + dir_name

   try:
      os.makedirs(save_dir)
   except OSError, e:
      if os.error.errno != errno.EEXIST:
         print "Failed to Create Save Dir: ", e
         save_dir = None

   return(save_dir)

def fetch(save_dir):
   ''' 
   Take down the various feeds and store them according to a set pattern,
   usually for post-processing
   '''
   import urllib
   import socket

   SAVE_FEED_TUPLE = (['digg.xml', 'http://feeds.digg.com/digg/topic/programming/popular.rss'],\
                    ["reddit_prog.xml", "http://www.reddit.com/r/programming/.rss"],\
                    ["delicious.xml", "http://feeds.delicious.com/v2/rss/popular/programming?count=15"],\
                    ["reddit_cpp.xml", "http://www.reddit.com/r/cpp/.rss"],\
                    ["ycombinator.xml", "http://news.ycombinator.com/rss"],\
                    ["pipes.xml", "http://pipes.yahoo.com/pipes/pipe.run?_id=biazNR0X3hG3ldiaBBNMsA&_render=rss"])

   # take down the current feed
   socket.setdefaulttimeout(10)

   try:
      for location in SAVE_FEED_TUPLE:
         localfile = save_dir + '/' + location[0]
         feedUrl = location[1]
         print 'Fetching: ', feedUrl

         (filename, headers) = urllib.urlretrieve(feedUrl, localfile)
   except socket.timeout:
      print "Timed out on url:", feedUrl

def main():
   ''' 
   Entry point for the stand-alone program
   '''
   from optparse import OptionParser

   parser = OptionParser()
   parser.add_option("-d", "--directory", dest="directory", 
                     help="Root Directory is DIR", metavar="DIR")
   (options, args) = parser.parse_args()

   if options.directory == None:
      parser.print_help()
      sys.exit()

   root_dir = options.directory
   save_dir = createdir(root_dir)
   if save_dir != None:
      fetch(save_dir)

# "main" body
if __name__ == '__main__':
   main()
