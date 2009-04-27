#!/usr/bin/env python

'''
Module Documentation
'''

# Imports
import sys

# Global Variables

# Class Declarations

# Function Declarations
def createdir(rootDir):
   '''
   Create directory name based on current time and root directory name
   '''
   import time
   import os
   import errno

   # build the Save Directory name from the current time + root
   utcSec = time.time()
   utc = time.gmtime(utcSec)
   dirName = time.strftime("%Y%m%d_%H%M", utc)
   saveDir = rootDir + '/' + dirName

   try:
      os.makedirs(saveDir)
   except OSError, e:
      if os.error.errno != errno.EEXIST:
         print "Failed to Create Save Dir: ", e
         saveDir = None

   return(saveDir)

def fetch(saveDir):
   ''' 
   Take down the various feeds and store them according to a set pattern,
   usually for later processing
   '''
   import urllib
   import socket

   saveFeedTuple = (['digg.xml', 'http://feeds.digg.com/digg/topic/programming/popular.rss'],\
                    ["reddit_prog.xml", "http://www.reddit.com/r/programming/.rss"],\
                    ["delicious.xml", "http://feeds.delicious.com/v2/rss/popular/programming?count=15"],\
                    ["reddit_cpp.xml", "http://www.reddit.com/r/cpp/.rss"],\
                    ["ycombinator.xml", "http://news.ycombinator.com/rss"])

   # take down the current feed
   socket.setdefaulttimeout(10)

   try:
      for location in saveFeedTuple:
         localFile = saveDir + '/' + location[0]
         feedUrl = location[1]
         (filename, headers) = urllib.urlretrieve(feedUrl, localFile)
   except socket.timeout:
      print "Timed out on url:", pipes_url


def main():
   from optparse import OptionParser

   parser = OptionParser()
   parser.add_option("-d", "--directory", dest="directory", 
                     help="Root Directory is DIR", metavar="DIR")
   (options, args) = parser.parse_args()

   if options.directory == None:
      parser.print_help()
      sys.exit()

   rootDir = options.directory
   saveDir = createdir(rootDir)
   if saveDir != None:
      fetch(saveDir)

# "main" body
if __name__ == '__main__':
   main()
