#!/usr/bin/env python

'''
Module Documentation
'''

# Imports
import sys

# Global Variables

# Class Declarations

# Function Declarations

def fetch(localfile):
   ''' 
   Take down Yahoo Pipes feed and store for post-processing
   '''

   import urllib
   import socket

   PIPESURL = 'http://pipes.yahoo.com/pipes/pipe.run?_id=biazNR0X3hG3ldiaBBNMsA&_render=rss'

   socket.setdefaulttimeout(10)

   try:
      (filename, headers) = urllib.urlretrieve(PIPESURL, localfile)
   except socket.timeout:
      print "Timed out on url:", PIPESURL

def main():
   ''' 
   Entry point for the stand-alone program
   '''
   from optparse import OptionParser

   parser = OptionParser()
   parser.add_option("-f", "--file", dest="filename", 
                     help="Write Pipe Output to FILE", metavar="FILE")
   (options, args) = parser.parse_args()

   if options.filename == None:
      parser.print_help()
      sys.exit()

   fetch(options.filename)

# "main" body
if __name__ == '__main__':
   main()
