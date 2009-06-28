#!/usr/bin/env python

'''NLTK pipeline based on Google Reader feed(s)
'''

# Imports
import logging
import sys, nltk, re, pprint
from repo.google.reader import *

# Global Variables

# Class Declarations

# Function Declarations
def getcontent(tokens):
   ''' Use NLTK to drive off stopwords '''
   stopwords = nltk.corpus.stopwords.words('english')
   content = [w for w in tokens if w.lower() not in unicode(stopwords)]
   longcontent = [w for w in content if len(w) > 3]

   return longcontent

def topcontent(tokens):
   ''' Use NLTK to discover the top ten most frequent terms '''
   content = getcontent(tokens)

   fdist = nltk.FreqDist(content)
   vocab = fdist.keys()

   printable_output = []
   for each_sample in vocab[:50]:
      output_str = '%s : %d' % (each_sample, fdist[each_sample])
      printable_output.append(output_str)

   return printable_output

def contentfraction(tokens):
   ''' Sample function from NLTK section 2.4.1 '''
   from decimal import Decimal

   content = getcontent(tokens)
   return Decimal(len(content)) / Decimal(len(tokens))

def tokenize(feedset):
   ''' Use NLTK to tokenize titles from Feed Set '''
   titletokens = []
   for (title, link) in feedset:
      tokens = nltk.word_tokenize(title)
      titletokens.extend(tokens)

   return titletokens

def create_feedset(feed_seq):
   ''' Call on Google Reader with subscription request
   and create a set of (title, link) pairs: a Feed Set '''
   feedset = []
   for eachfeed in feed_seq:
      eachfeed.refresh()
      pipe_feed = eachfeed.parse()

      for entry in pipe_feed.entries:
         feedset.append((entry.title, entry.link))

   return feedset

def parse_credentials():
   '''Parse login info from options
   '''
   import optparse

   parser = optparse.OptionParser()
   parser.add_option("-u", "--user", dest="username", 
                     help="USER associated with Feed Set", metavar="USER")
   parser.add_option("-p", "--password", dest="password", 
                     help="PWD associated with Feed Set", metavar="PWD")
   (options, args) = parser.parse_args()

   if options.username == None or options.password == None:
      parser.print_help()
      raise ValueError

   return (options.username, options.password)

def main():
   ''' Program entry point '''
   try:
      (username, password) = parse_credentials()
   except ValueError:
      sys.exit()

   reader_feeds = atom.feeds(username, password)
   feedset = create_feedset(reader_feeds)

   tokens = tokenize(feedset)
   fraction = contentfraction(tokens)
   mostfrequent = topcontent(tokens)

   print 'content fraction: ' + str(fraction)
   print 'top fifty: '
   for each_term in mostfrequent:
      print each_term

# "main" body
if __name__ == '__main__':
   main()
