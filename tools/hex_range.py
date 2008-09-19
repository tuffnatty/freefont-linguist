#!/usr/bin/env python

""" Print out a range of hex values formatted for e.g. HTML.
    Takes one or two numerical arguments.
"""
__author__ = "Stevan White <stevan.white@googlemail.com>"
__date__ = "$Date: 2008-09-19 09:48:19 $"
__version__ = "$Revision: 1.2 $"

import sys

# Python Unicode prefix
prefix = '\\u'
postfix = ''
# General Unicode prefix
prefix = 'U+'
postfix = ''
# HTML Entity
prefix = '&#x'
postfix = ';'

def explain_error_and_quit( e ):
	if e:
		print 'Error: ', e
	print "Usage:"
	print "       hex_range num1 [num2]"
	exit( 1 )

def print_formatted_hex_value( n ):
	print '%s%0.4x%s' %( prefix, n, postfix )

if len( sys.argv ) == 3:
	try:
		a = int( sys.argv[1], 0 )
		b = int( sys.argv[2], 0 )
		for i in xrange( a, b + 1 ):
			print_formatted_hex_value( i )
	except ValueError, e:
		explain_error_and_quit( e )
elif len( sys.argv ) == 2:
	try:
		a = int( sys.argv[1], 0 )
		print_formatted_hex_value( a )
	except ValueError, e:
		explain_error_and_quit( e )
else:
		explain_error_and_quit()

