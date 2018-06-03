#!/usr/bin/python

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
__email__ = "stevan.white@gmail.com"
__copyright__ = "Copyright 2017, 2018 Stevan White"
__date__ = "$Date:: 2013-04-09 12:44:41 +0200#$"
__version__ = "$Revision: 1.5 $"

__doc__ = """
Makes a dictionaries of characters in a local text file
	UnicodeData.txt
obtainable from unicode.org, which has fields:
	"codept", "uname", "cat", "comb", "bidi", "dcmp",
	"deci", "digi", "num", "mir", "U1", "cmmt", "uppr", "lowr", "titl" 
Provides lookup methods for some of these.

Note the Python unicodedata module should do all of this and more:
	https://docs.python.org/2/library/unicodedata.html
However, the Python 2.7 implementation covers only Unicode 5.1, and at the
time of this writing, the Python 3 implementation covers only to Unicode 8. 
I wonder why so old?
"""

import re
from sys import argv, exit, stdout as out, stderr as err

def _explain_error_and_quit( e='' ):
	if e:
		print( 'Error {%s}'.format( e ), file=err )
	print( 'Usage', file=err )
	print( '       unicodedata [filepath]', file=err )
	exit( 1 )

_charlineRe = '^([A-F0-9]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);' 

_charline = re.compile( _charlineRe )

fields = ( "codept", "uname", "cat", "comb", "bidi", "dcmp",
	"deci", "digi", "num", "mir", "U1", "cmmt", "uppr", "lowr", "titl" )

class character:
	def __init__( self, *arglist ):
		self.vals = zip( fields, arglist )
		for i in range( len( fields ) ):
			self.__dict__[fields[i]] = arglist[i]
		self.unicodeval = int( self.codept, 16 )
		self.name = self.uname

	def __str__( self ):
		return "U+{0:s} {1:s}".format( self.codept, self.name )

class controlchar(character):
	def __init__( self, *arglist ):
		character.__init__(self, *arglist )
		self.name = self.U1

class rangestartchar(character):
	def __init__( self, *arglist ):
		character.__init__(self, *arglist )
		self.name = self.uname[1:-8]

class rangeendchar(character):
	def __init__( self, *arglist ):
		character.__init__(self, *arglist )
		self.name = self.uname[1:-7]

def makeCharacter( *arglist ):
	codept = arglist[ 0 ]
	name = arglist[ 1 ]

	if name == "<control>":
		return controlchar( *arglist )
	elif name.endswith(", First>"):
		return rangestartchar( *arglist )
	elif name.endswith(", Last>"):
		return rangeendchar( *arglist )
	else:
		return character( *arglist )

def build_charsByUnicode( f ):
	charsByUnicode = {}
	for line in f:
		m = line.split( ';' )
		
		if len( m ) < 14:
			print( str( len( m ) ), file=err )
			print( "didn't find all fields in line:\n%s"
						% (line), file=err )
		else:
			c = makeCharacter( *m )
			charsByUnicode[c.unicodeval] = c
	return charsByUnicode

class characters:
	def __init__( self ):
		self._charsByUnicode = None

	def _build( self, filename='UnicodeData.txt' ):
		f = open( filename )
		if not f:
			print( 'UnicodeData.txt should be in current directory.'
					, file=err )
			exit( 1 )
		self._charsByUnicode = build_charsByUnicode( f )

	def byUnicode( self ):
		if not self._charsByUnicode:
			self._build()
		return self._charsByUnicode

_characters = characters()

def _char_arg_OK( character ):
	if isinstance( character, unicode ):
		if len( character ) == 1:
			return True
		else:
			raise Exception( "expected string of length 1, got "
				+ str( len( character ) ) )
	else:
		raise Exception( "expected unicode string of length 1, got "
				+ str( type( character ) ) )
	return False

def combining( character ):
	if _char_arg_OK( character ):
		charsByUnicode = _characters.byUnicode()
		cp = ord( character )
		if cp in charsByUnicode:
			return int( charsByUnicode[cp].comb )
	return 0

_comb_char_cls = ( 'Mc', 'Mn', 'Me' )

def is_combining_character( character ):
	""" See Uncode Standard ch 3 Conformance, sect 3.6 Combination.
	"""
	if _char_arg_OK( character ):
		charsByUnicode = _characters.byUnicode()
		cp = ord( character )
		if cp in charsByUnicode:
			return ( ( charsByUnicode[cp].cat in _comb_char_cls )
				or ( combining( character ) > 0 ) )
	return False

def name( character ):
	if _char_arg_OK( character ):
		charsByUnicode = _characters.byUnicode()
		cp = ord( character )
		if cp in charsByUnicode:
			return charsByUnicode[cp].name
	raise ValueError( "Character not found." )

def category( character ):
	if _char_arg_OK( character ):
		charsByUnicode = _characters.byUnicode()
		cp = ord( character )
		if cp in charsByUnicode:
			return charsByUnicode[cp].cat
	raise ValueError( "Character not found." )

def lookup( name ):
	if isinstance( name, str ) and len( str ) > 0:
		charsByName = _characters.byName()
		if cp in charsByName:
			return charsName[cp]
		else:
			raise ValueError( "Name not found in Unicode "
					+ name )
	raise Exception( "Expected nonempty string for name." )

"""
if err.isatty():
	filename = 'UnicodeData.txt'

	if len( argv ) == 2:
		filename = argv[1]
	if len( argv ) > 2:
		_explain_error_and_quit()
	initialize( filename )

	for cp in sorted( _charsByUnicode ):
		#print( str( charsByUnicode[cp] ) )
		c = _charsByUnicode[cp]
		print( str( c ) )
		#out.write( "\tcategory=" + c.cat )
		#if c.uppr:
		#	out.write( "\tuc_is=" + c.uppr )
		#if c.lowr:
		#	out.write( "\tlc_is=" + c.lowr )
		#if c.cat == "Mc":
		#	out.write( "\tis_combining(" + c.cat + ")" )
		if c.comb != '0':
			out.write( "\tcombining_type(" + c.comb + ")" )
		out.write( "\n" )

#out.write( str( len( charsByUnicode ) ) + "\n" )
"""
