#!/usr/bin/env python

'''
Module Documentation
'''

# Imports

# Global Variables

# Class Declarations

# Function Declarations
def start_element(name, attrs):
    print 'Start element:', name, attrs
def end_element(name):
    print 'End element:', name
def char_data(data):
    print 'Character data:', repr(data)

def main():
   ''' The following program defines three handlers that just print out their arguments.
   '''
   import xml.parsers.expat

   # 3 handler functions
   p = xml.parsers.expat.ParserCreate()

   p.StartElementHandler = start_element
   p.EndElementHandler = end_element
   p.CharacterDataHandler = char_data

   p.Parse("""<?xml version="1.0"?>
   <parent id="top"><child1 name="paul">Text goes here</child1>
   <child2 name="fred">More text</child2>
   </parent>""", 1)

# "main" body
if __name__ == '__main__':
   main()
