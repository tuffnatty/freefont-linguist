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
__date__ = "$Date$"
__version__ = "$Revision$"

__doc__ = """ Classes for TrueType font cmap tables.
"""
from .table import Table, _setup_structs, registerStructFields, TableRecord

_cmap_subtable_common = [
	( 'format',   'uint16', None, 'Format number' ),
]
_cmap_0_fields = [
	( 'length',   'uint16', None, 'length of subtable in bytes' ),
	( 'language', 'uint16', None, '' ),
	( 'glyphIdArray', 'string[256]', None, 'maps char code to glyph IDs' )
]
_cmap_2_fields = [
	( 'length',   'uint16', None, 'length of subtable in bytes' ),
	( 'language', 'uint16', None, '' ),
	( 'subHeaderKeys', 'uint16[256]', None, 'maps hi bytes to subheaders' ),
	( 'subHeaders', 'uint16[5]', None, 'maps hi bytes to subheaders', 4 ),
	( 'glyphIndexArray', 'uint16', None, 'maps hi bytes to subheaders' )
	]
_cmap_4_fields = [
	( 'length',   'uint16', None, 'length of subtable in bytes' ),
	( 'language', 'uint16', None, '' ),
	( 'secCountX2', 'uint16', None, 'segCount x 2' ),
	( 'searchRange', 'uint16', None, '2x(2^floor( log_2( segCount ) ) )' ),
	( 'entrySelector', 'uint16', None, 'log_2( searchRange / 2 )' ),
	( 'rangeShift', 'uint16', None, '2 x segCount - searchRange' ),
	]
_cmap_6_fields = [
	( 'length',   'uint16', None, 'length of subtable in bytes' ),
	( 'language', 'uint16', None, '' ),
	( 'firstCode', 'uint16', None, 'first character code' ),
	( 'entryCount', 'uint16', None, 'number of character codes' ),
	( 'glyphIdArray', 'uint16[]', None, 'char code glyph index array' ),
	]
_cmap_8_fields = [
	( 'reserved',   'uint16', None, 'reserved; set to 0' ),
	( 'length', 'uint32', None, 'byte length subtable and header' ),
	( 'language', 'uint32', None, '' ),
	( 'is32', 'byte[8192]', None, 'each shows if index is 32 bit char' ),
	( 'nGroups', 'uint32', None, 'number of groups to follow' ),
	]
_cmap_10_fields = [
	( 'reserved',   'uint16', None, 'set to 0' ),
	( 'length',   'uint32', None, 'byte length of subtable and header' ),
	( 'language', 'uint32', None, '' ),
	( 'startCharCode', 'uint32', None, 'first character code' ),
	( 'numChars', 'uint32', None, 'number of character codes' ),
	( 'glyphs', 'uint16', None, 'char code glyph index array' ),
	]
_cmap_12_fields = [
	( 'reserved',   'uint16', None, 'set to 0' ),
	( 'length',   'uint32', None, 'byte length of subtable and header' ),
	( 'language', 'uint32', None, '' ),
	( 'nGroups', 'uint32', None, 'number of groups to follow' ),
	]
_cmap_13_fields = [
	( 'reserved',   'uint16', None, 'set to 0' ),
	( 'length',   'uint32', None, 'byte length of subtable and header' ),
	( 'language', 'uint32', None, '' ),
	( 'nGroups', 'uint32', None, 'number of groups to follow' ),
	]
_cmap_14_fields = [
	( 'length',   'uint32', None, 'byte length of subtable and header' ),
	( 'numVarSelectorRecords', 'uint32', None,
		'number of variation selector records' ),
	]

@_setup_structs
@registerStructFields
class cmapSubtable( Table ):
	_name = 'cmap_generic_subtable'
	_field_desc = _cmap_subtable_common
	_further_field_desc = []

	def _copy( self ):
		self.format = other.format

""" Format 0: byte encoding table """
@_setup_structs
@registerStructFields
class cmap0Subtable( cmapSubtable ):
	_name = 'cmap_0'
	_further_field_desc = [
	( 'glyphIdArray', 'string[256]', None, 'maps char code to glyph IDs' )
	]

""" Format 2: high-byte mapping through table.
	For CJK encodings."""
@_setup_structs
@registerStructFields
class cmap2Subtable( cmapSubtable ):
	_name = 'cmap_2'
	_further_field_desc = [
	( 'subHeaderKeys', 'uint16[256]', None, 'maps hi bytes to subheaders' ),
	"""
	( 'subHeaders', 'uint16[4]', None, 'maps hi bytes to subheaders' ),
	( 'glyphIndexArray', 'uint16', None, 'maps hi bytes to subheaders' )
	"""
	]
	#FIXME lots of problems with this.  Immediately followed by two arrays.
	def __init__( self, buf, offset = 0 ):
		raise CMAPTableException( "Unsupported 'cmap' subtable type 2" )

class cmap2Subheader( TableRecord ):
	_name = 'cmap_2_subheader'
	_field_desc = [
	( 'firstCode', 'uint16', None, 'first "valid" low byte for subheader' ),
	( 'entryCount', 'uint16', None, 'num "valid" low bytes for subheader' ),
	( 'idDelta', 'int16', None, 'complicated' ),
	( 'idRangeOffset', 'uint16', None, 'complicated' ),
	]

def _cmap4variable_fields( sc ):
	return [
	( 'endCount', 'uint16', None, 'End character code for segments', sc ),
	( 'reservedPad', 'uint16', None, 'padding set to 0' ),
	( 'startCount', 'uint16', None, 'Start char code for segments', sc ),
	( 'idDelta', 'int16', None, 'Delta for char codes in segment', sc ),
	( 'idRangeOffset', 'uint16', None, 'Offsets of glyphIdArray or 0', sc ),
	( 'glyphIdArray', 'uint16', None, 'Glyph index array', '[]'),
	]

""" Format 4: segment mapping to delta values """
@_setup_structs
@registerStructFields
class cmap4Subtable( cmapSubtable ):
	_name = 'cmap_4'
	_further_field_desc = [
	( 'secCountX2', 'uint16', None, 'segCount x 2' ),
	( 'searchRange', 'uint16', None, '2x(2^floor( log_2( segCount ) ) )' ),
	( 'entrySelector', 'uint16', None, 'log_2( searchRange / 2 )' ),
	( 'rangeShift', 'uint16', None, '2 x segCount - searchRange' ),
	]
	def __init__( self, buf, offset = 0 ):
		TableRecord.__init__( self, buf, offset )
		sc = self.segCountX2 / 2

""" Format 6: trimmed table mapping """
@_setup_structs
@registerStructFields
class cmap6Subtable( cmapSubtable ):
	_name = 'cmap_6'
	_further_field_desc = [
	( 'secCountX2', 'uint16', None, 'segCount x 2' ),
	( 'searchRange', 'uint16', None, '2x(2^floor( log_2( segCount ) ) )' ),
	( 'entrySelector', 'uint16', None, 'log_2( searchRange / 2 )' ),
	( 'rangeShift', 'uint16', None, '2 x segCount - searchRange' ),
	]
	def __init__( self, buf, offset = 0 ):
		TableRecord.__init__( self, buf, offset )
		sc = self.segCountX2 / 2

""" Format 8: mixed 16-bit and 32-bit coverage """
@_setup_structs
@registerStructFields
class cmap8Subtable( cmapSubtable ):
	_name = 'cmap_8'
	_further_field_desc = [
	( 'startCharCode', 'uint32', None, '1st char code of group.' ),
	( 'endCharCode', 'uint32', None, 'last char code in group' ),
	( 'startGlyphID', 'uint32', None, 'glyph index of start char code' ),
	]
	def __init__( self, buf, offset = 0 ):
		TableRecord.__init__( self, buf, offset )

""" Format 10: trimmed array """
@_setup_structs
@registerStructFields
class cmap10Subtable( cmapSubtable ):
	_name = 'cmap_10'
	_further_field_desc = []
	def __init__( self, buf, offset = 0 ):
		TableRecord.__init__( self, buf, offset )

""" Format 12: segmented coverage """
@_setup_structs
@registerStructFields
class cmap12Subtable( cmapSubtable ):
	_name = 'cmap_12'
	_further_field_desc = [
	( 'startCharCode', 'uint32', None, '1st char code of group.' ),
	( 'endCharCode', 'uint32', None, 'last char code in group' ),
	( 'startGlyphID', 'uint32', None, 'glyph index of start char code' ),
	]
	def __init__( self, buf, offset = 0 ):
		TableRecord.__init__( self, buf, offset )

""" Format 13: last resort font """
@_setup_structs
@registerStructFields
class cmap13Subtable( cmapSubtable ):
	_name = 'cmap_13'
	_further_field_desc = [
	( 'startCharCode', 'uint32', None, '1st char code of group' ),
	( 'endCharCode', 'uint32', None, 'last char code in group' ),
	( 'glyphID', 'uint32', None, 'glyph index of chars in range' ),
	]
	def __init__( self, buf, offset = 0 ):
		TableRecord.__init__( self, buf, offset )

""" Format 14: Unicode variation sequences """
""" Mysterious phrase:
	"Unicode Variation Sequences supported by the font may be specified in
	the cmap table only under platform ID 0 and encoding ID 5, using a
	format 14 cmap subtable."
"""
@_setup_structs
@registerStructFields
class cmap14Subtable( cmapSubtable ):
	_name = 'cmap_14'
	_further_field_desc = [
	( 'varSelector', 'uint24', None, 'variation selector' ),
	( 'defaultUVSOffset', 'uint32', None,
		'offset to Default UVS Table, or 0' ),
	( 'nonDefaultUVSOffset', 'uint32', None,
		'offset to Non-Default UVS Table, or 0' ),
	]
	def __init__( self, buf, offset = 0 ):
		TableRecord.__init__( self, buf, offset )

class cmapSubtableFactory( object ):
	_subtable_versions = {
		0: cmap0Subtable,
		2: cmap2Subtable,
		4: cmap4Subtable,
		6: cmap6Subtable,
		8: cmap8Subtable,
		10: cmap10Subtable,
		12: cmap12Subtable,
		13: cmap13Subtable,
		14: cmap14Subtable,
	}
	def make( self, buf, offset ):
		base = cmapSubtable( buf, offset )
		if not base.version in _subtable_versions:
			raise CMAPTableException( 
			"Unknown 'cmap' table version: " + str( base.version ) )
		constr = cmapSubtableFactory._subtable_versions[base.version]
		return constr( base, buf, offset )

