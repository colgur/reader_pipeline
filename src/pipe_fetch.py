#!/usr/bin/env python

'''
Created on Apr 12, 2009

@author: crc
'''
import sys
import urllib
import socket

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", 
                  help="Write Pipe Output to FILE", metavar="FILE")
(options, args) = parser.parse_args()

if options.filename == None:
   parser.print_help()
   sys.exit()

pipes_url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=biazNR0X3hG3ldiaBBNMsA&_render=rss'
local_file = options.filename

socket.setdefaulttimeout(10)

try:
   (filename, headers) = urllib.urlretrieve(pipes_url, local_file)
except socket.timeout:
   print "Timed out on url:", pipes_url

