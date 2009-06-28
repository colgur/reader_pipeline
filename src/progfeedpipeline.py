#!/usr/bin/env python

'''NLTK learning
'''

# Imports
import sys, nltk, re, pprint

# Global Variables

# Class Declarations

# Function Declarations
def getcontent(tokens):
   '''
   Use NLTK to drive off stopwords
   '''
   stopwords = nltk.corpus.stopwords.words('english')
   content = [w for w in tokens if w.lower() not in unicode(stopwords)]
   longcontent = [w for w in content if len(w) > 3]

   return longcontent

def topcontent(tokens):
   '''
   Use NLTK to discover the top ten most frequent terms
   '''
   content = getcontent(tokens)

   fdist = nltk.FreqDist(content)
   vocab = fdist.keys()

   return vocab[:50]

def contentfraction(tokens):
   '''
   Sample function from NLTK section 2.4.1
   '''
   from decimal import Decimal

   content = getcontent(tokens)

   return Decimal(len(content)) / Decimal(len(tokens))

def tokenize(feedsetfile):
   '''
   Use NLTK to tokenize titles from Feed Set
   '''
   import feedaggregator

   feedset = feedaggregator.copyexistingfeeds(feedsetfile)
   titletokens = []
   for (title, link) in feedset:
      tokens = nltk.word_tokenize(title)
      titletokens.extend(tokens)

   return titletokens

def getpicklefile():
   '''
   Parse for the Persistent Feed Set
   '''
   from optparse import OptionParser
   from os.path import exists

   parser = OptionParser()
   parser.add_option("-f", "--file", dest="filename",
                     help="Persistent Feed Set FILE", metavar="FILE")
   (options, args) = parser.parse_args()

   if options.filename == None:
      parser.print_help()
      sys.exit()

   if not exists(options.filename):
      print 'No such file: ', options.filename
      sys.exit()

   return options.filename

def main():
   ''' 
   Entry point for the stand-alone program
   '''
   picklefile = getpicklefile()
   tokens = tokenize(picklefile)
   fraction = contentfraction(tokens)
   mostfrequent = topcontent(tokens)

   print 'content fraction: ' + str(fraction)
   print 'top ten: '
   pprint.pprint(mostfrequent)

# "main" body
if __name__ == '__main__':
    main()
