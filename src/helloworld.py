#!/usr/bin/env python

'''Test out AppEngine installation'''

# Imports
import cgi
import os, sys
import logging
import datetime

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from user import pipeline

# Global Variables

# Class Declarations
class MainPage(webapp.RequestHandler):
  def get(self):
     self.redirect('./user', True)

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/user', pipeline.UserPipeline)],
                                     debug=True)

# Function Declarations
def main():
   sys.path.insert(0, 'nltk-0_9_9.zip')
   logging.getLogger().setLevel(logging.DEBUG)
   run_wsgi_app(application)

# "main" body
if __name__ == '__main__':
   main()

