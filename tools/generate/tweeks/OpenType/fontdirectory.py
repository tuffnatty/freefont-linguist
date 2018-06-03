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
__version__ = "$Revision: 1.7 $"

__doc__ = """ Classes representing the basic OpenType/TrueType Font
	Directory tables.
"""
from .table import Table, registerStructFields, _setup_structs
from .typeutils import int_to_tag

""" OpenType/TrueType font directory tables.
"""
@_setup_structs
@registerStructFields
class OffsetTable( Table ):
	_name = 'Offset'
	_field_desc = [
		( 'sfnt_ver',      'int32',  'Fixed' ),
		( 'numTables',     'uint16', ),
		( 'searchRange',   'uint16', ),
		( 'entrySelector', 'uint16', ),
		( 'rangeShift',    'uint16', ),
		]

@_setup_structs
@registerStructFields
class DirectoryEntry( Table ):
	_name = 'Entry'
	_field_desc = [
		( 'tag',      'uint32',  'tag' ),
		( 'checkSum', 'uint32',  'hex'),
		( 'offset',   'uint32', ),
		( 'length',   'uint32', ),
		]

	def getTagStr( self ):
		return int_to_tag( self.tag )

	def getIndex( self ):
		return self._index

	def __init__( self, buf, entryIndex ):
		self._index = entryIndex
		offset = OffsetTable._size + self._index * DirectoryEntry._size
		Table.__init__( self, buf, offset )

def getDirectoryEntriesByTag( filebuf ):
	if len( filebuf ) == 0:
		raise Exception( "Buffer appears to be empty!" )

	ot = OffsetTable( filebuf )

	entries = {}
	for i in range( 0, ot.numTables ):
		de = DirectoryEntry( filebuf, i )
		entries[int_to_tag(de.tag)] = de

	return entries
