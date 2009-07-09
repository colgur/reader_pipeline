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
import os
import logging
import nltk

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required

# Global Variables

# Class Declarations

# Function Declarations

class UserPipeline(webapp.RequestHandler):
   @login_required
   def get(self):
      ''' Program entry point '''
      logging.debug('colgur@gmail.com')

      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'

      template_values = {'url': url,
                         'url_linktext': url_linktext}

      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))
#      reader_feeds = atom.feeds('colgur@gmail.com', 'Ck8IDxia')
#      feedset = create_feedset(reader_feeds)
#
#      tokens = tokenize(feedset)
#      fraction = contentfraction(tokens)
#      mostfrequent = topcontent(tokens)

# "main" body
if __name__ == '__main__':
   pass
