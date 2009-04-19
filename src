#!/usr/bin/env python

'''
Created on Apr 12, 2009

@author: crc
'''
import urllib
import socket

socket.setdefaulttimeout(10)

pipes_url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=biazNR0X3hG3ldiaBBNMsA&_render=rss'
local_file = '/home/crc/builds/Apollo/programming_pipe.xml'

try:
   (filename, headers) = urllib.urlretrieve(pipes_url, local_file)
except socket.timeout:
   print "Timed out on url:", pipes_url

