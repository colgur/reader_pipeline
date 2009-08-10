#!/usr/bin/env python

''' Based on GoogleReader from GoogleReaderAPI 
(http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
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
import urllib
import urllib2

# Global Variables
URI_LOGIN = 'https://www.google.com/accounts/ClientLogin'
URI_READER = 'http://www.google.com/reader/'
URI_API = URI_READER + 'api/0/'
URI_ATOM = URI_READER + 'atom/'
URI_VIEW = URI_READER + 'view/'

# Local Variables
__header__ = {}
__login__ = ''

# Class Declarations

# Local Function Declarations
def _initcookie(auth_resp_content):
   ''' Parse Reader response to login for session cookie
   '''
   auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
   SID = auth_resp_dict["SID"]

   # Create a cookie in the header using the SID
   __header__['Cookie'] = 'Name=SID;SID=%s;Domain=.google.com;Path=/;Expires=160000000000' % SID

# Global Function Declarations
def login(login, password):
   ''' Authenticate user and return corresponding header
   '''
   if login==None or password==None:
      #TODO: throw
      return

   global __login__
   __login__ = login
   auth_req_data = urllib.urlencode({'Email': login, 'Passwd': password})
   # TODO: Catch HttpError here
   auth_req = urllib2.Request(URI_LOGIN, data=auth_req_data)

   auth_resp = urllib2.urlopen(auth_req)
   auth_resp_content = auth_resp.read()

   _initcookie(auth_resp_content)

def username():
   global __login__
   return __login__

def request(url, data=None):
   ''' Generic URL request
   '''
   reader_req = urllib2.Request(url, data, __header__)
   reader_resp = urllib2.urlopen(reader_req)
   reader_resp_content = reader_resp.read()

   return reader_resp_content

def test():
   ''' Quick and dirty unit testing
   '''
   # Nothing to do: All IO
   pass

# "main" body
if __name__ == '__main__':
   test()
