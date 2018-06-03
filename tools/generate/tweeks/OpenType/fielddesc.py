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
__copyright__ = "Copyright 2012, 2015, 2018 Stevan White"
__date__ = "$Date: 2015/06/02 21:02:23 $"
__version__ = "$Revision: 1.3 $"

__doc__ = """ Utility class to translate between TrueType/OpenType table
field descriptors and 'struct' module field descriptors.
that implement automatic generation of internal named structures,
and automatic generation of code format strings for output.
"""

import re

"""
	uint16	offset, glyphID, 
	int16	short, bitfield, f2dot14
	uint32	uint, Fixed, bitfield
	int32	long, bitfield, 4-char tag,
	uint64	long
	int64	longlong, longdatetime
	byte	byte
	char[]	(signed byte... used for strings)
"""
"""
Regarding PANOSE

The OpenType Standard explains:
"The PANOSE definition contains ten digits each of which currently describes up to sixteen variations."

"digits:?  But it's a 10-*byte* field?  Want to call a byte a digit?
OK, but then it would take up to 2^8 = 256 values.
Well, if only half of the bits of each byte are used, that would amount
to 2^4 = 16 different values.
OK, so each byte of this 10-byte field takes hex values 0 through 0xF, and no others.
Still, a funny sort of "digit".

If that is the case, there's no need to worry about the sign bit,
although the OpenType standard says Panose is a uint8[10].
The unsigned-byte and signed-byte interpretation would always be the same.
"""

_pytype_structsym = {
	'byte':    'b',
	'char':    'c',
	'string':  's',
	'uint16':  'H',
	'int16':   'h',
	'uint32':  'L',
	'int32':   'l',
	'uint64':  'Q',
	'int64':   'q',
	# used in MS OpenType docs
	'GlyphID': 'H',
	'Offset':  'H',
	'SHORT':   'h',
	'USHORT':  'H',
	'LONG':    'i',
	'ULONG':   'I',
	'Fixed':   'I',
	'Tag':     'I4',
	'PANOSE':  '10s',
}

_pytype_fmtsym = {
	'uint16': 'u',
	'int16':  'i',
	'uint32': 'u',
	'int32':  'i',
	'uint64': 'u',
	'int64':  'i',
	'string': 's',
	# used in MS OpenType docs
	'GlyphID': 'u',
	'Offset':  'u',
	'SHORT':   'i',
	'USHORT':  'u',
	'LONG':    'i',
	'ULONG':   'u',
	'Fixed':   'u',
	'PANOSE':  '10u',
}
_interp_conv = {
	'longdatetime': 'longdatetime2date',
	'bitfield': 'bitfield2str',
	'Fixed': 'fixed_str',
	'hex': 'hex',
	'tag': 'int_to_tag',
	'bool': 'bool',
	'PANOSE': 'panose_str',
}

_OT_typesize = {
	'byte':   1,
	'char':   1,
	'uint16': 2,
	'int16':  2,
	'uint32': 4,
	'int32':  4,
	'uint64': 8,
	'int64':  8,
	'PANOSE': 10,
}

_type_plurality_re = re.compile( '(\w+)(?:\[(\d\+)\])?' )

class FieldDesc():
	def __init__( self, name, pytype, interp = None, desc = '' ):
		self.name = name
		m = _type_plurality_re.match( pytype )
		self.num = 0
		if m:
			self.pytype = m.group(1)
			if len( m.groups() ) > 2:
				self.num = int( m.group(2) )
			else:
				self.num = 1
		else:
			raise Exception( "can't parse field type:" + pytype )
		self.interp = interp
		self.desc = desc

	@classmethod
	def buildList( cls, fdtuple ):
		return [ FieldDesc( *fd ) for fd in fdtuple ]

	@classmethod
	def structdefs( cls, fielddefs ):
		""" Takes a list of FieldDesc, returns a string
		for 'struct' module Struct constructor and calcsize().
		"""
		deflist = [ '>' ]
		for fd in fielddefs:
			structsym = _pytype_structsym[fd.pytype]
			if fd.num > 1:
				structsym = str( fd.num ) + structsym
			deflist.append( structsym )
		return ' '.join( deflist )

	@classmethod
	def namelist( cls, fielddefs ):
		return ' '.join( [ fd.name for fd in fielddefs ] )

	@classmethod
	def formatstring( cls, tablename, fielddefs ):
		""" From a table name and field definitions, returns a python
		format string, which, when fed corresponding field values 
		produces a human-readable string representing the table.
		"""
		frmt = []
		conv = []
		for fd in fielddefs:
			n = fd.name + ": "
			v = 'self.' + fd.name
			if fd.interp:
				if fd.interp == "Fixed":
					frmt.append( n + '%s' )
				else:
					frmt.append( n + "'%s'" )
				conv.append( _interp_conv[fd.interp] 
					+ '( ' + v + ' )' )
			else:
				frmt.append( n + '%' + _pytype_fmtsym[fd.pytype] )
				conv.append( v )
		frmtstr = tablename + ' = { ' + ', '.join( frmt ) + ' }'
		convstr = ', '.join( conv )
		s = '"%s" %s ( %s )' % ( frmtstr, '%', convstr )
		#print( s )
		return s

	@classmethod
	def has_type_symbol( cls, symb ):
		return symb in _pytype_structsym

	@classmethod
	def type_to_format( cls, symb ):
		return _pytype_structsym[symb]

	@classmethod
	def size_OT_type( cls, symb ):
		return _OT_typesize[symb]
