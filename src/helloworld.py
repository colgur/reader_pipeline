#!/usr/bin/env python

'''Test out AppEngine installation'''

# Imports
import cgi
import os
import logging
import datetime

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

# Global Variables

# Class Declarations
class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
  def get(self):
     try:
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)
     except:
        logging.error('Error retrieving posts from the datastore')

     if users.get_current_user():
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
     else:
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'

     template_values = {'greetings': greetings,
                        'url': url,
                        'url_linktext': url_linktext,
                        }

     path = os.path.join(os.path.dirname(__file__), 'index.html')
     self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
   def post(self):
     logging.debug('Start guestbook signing request')

     greeting = Greeting()

     if users.get_current_user():
        logging.info('Signed by user %s' % users.get_current_user().nickname())
        greeting.author = users.get_current_user()
     else:
        logging.info('Signed by anonymous user')

     greeting.content = self.request.get('content')
     greeting.date = datetime.datetime.now()
     try:
        greeting.put()
     except:
        logging.error('There was an error saving comment %s' % self.request.get('content'))

     logging.debug('Finish guestbook signing')
     self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook)],
                                     debug=True)

# Function Declarations
def main():
   logging.getLogger().setLevel(logging.DEBUG)
   run_wsgi_app(application)

# "main" body
if __name__ == '__main__':
   main()

