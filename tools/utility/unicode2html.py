#!/usr/bin/env python
from __future__ import print_function
from sys import argv, exit, stdout, stderr
import codecs
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
__copyright__ = "Copyright 2013, 2017, 2018 Stevan White"
__date__ = "$Date:: 2015-05-20 22:15:23 +0200#$"
__version__ = "$Revision: 2589 $"

__doc__ = """
Prints to standard output a stream of HTML (SGML) entity strings
corresponding to Unicode in the input file.

Purpose is to see clearly what characters are in a string of Unicode,
and to put them into the text of an HTML file in that clearly readable form.

This is a hack.
"""

def explain_error_and_quit( e = False ):
	if e:
		print( 'Error:', e, file=sterr )
	print( "Usage:", file=stderr )
	print( "       unicode2html filename", file=stderr )
	print( "       where filename is the name of a UTF8-encoded text file",
		file=stderr )
	exit( 1 )

def formatted_hex_value( n ):
	return '%s%0.4x%s' %( "&#x", n, ";" )

def print_HTML_versions_of_utf8( infile ):
	for line in infile:
		for char in line.strip():
			stdout.write( formatted_hex_value( ord( char ) ) )
		stdout.write( '\n' )

if len( argv ) == 2:
	try:
		fileName = argv[1]
		f = codecs.open( fileName, 'r', encoding='utf_8' )
		print_HTML_versions_of_utf8( f )
	except ValueError as e:
		explain_error_and_quit( e )
else:
	explain_error_and_quit()
