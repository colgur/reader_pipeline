#!/usr/bin/env python

''' Build a new Label Cloud from Feed Title Corpus
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
import re, logging
from repo.google.reader import *
from visualizations.labelcloud.models import User, Label

# Global Variables

# Class Declarations

# Function Declarations
def create_feedset(feed_seq):
   ''' Call on Google Reader with subscription request
   and create a set of (title, link) pairs: a Feed Set '''
   import nltk
#   import pickle
#   f = open('/home/crc/tmp/apollo.pkl', 'rb')
#   feedset = pickle.load(f)
#   f.close()

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
         title = nltk.clean_html(entry.title)
         # actually want 'id' here in order to Edit
         feedset.append((title, entry.id))

   logging.info("Done")
   return feedset

def tokenize(feedset):
   ''' Use NLTK to tokenize titles from Feed Set '''
   from utils.nlp import progwordpunct_tokenize

   titletokens = []
   for (title, id) in feedset:
      tokens = progwordpunct_tokenize(title)
      titletokens.extend(tokens)

   return titletokens

def clear_labels(username):
   '''Query Data Model for any existing Labels'''
   logging.info("Clearing existing Labels")
   user_list = User.objects.all()
   current_user = None

   user_pattern = '%s%s%s' % ('^', username, '$')
   user_re = re.compile(user_pattern)

   # Should probably loop a different way here: no sense continuing once User is located
   for eachuser in user_list:
      user_match = user_re.match(eachuser.name)
      if user_match is not None:
         current_user = eachuser

   if current_user is None:
      return current_user

   label_list = current_user.label_set.all()
   for eachlabel in label_list:
      edit.remove_label(eachlabel)

   label_list.delete()

   logging.info("Done")
   return current_user

def apply_labels(db_user, feed_tokens, feedset):
   '''Label Feed Items in Google Reader'''
   from utils.nlp import Content
   feed_content = Content()

   logging.info("Calculating Top Content")
   top_content = feed_content.top(feed_tokens, lowest_rank=20)
   for eachlabel in top_content:
      label_str = eachlabel
      uri_str = '%s%s%s' % (access.URI_VIEW, 'user/-/label/', eachlabel)
      freq_str = feed_content.frequency(eachlabel)
      db_user.label_set.create(label=label_str, uri=uri_str, frequency=freq_str)
      for (title, id) in feedset:
         r = re.compile(eachlabel, re.I).search(title)
         if r is not None:
            logging.info("Labeling '%s' as '%s'", id, label_str)
            edit.add_label(eachlabel, id)
   logging.info("Done")

   logging.info("Calculating Collocations")
   collocations = feed_content.collocations(feed_tokens)
   for eachtuple in collocations:
      for (title, id) in feedset:
         phrase = '%s%s%s' % (eachtuple[0], ' ', eachtuple[1])
         r = re.compile(phrase).search(title)
         if r is not None:
            label = '%s%s%s' % (eachtuple[0], '_', eachtuple[1])
            edit.add_label(label, id)
   logging.info("Done")

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

   feed_tokens = tokenize(feedset)

   db_user = clear_labels(username)
   apply_labels(db_user, feed_tokens, feedset)

if __name__ == '__main__':
   main()
