#!/usr/bin/env python

'''
Universal FeedParser Learning
'''

# Imports
import sys

# Global Variables

# Class Declarations

# Function Declarations
def print_title_keywords(title):
   "Ignore the 'common' words in each title"
   # Look up (case insensitive) each (stemmed) word in title
   # if there is a hit in "common word" list then drop it and move on

def print_feed_titles(filename):
   "Simple iteration of feed titles"
   import feedparser
   pipe_feed = feedparser.parse(filename)
   for entry in pipe_feed.entries:
      print "original: " << entry.title
      print_title_keywords(entry.title)

def main():
   "Working through simple parse tree navigation"
   from optparse import OptionParser

   parser = OptionParser()
   parser.add_option("-f", "--file", dest="filename",
                     help="Read Pipe Output from FILE", metavar="FILE")
   (options, args) = parser.parse_args()

   if options.filename == None:
      parser.print_help()
      sys.exit()

   print_feed_titles(options.filename)

# "main" body
if __name__ == '__main__':
   main()
