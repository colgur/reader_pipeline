#!/usr/bin/env python

''' Based on GoogleReader from GoogleReaderAPI 
(http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
'''

# Imports
import logging
import urllib
import urllib2

# Global Variables
URI_LOGIN = 'https://www.google.com/accounts/ClientLogin'
URI_READER = 'http://www.google.com/reader/'
URI_API = URI_READER + 'api/0/'
URI_ATOM = URI_READER + 'atom/'

# Local Variables
_header = {}

# Class Declarations

# Local Function Declarations
def _initcookie(auth_resp_content):
   ''' Parse Reader response to login for session cookie
   '''
   auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
   SID = auth_resp_dict["SID"]

   # Create a cookie in the header using the SID
   _header['Cookie'] = 'Name=SID;SID=%s;Domain=.google.com;Path=/;Expires=160000000000' % SID

# Global Function Declarations
def login(login, password):
   ''' Authenticate user and return corresponding header
   '''
   if login==None or password==None:
      return

   auth_req_data = urllib.urlencode({'Email': login, 'Passwd': password})
   auth_req = urllib2.Request(URI_LOGIN, data=auth_req_data)

   auth_resp = urllib2.urlopen(auth_req)
   auth_resp_content = auth_resp.read()

   _initcookie(auth_resp_content)

def request(url):
   ''' Generic URL request
   '''
   reader_req = urllib2.Request(url, None, _header)
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
