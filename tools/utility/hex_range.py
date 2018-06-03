#!/usr/bin/env python
from __future__ import print_function
__license__ = """
This file is part of GNU FreeFont.

GNU FreeFont is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

GNU FreeFont is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
GNU FreeFont.  If not, see <http://www.gnu.org/licenses/>. 
"""
__author__ = "Stevan White"
__email__ = "stevan.white@googlemail.com"
__copyright__ = "Copyright 2009, 2010, 2011 Stevan White"
__date__ = "$Date$"
__version__ = "$Revision$"

__doc__ = """Sends to standard output a range of hex values formatted
    for e.g. HTML.
    Takes one or two numerical arguments.  With one argument the output
    is just the formatted value of the argument.
"""

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

def explain_error_and_quit( e=None ):
	if e:
		print( 'Error:', e )
	print( "Usage:" )
	print( "       hex_range num1 [num2]" )
	sys.exit( 1 )

def print_formatted_hex_value( n ):
	hexstr = '{0}{1:04x}{2}'.format( prefix, n, postfix )
	print( hexstr )

if len( sys.argv ) == 3:
	try:
		a = int( sys.argv[1], 0 )
		b = int( sys.argv[2], 0 )
		for i in range( a, b + 1 ):
			print_formatted_hex_value( i )
	except ValueError as e:
		explain_error_and_quit( e )
elif len( sys.argv ) == 2:
	try:
		a = int( sys.argv[1], 0 )
		print_formatted_hex_value( a )
	except ValueError as e:
		explain_error_and_quit( e )
else:
		explain_error_and_quit()

