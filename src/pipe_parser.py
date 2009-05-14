#!/usr/bin/env python

'''
Universal FeedParser Learning
'''

# Imports
import sys

# Global Variables

# Class Declarations

# Function Declarations
def is_stopword(title_entity):
   stopwords = ('a', 'about', 'above', 'above', 'across', 'after', \
                'afterwards', 'again', 'against', 'all', 'almost', \
                'alone', 'along', 'already', 'also','although',\
                'always','am','among', 'amongst', 'amongst', \
                'amount',  'an', 'and', 'another', 'any','anyhow',\
                'anyone','anything','anyway', 'anywhere', 'are', \
                'around', 'as',  'at', 'back','be','became', \
                'because','become','becomes', 'becoming', 'been', \
                'before', 'beforehand', 'behind', 'being', 'below', \
                'beside', 'besides', 'between', 'beyond', 'bill', \
                'both', 'bottom','but', 'by', 'call', 'can', 'cannot', \
                'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', \
                'describe', 'detail', 'do', 'done', 'down', 'due', \
                'during', 'each', 'eg', 'eight', 'either', 'eleven',\
                'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', \
                'ever', 'every', 'everyone', 'everything', 'everywhere', \
                'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', \
                'first', 'five', 'for', 'former', 'formerly', 'forty', \
                'found', 'four', 'from', 'front', 'full', 'further', 'get', \
                'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', \
                'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', \
                'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', \
                'hundred', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', \
                'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', \
                'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', \
                'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', \
                'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', \
                'name', 'namely', 'neither', 'never', 'nevertheless', 'next', \
                'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', \
                'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', \
                'once', 'one', 'only', 'onto', 'or', 'other', 'others', \
                'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own',\
                'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', \
                'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', \
                'she', 'should', 'show', 'side', 'since', 'sincere', 'six', \
                'sixty', 'so', 'some', 'somehow', 'someone', 'something', \
                'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', \
                'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', \
                'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', \
                'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third', \
                'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', \
                'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', \
                'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', \
                'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', \
                'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', \
                'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', \
                'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', \
                'whom', 'whose', 'why', 'will', 'with', 'within', 'without', \
                'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves', 'the')
   for stopword in stopwords:
      # Being lazy here and coercing stopwords
      unistopword = unicode(stopword)
      if unistopword == title_entity:
         return 1

   return 0

def print_title_keywords(title):
   "Ignore the 'common' words in each title"
   # Look up (case insensitive) each (stemmed) word in title
   # if there is a hit in "common word" list then drop it and move on
   titlearray = title.split()

   print_title = 'keywords:'
   for entity in titlearray:
      if is_stopword(entity) == 0:
         print_title = ' '.join((print_title, entity))

   print print_title

def print_feed_titles(filename):
   "Simple iteration of feed titles"
   import feedparser
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
