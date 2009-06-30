#!/usr/bin/env python

'''Test out AppEngine installation'''

# Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Global Variables

# Class Declarations
class MainPage(webapp.RequestHandler):
   def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('Hello, webapp World!')

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

# Function Declarations
def main():
   run_wsgi_app(application)

# "main" body
if __name__ == '__main__':
   main()
