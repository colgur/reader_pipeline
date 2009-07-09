#!/usr/bin/env python

'''NLTK pipeline based on Google Reader feed(s)
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
   pat = re.compile('http://.*$')
   feedset = []
   for eachfeed in feed_seq:
      feed_str = eachfeed.id()
      result = pat.search(feed_str)
      if result is not None:
         logging.info("Refreshing %d from '%s'...", 
                      eachfeed.unread_count(), 
                      result.group())
      eachfeed.refresh()
      logging.info("Parsing...")
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
   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s : %(message)s',
                       datefmt='%H:%M:%S')

   try:
      (username, password) = parse_credentials()
   except ValueError:
      sys.exit()

   reader_feeds = atom.feeds(username, password)
   feedset = create_feedset(reader_feeds)

   logging.info('Analyzing Feed Titles')

   tokens = tokenize(feedset)
   fraction = contentfraction(tokens)
   mostfrequent = topcontent(tokens)

   logging.info('Done!')

   print 'content fraction: ' + str(fraction)
   print 'top fifty: '
   for each_term in mostfrequent:
      print each_term

# "main" body
if __name__ == '__main__':
   main()
