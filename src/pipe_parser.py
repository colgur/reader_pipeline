#!/usr/bin/env python

'''
Universal FeedParser Learning
'''

# Imports
import sys
import logging

# Global Variables

# Class Declarations

# Function Declarations
def print_title_keywords(title):
   "Ignore the 'common' words in each title"
   # Look up (case insensitive) each (stemmed) word in title
   # if there is a hit in "common word" list then drop it and move on
   try:
      import nltk
   except ImportError:
      logging.critical("Require NLTK stopwords")
      return

   stopwords = nltk.corpus.stopwords.words('english')
   content = [w for w in title if w.lower() not in stopwords]

   print_title = 'keywords:'
   for entity in content:
      print_title = ' '.join((print_title, entity))

   print print_title

def print_feed_titles(filename):
   "Simple iteration of feed titles"
   try:
      import feedparser
   except ImportError:
      logging.critical("Require feedparser module")
      return

   pipe_feed = feedparser.parse(filename)
   for entry in pipe_feed.entries:
      original = ' '.join(('original:', entry.title))
      print original
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
