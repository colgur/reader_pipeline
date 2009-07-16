#!/usr/bin/env python

'''Package some convenient NLTK processing'''

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
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.corpus import stopwords

# Global Variables
__ignored_words__ = stopwords.words('english')

# Class Declarations
class ProgWordPunctTokenizer(RegexpTokenizer):
   def __init__(self):
      RegexpTokenizer.__init__(self, r'[\w+#]+|[^\w\s]+')

class Content:
   ''''''
   def __init__(self, locale='enlish'):
      self.ignored_words = stopwords.words(locale)

   def words(self, tokens):
      ''' Use NLTK to drive off stopwords '''
      content = [w for w in tokens if w.lower() not in unicode(self.ignored_words)]
      longcontent = [w for w in content if len(w) > 3]
   
      return longcontent

# Function Declarations
def extend_ignored_words(custom_words):
   '''Use this instead of the dictionary '''
   __ignored_words__.extend(custom_words)

def get_content(tokens):
   ''' Use NLTK to drive off stopwords '''
   content = [w for w in tokens if w.lower() not in unicode(__ignored_words__)]
   longcontent = [w for w in content if len(w) > 3]

   return longcontent

def content_fraction(tokens):
   ''' Sample function from NLTK section 2.4.1 '''
   from decimal import Decimal

   content = get_content(tokens)
   return Decimal(len(content)) / Decimal(len(tokens))

def collocations(tokens, num=20, window_size=2):
   ''' Adopted from nltk.Text method by the same name'''
   from nltk.collocations import BigramCollocationFinder, bigram_measures
   finder = BigramCollocationFinder.from_words(tokens, window_size)
   finder.apply_freq_filter(2) 
   finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in __ignored_words__) 

   return finder.nbest(bigram_measures.likelihood_ratio, num) 

def top_content(tokens):
   ''' Use NLTK to discover the top ten most frequent terms '''
   content = getcontent(tokens)

   fdist = nltk.FreqDist(content)
   vocab = iter(fdist.keys())

   words = {}
   frequency = 0
   while frequency < 50:
      try:
         word = vocab.next()
      except StopIteration:
         break

      word_lower = word.lower()
      if word_lower in words:
         words[word_lower] = words[word_lower] + fdist[word]
      else:
         words[word_lower] = fdist[word]

      frequency = frequency + 1

   printable_output = []
   for word in words:
      output_str = '%s : %d' % (word, words[word])
      printable_output.append(output_str)

   return printable_output

# "main" body
if __name__ == '__main__':
   pass

progwordpunct_tokenize = ProgWordPunctTokenizer().tokenize
