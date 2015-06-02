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
__copyright__ = "Copyright 2012, 2015 Stevan White"
__date__ = "$Date: 2015/06/02 21:02:24 $"
__version__ = "$Revision: 1.5 $"

__doc__ = """ Utilities for handling OpenType/TrueType data types.
"""

from datetime import date, timedelta

"""Returns a string representation of a TrueType 4-character tag """
def int_to_tag( val ):
	c = ( chr( ( val >> 24 ) & 0x000000FF ),
	      chr( ( val >> 16 ) & 0x000000FF ),
	      chr( ( val >> 8 ) & 0x000000FF ),
	      chr( ( val ) & 0x000000FF ) )
	return ''.join( c )

"""Returns a string representation of a TrueType Fixed-point (16.16)
number """
def fixed_str( val ):
	ct = ( val >> 16 )
	cb = ( val ) & 0xFFFF
	return "%i.%u" % ( ct, cb )

_truetype_start_date = date( 1904, 1, 1 )
"""Returns a Python date object from a 64-bit signed TrueType longdatetime """
def longdatetime2date( ldt ):
	delta = timedelta( seconds = ldt )
	return delta + _truetype_start_date

def bitfield2str( val, fieldlen = 16 ):
	s = [ str( ( val >> i ) & 1 ) for i in range( 0, fieldlen ) ]
	return ''.join( s )

def panose_str( val ):
	v = str( val )
	s = [ str( ord( v[i] ) ) for i in range( 0, 10 ) ]
	return '|'.join( s ) 
