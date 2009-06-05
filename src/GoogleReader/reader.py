#!/usr/bin/env python

''' Interfaces with Google Reader database
- based on accepted answer in StackOverflow article 52880
- references from GoogleReaderAPI (http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
'''

# Imports
import logging
import urllib
import urllib2

# Global Variables

# Class Declarations
class GoogleReader:
   ''' Based on GoogleReader from GoogleReaderAPI 
   (http://code.google.com/p/pyrfeed/wiki/GoogleReaderAPI)
   '''
   URI_LOGIN = 'https://www.google.com/accounts/ClientLogin'
   URI_READER = 'http://www.google.com/reader/'
   URI_API = URI_READER + 'api/0/'
   URI_ATOM = URI_READER + 'atom/'

   PREFERENCE = 'preference/list'
   SUBSCRIPTION = 'subscription/list'
   TAG = 'tag/list'
   UNREAD_COUNT = 'unread-count'

   ATOM_STATE = 'state/com.google/'
   STATE_READING = ATOM_STATE + 'reading-list'

   def __init__(self, login=None, password=None):
      self._login=login
      self._password=password
      self._header = {}

   def identity(self, login, password):
      '''Provide log-in info
      '''
      self._login=login
      self._password=password

   def login(self):
      ''' Authenticate user and return corresponding header
      '''
      if self._login==None or self._password==None:
         return

      auth_url = self.URI_LOGIN
      auth_req_data = urllib.urlencode({'Email': self._login, 'Passwd': self._password})
      auth_req = urllib2.Request(auth_url, data=auth_req_data)
      auth_resp = urllib2.urlopen(auth_req)
      auth_resp_content = auth_resp.read()

      auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
      SID = auth_resp_dict["SID"]

      # Create a cookie in the header using the SID
      self._header['Cookie'] = 'Name=SID;SID=%s;Domain=.google.com;Path=/;Expires=160000000000' % SID

   def request(self, url):
      ''' Generic URL request
      '''
      reader_req = urllib2.Request(url, None, self._header)
      reader_resp = urllib2.urlopen(reader_req)
      reader_resp_content = reader_resp.read()

      return reader_resp_content

   def listapi(self, function):
      ''' List API accessor
      '''
      reader_url = '%s%s' % (self.URI_API, function)

      response = self.request(reader_url)
      return response

   def get_preferences(self):
      ''' Convenient access to Preferences
      '''
      parameters = urllib.urlencode({'output': 'xml'})
      function = '%s?%s' % (self.PREFERENCE, parameters)
      content = self.listapi(function)

      return content

   def get_subscriptions(self):
      ''' Convenient access to Subscriptions
      '''
      parameters = urllib.urlencode({'output': 'xml'})
      function = '%s?%s' % (self.SUBSCRIPTION, parameters)
      content = self.listapi(function)

      return content

   def get_unreadcount(self):
      ''' Convenient access to Count of Unread
      '''
      parameters = urllib.urlencode({'output': 'xml'})
      function = '%s?%s' % (self.UNREAD_COUNT, parameters)
      content = self.listapi(function)

      return content

   def get_readinglist(self, count):
      ''' Pull atom of unread feed items
      '''
      # Atom set of items via http://www.google.com/reader/atom/
#      reader_base_url = 'http://www.google.com/reader/atom/user/%s/state/com.google/reading-list'
#      reader_url = reader_base_url % (user)
      parameters = urllib.urlencode({'n': str(count)})
      function = '%s?%s' % (self.STATE_READING, parameters)
      reader_url = '%s%s%s' % (self.URI_ATOM, 'user/13259633724732126029/', function)

      response = self.request(reader_url)
      return response

# Function Declarations
