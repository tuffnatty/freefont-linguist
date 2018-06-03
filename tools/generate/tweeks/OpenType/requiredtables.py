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
__copyright__ = "Copyright 2012, 2015, 2017, 2018 Stevan White"
__date__ = "$Date: 2015/06/02 21:02:23 $"
__version__ = "$Revision: 1.7 $"

__doc__ = """ Classes for the core required OpenType/TrueType font tables.
"""
from .table import Table, _setup_structs, ReferredTable, registerStructFields, TableRecord

@_setup_structs
@registerStructFields
class postTable( ReferredTable ):
	_name = 'post'
	_field_desc = [
		( 'format',             'uint32', 'Fixed' ),
		( 'italicAngle',        'uint32', 'Fixed' ),
		( 'underlinePosition',  'int16', ),
		( 'underlineThickness', 'uint16', ),
		( 'isFixedPitch',       'uint32', 'bool' ),
		( 'minMemType42',       'uint32', ),
		( 'maxMemType42',       'uint32', ),
		( 'minMemType1',        'uint32', ),
		( 'maxMemType1',        'uint32', ),
		]

@_setup_structs
@registerStructFields
class headTable( ReferredTable ):
	_name = 'head'
	_field_desc = [
                ( 'version',            'uint32', 'Fixed' ),
		( 'fontRevision',       'uint32', 'Fixed' ),
		( 'checkSumAdjustment', 'uint32', ),
		( 'magicNumber',        'uint32', 'hex' ),
		( 'flags',              'uint16', 'bitfield' ),
		( 'unitsPerEm',         'uint16', ),
		( 'created',            'int64', 'longdatetime' ),
		( 'modified',           'int64', 'longdatetime' ),
		( 'xMin',               'int16', ),
		( 'yMin',               'int16', ),
		( 'xMax',               'int16', ),
		( 'yMax',               'int16', ),
		( 'macStyle',           'uint16', 'bitfield' ),
		( 'lowestRecPPEM',      'uint16', ) ,
		( 'fontDirectionHint',  'int16', ),
		( 'indexToLocFormat',   'int16', ),
		( 'glyphDataFormat',    'int16', ),
		]

@_setup_structs
@registerStructFields
class hheaTable( ReferredTable ):
	_name = 'hhea'
	_field_desc = [
                ( 'version',             'uint32', 'Fixed' ),
		( 'ascent',              'int16' ),
		( 'descent',             'int16' ),
		( 'linegap',             'int16' ),
		( 'advanceWidthMax',     'uint16' ),
		( 'minLeftSideBearing',  'int16' ),
		( 'minRightSideBearing', 'int16' ),
		( 'xMaxExtent',          'int16' ),
		( 'caretSlopeRise',      'int16' ),
		( 'caretSlopeRun',       'int16' ),
		( 'caretOffset',         'uint16' ),
		( 'reserved1',           'int16' ),
		( 'reserved2',           'int16' ),
		( 'reserved3',           'int16' ),
		( 'reserved4',           'int16' ),
		( 'metricDataFormat',    'int16' ),
		( 'numOfLongHorMetrics', 'uint16' ),
		]

@_setup_structs
@registerStructFields
class maxpTable( ReferredTable ):
	_name = 'maxp'
	_field_desc = [
		( 'version', 'uint32', 'Fixed',
			'0x00010000 (1.0)' ),
		( 'numGlyphs', 'uint16', None,
			'the number of glyphs in the font' ),
		( 'maxPoints', 'uint16', None,
			'points in non-compound glyph' ),
		( 'maxContours', 'uint16', None,
			'contours in non-compound glyph' ),
		( 'maxComponentPoints', 'uint16', None,
			'points in compound glyph' ),
		( 'maxComponentContours', 'uint16', None,
			'contours in compound glyph' ),
		( 'maxZones', 'uint16', None,
			'set to 2' ),
		( 'maxTwilightPoints', 'uint16', None,
			'points used in Twilight Zone (Z0)' ),
		( 'maxStorage', 'uint16', None,
			'number of Storage Area locations' ),
		( 'maxFunctionDefs', 'uint16', None,
			'number of FDEFs' ),
		( 'maxInstructionDefs', 'uint16', None,
			'number of IDEFs' ),
		( 'maxStackElements', 'uint16', None,
			'maximum stack depth' ),
		( 'maxSizeOfInstructions', 'uint16', None,
			'byte count for glyph instructions' ),
		( 'maxComponentElements', 'uint16', None,
			'number of glyphs referenced at top level' ),
		( 'maxComponentDepth', 'uint16', None,
			'levels of recursion, set to 0 if font has only simple glyphs' ),

		]

@_setup_structs
@registerStructFields
class OS_2Table( ReferredTable ):
	""" See https://www.microsoft.com/typography/otspec/os2.htm
	The table changes size depending on its "version" entry.
	This very much complicates reading it.
	Even messier: the names of the fields changes between versions.
	That means, code that refers to the table has to check the version,
	and/or check that it has a given field, in order to use it.
	"""
	_name = 'OS/2'
	_field_desc_0 = [
	( 'version', 'uint16', 'Fixed',         
		'(always 0)' ),
	( 'xAvgCharWidth', 'uint16', None,   
		'Average weighted advance width of lower case letters' ),
	( 'usWeightClass', 'uint16', None,   
		'Glyph visual weight' ),
	( 'usWidthClass', 'uint16', None,    
		'Multiplier of normal glyph aspect ratio (width to height)' ),
	( 'fsType', 'int16', None,  
		'font characteristics and properties' ),
	( 'ySubscriptXSize', 'int16', None,         
		'Horizontal size in pixels of subscripts' ),
	( 'ySubscriptYSize', 'int16', None,         
		'Vertical size in pixels of subscripts' ),
	( 'ySubscriptXOffset', 'int16', None,       
		'Horizontal offset of subscripts' ),
	( 'ySubscriptYOffset', 'int16', None,       
		'Vertical offset from baseline of subscripts' ),
	( 'ySuperscriptXSize', 'int16', None,       
		'Horizontal size in pixels of superscripts' ),
	( 'ySuperscriptYSize', 'int16', None,       
		'Vertical size in pixels of superscripts' ),
	( 'ySuperscriptXOffset', 'int16', None,     
		'Horizontal offset of superscripts from baseline' ),
	( 'ySuperscriptYOffset', 'int16', None,     
		'Vertical offset of superscripts from baseline' ),
	( 'yStrikeoutSize', 'int16', None,  
		'Width of strikeout stroke' ),
	( 'yStrikeoutPosition', 'int16', None,      
		'Offset of strikeout stroke from baseline' ),
	( 'sFamilyClass', 'int16', None,    
		'font-family design classification' ),
	( 'panose', 'PANOSE', 'PANOSE',  
		'Visual characteristics of typeface' ),
	( 'ulUnicodeRange1', 'uint32', 'bitfield',  
		'Low 96 bits specify Unicode blocks supported by font.' ),
	( 'ulUnicodeRange2', 'uint32', 'bitfield',  
		'Low 96 bits specify Unicode blocks supported by font.' ),
	( 'ulUnicodeRange3', 'uint32', 'bitfield',  
		'Low 96 bits specify Unicode blocks supported by font.' ),
	( 'ulUnicodeRange4', 'uint32', 'bitfield',  
		'High 32 bits specify script sets supported by font' ),
	( 'achVendID', 'int32', 'tag',    
		'Font vendor ID' ),
	( 'fsSelection', 'uint16', 'bitfield',     
		'Font patterns info' ),
	( 'usFirstCharIndex', 'uint16', None,
		'Minimum Unicode value in font' ),
	( 'usLastCharIndex', 'uint16', None,
		'Maximum Unicode value in font' ),
	( 'sTypoAscender', 'int16', None,
		'' ),
	( 'sTypoDescender', 'int16', None,
		'' ),
	( 'sTypoLineGap', 'int16', None,
		'' ),
	( 'usWinAscent', 'uint16', None,
		'' ),
	( 'usWinDescent', 'uint16', None,
		'' ),
	]
	_field_desc_0_1 = [
	( 'ulCodePageRange1', 'uint32', 'bitfield',    
		'' ),
	( 'ulCodePageRange2', 'uint32', 'bitfield',    
		'' ),
	]
	_field_desc_1_2 = [
	( 'sxHeight', 'int16', None,
		'' ),
	( 'sxCapHeight', 'int16', None,
		'' ),
	( 'usDefaultChar', 'uint16', None,
		'' ),
	( 'usBreakChar', 'uint16', None,
		'' ),
	( 'usMaxContext', 'uint16', None,
		'' ),
	]
	_field_desc_2_5 = [
	( 'usLowerOpticalPointSize', 'uint16', None,
		'' ),
	( 'usUpperOpticalPointSize', 'uint16', None,
		'' ),
	]
	#FIXME this is valid only for versions 2, 3 and 4 of the OS/2 table
	_field_desc = _field_desc_0 + _field_desc_0_1 + _field_desc_1_2 

@_setup_structs
@registerStructFields
class cmapTable( ReferredTable ):
	_name = 'cmap'
	_field_desc = [
	( 'version', 'uint16', None, 'Set to 0' ),
	( 'numberSubtables', 'uint16', None, 'Number of encoding subtables' ),
	]

	def __init__( self, buf, offset = 0 ):
		self._records = []
		ReferredTable.__init__( self, buf, offset )
		#print "cmapTable " + str( self )
		for i in range( self.numberSubtables ):
			rec = cmapRecord( buf, self, i )
			self._records.append( rec )

	def getRecords( self ):
		return self._records

cmapPlatformIDs = {
		0: "Other",
		1: "Macintosh",
		3: "Windows",
}
""" MS requires at least one format 4 cmap table, with 'platform ID' = 3
	which uses the 'Encoding ID' field, where is interpreted as follows.
"""
cmapEncodingIDs = {
	0: 	'Symbol',	# on Mac, this is default.  
	1: 	'Unicode BMP (UCS-2)', # preferred for Windows fonts
	2: 	'ShiftJIS',
	3: 	'PRC',
	4: 	'Big5',
	5: 	'Wansung',
	6: 	'Johab',
	7: 	'Reserved',
	8: 	'Reserved',
	9: 	'Reserved',
	10: 	'Unicode UCS-4',
}

class CMAPTableException( Exception ):
	pass

@_setup_structs
@registerStructFields
class cmapRecord( TableRecord ):
	_name = 'cmapRecord'
	_field_desc = [
	( 'platformID', 'uint16', None, 'Platform ID' ),
	( 'encodingID', 'uint16', None, 'Platform-specific encoding ID' ),
	( 'offset',     'uint32', None, 'Offset from table start to record' ),
	]

	def getRecordContents():
		return _contents

	def __init__( self, buf, parent, index ):
		self._contents = None
		TableRecord.__init__( self, buf, parent, index )
		if not self.platformID in cmapPlatformIDs:
			raise CMAPTableException(
			"Unknown cmap platform ID in cmap encoding record: "
			+ str( self ) )
		if not self.encodingID in cmapEncodingIDs:
			raise CMAPTableException(
			"Unknown cmap encoding ID in cmap encoding record: "
			+ str( self ) )
		#print str( self )
		self._contents = cmapSubtable( buf, self.offset )

