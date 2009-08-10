#!/usr/bin/env python

''' Edit API as described in pyrfeed (http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
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
import urllib
from repo.google.reader import access

# Global Variables
SUBSCRIPTION = 'subscription/edit'
EDIT_TAG = 'edit-tag'
DISABLE_TAG = 'disable-tag'
TOKEN = 'token'

# Class Declarations

# Function Declarations
def add_label(label, item):
   token = request(TOKEN)
   label_str = '%s%s' % ('user/-/label/', label)

   params = dict(i = item,
                 a = label_str,
                 ac = 'edit',
                 T = token)

   request(EDIT_TAG, params)

def remove_label(label):
   token = request(TOKEN)
   params = dict(i = label,
                 ac = 'disable-tag',
                 T = token)

   request(DISABLE_TAG, params)

def request(api_id, data=None):
   ''' Helper formats request'''
   function = '%s%s' % (access.URI_API, api_id)
   if data is not None:
      #TODO: throw if username hasn't been set
      client_id = urllib.urlencode(dict(client=access.username()))
      data = urllib.urlencode(data)
      function = '%s?%s' % (function, client_id)

   response = access.request(function, data)
   return response

# "main" body
if __name__ == '__main__':
   pass
