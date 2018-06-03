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
__copyright__ = "Copyright 2017, 2018 Stevan White"
__date__ = "$Date: 2015/06/02 21:02:24 $"
__version__ = "$Revision: 1.12 $"

__doc__ = """ Utilities for calculating 32-bit checksums of table fields.
This assumes the tables are padded with zeros to 32 bits.
"""
from ctypes import c_uint64, c_uint32, c_uint16, c_uint8, c_ubyte

PANOSE = c_ubyte * 10

class BigEndian32BitList:
	""" Breaks up fields into bytes in big-endian fashion, and adds them
	to a list of 32-byte integers also in big-endian fashion.
	"""
	def __init__( self ):
		self._byte_count = 0
		self._wordList = []

	def accumVal( self, val, size ):
		""" Pushes a value onto the current 32 bit integer of the
		list, making a new integer entry when needed.
		For 10-byte PANOSE entries, order of entries is not changed.
		(Only the order of bits within the bytes is affected by
		endianness.)
		"""
		if size == 1:
			v = 0xFF & c_ubyte( val ).value
			self.addByteVal( v )
		elif size == 2:
			v = c_uint16( val ).value
			for b in range( 0, size ):
				shift = 8 * ( size - b - 1 )
				self.accumByte( 0xFF & ( v >> shift ) )
		elif size == 4:
			v = c_uint32( val ).value
			for b in range( 0, size ):
				shift = 8 * ( size - b - 1 )
				self.accumByte( 0xFF & ( v >> shift ) )
		elif size == 8:
			v = c_uint64( val ).value
			for b in range( 0, size ):
				shift = 8 * ( size - b - 1 )
				self.accumByte( 0xFF & ( v >> shift ) )
		elif size == 10:
			for i in range( 0, size ):
				v = ord( val[i] )
				#print( "FLAG",  "{0:d}".format( v ) )
				self.accumByte( 0xFF & v )
		else:
			raise Exception( "Unexpected size {}".format( size ) )

	def accumByte( self, val ):
		""" Pushes a byte value onto the current 32 bit integer of the
		list, making a new integer entry when needed.
		Records the count of bytes thus pushed.
		(Unless the count is a mult of 4, this is different from 1/4
		the number of entries in the word list.)
		"""
		if self._byte_count % 4 == 0:
			self._wordList.append( 0 )
		byte_off = ( 3 - self._byte_count ) % 4
		
		new_byte = int( val ) << ( byte_off * 8 )
		#print( "new_byte", new_byte )
		self._wordList[-1] |= new_byte
		self._byte_count += 1

	def get32BitSum( self ):
		""" Returns the 32-bit truncated unsigned sum of the unsigned
		integers in the list.
		"""
		checksum = 0
		for w in self._wordList:
			checksum = 0xFFFFFFFF & ( checksum + w )
		return checksum

from numpy import fromfile, uint32, uint64

def get_file32Bit_checkSumAdjustment( f ):
	""" See the OpenType spec
		"The OpenType Font File"
		section
		"Calculating Checksums"
	"""
	a = fromfile( f, dtype='>u4', count=-1 )
	#FIXME I can't tell from the docs if this is platform-independent or not
	s = uint64( 0 )
	for v in a:
		s += v
	cs = 0xFFFFFFFF & int( s )
	checkSumAdjustment = 0xB1B0AFBA - cs
	return 0xFFFFFFFF & checkSumAdjustment

