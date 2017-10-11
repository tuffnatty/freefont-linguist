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
__copyright__ = "Copyright 2012, 2015, 2017 Stevan White"
__date__ = "$Date: 2015/06/02 21:02:24 $"
__version__ = "$Revision: 1.12 $"

__doc__ = """ Supporting superclasses of font tables, with base classes
implementing automatic generation of internal named structures and code
format strings for output.
"""

from .fielddesc import FieldDesc
from struct import Struct, calcsize
from collections import namedtuple
from checksum import BigEndian32BitList

def registerStructFields( cls ):
	""" Decorator for subclasses of Table; associates members of the
	structure defined in _field_desc with class members via the _fdlist
	member.
	"""
	cls._fdlist = FieldDesc.buildList( cls._field_desc )
	return cls

def _setup_structs( cls ):
	#FIXME REALLY need to warn programmer if decorator is not present
	# otherwise they get nasty recursions
	""" Decorator for all basic subclasses of Table. 
	    Initializes class internal variables based on the class variables
	    _name (must be unique to class) and
	    _fdlist, a list of FieldDesc constructor argument lists. 
	    Seems to run *after* the rest of the class members are initialized.
	    1) makes class members _layout, _size, _structtype if not present.
	    2) from class' _fdlist member, entry in a _layout entry for this
	       class' name, and calculates _size
	    3) generates a program for string formatting of current object
	    4) compiles program and puts in  _strcode
	"""
	if not '_layout' in cls.__dict__:
		cls._layout = {}
	if not '_size' in cls.__dict__:
		cls._size = 0
	if not '_structtype' in cls.__dict__:
		cls._structtype = []
	#print cls._classname()
	structname = cls._classname() + 'struct'
	structdef = FieldDesc.structdefs( cls._fdlist )
	cls._layout[cls._classname()] = Struct( structdef )
	cls._size += calcsize( structdef )
	#cls._size += cls._layout[cls._classname()].size()
	namelist = FieldDesc.namelist( cls._fdlist )
	cls._structtype.append( namedtuple( structname, namelist ) )
	strfmt = FieldDesc.formatstring( cls._name, cls._fdlist )
	cls._strcode = compile( 'self._astr = ' + strfmt, '<string>', 'exec' )
	return cls

class BaseTable( object ):
	"""Base class of font tables.
		Much magic.  Intent is to render tables to such a degree
		as possible to be objects whose members are set by
		field descriptions.
	"""

	@classmethod
	def _classname( cls ):
		return cls.__name__.rpartition( '.' )[2]

	def __init__( self, buf, offset = 0 ):
		""" Idea is to override the member access functions, so that
		font structure fields come from an implementation struct,
		which can be replaced on the fly. 
		"""
		self._offset = offset
		#print self.__class__
			#FIXME need to calculate offset
		#print "unpacking: " + str( self._structtype )
		vals = self._layout[self.__class__.__name__].unpack_from( buf, offset )
		structconstructor = self._structtype[0]
		self.__dict__['_struct'] = structconstructor( *vals )
		# Note __dict__ is an auto member--other proper members
		# are items in __dict__.  Here, avoid the use of __setitem__
		# by explicitly placing _struct in __dict__.

	def __getattr__( self, name ):
		if name in self.__dict__:	#don't override proper members
			return self.__dict__[name]
		if not '_struct' in self.__dict__:
			raise Exception( "No _struct member: " + str( self ) )
		if name in self._struct.__dict__:
			return self._struct.__dict__[name]
		else:
			raise KeyError( "item " + name + " not found" )

	def __setattr__( self, name, value ):
		if( '_struct' in self.__dict__
		and name in self.__dict__['_struct'] ):
			self._struct.name = value
		else:
			self.__dict__[name] = value

	def __getitem__( self, key ):
		return self._struct[key]

	def __setitem__( self, key, value ):
		self._struct[key] = value

	def __str__( self ):
		self._astr = ''
		if hasattr( type(self), '_strcode' ): # class member
			#print( "in str - class:", str( type(self)._strcode ) )
			exec( type(self)._strcode )
		elif hasattr( self, '_strcode' ): # object member
			#print( "in str - obj:", str( self._strcode ) )
			exec( self._strcode )
		else:
			self._astr = repr( self )
		return self._astr

	def getOffset( self ):
		return self._offset

	def getSize( self ):
		#FIXME some tables change size, so this won't work for them
		thestruct = self._layout[self.__class__.__name__]
		return thestruct.size

	def writeInto( self, buf, offset=0 ):
		#FIXME some tables change size, so this won't work for them
		thestruct = self._layout[self.__class__.__name__]
		vals = [ self.__getattr__( i.name  ) for i in self._fdlist ]
		res = thestruct.pack_into( buf, offset, *vals )
		return res

	def getChecksum( self ):
		wL = BigEndian32BitList()
		for desc in self._field_desc:
			key = desc[0]
			val = self.__getattr__( key )
			size = FieldDesc.size_OT_type( desc[1] )
			#print( "size val key", size, val, key )
			wL.accumVal( val, size )
		return wL.get32BitSum()

class Table( BaseTable ):

	def __init__( self, buf, offset = 0 ):
		BaseTable.__init__( self, buf, offset )

	@classmethod
	def getTableSize( cls ):
		return cls._size

	@classmethod
	def getFieldDesc( cls ):
		return cls._fdlist

class VariableSizedTable( BaseTable ):
	def __init__( self, buf, offset = 0 ):
		_setup_structs( self )
		BaseTable.__init__( self, buf, offset )

	def getTableSize( self ):
		return self._size

	def getFieldDesc( self ):
		return self._fdlist

class ReferredTable( Table ):
	@classmethod
	def getTableName( cls ):
		return _tag;

class TableRecord( Table ):
	def __init__( self, buf, parent, index ):
		self._itemno = index + 1
		self._parent = parent
		offset = parent.getOffset() + parent.getTableSize() + index * type(self)._size
		Table.__init__( self, buf, offset )

	def getItemNo( self ):
		#FIXME what if order of items is changed in parent?
		return self._itemno

	def getParentTable( self ):
		return self._parent

class StructArrayTable( VariableSizedTable ):
	"""Table that contains a variable-sized array of other tables. 
	The "size" of such a table is thus more complex:
	Has "getHeaderSize", "getTotalSize"
	"""
	def __init__( self, filebuf, offset ):
		VariableSizedTable.__init__( self, filebuf, offset )
		self._items = []
		if not getattr( self, '_item_type' ):
			raise Exception(
			"Subclasses must set _item_type class member" )

	def getItemSize( self ):
		return self._item_type.getTableSize()

	def getNumItems( self ):
		raise Exception( "Subclasses must override" )

	def getItems( self, filebuf ):
		if not self._items:
			size = self.getTableSize()
			self._readItems( filebuf, size + self._offset )
		return self._items

	def getItem( self, filebuf, idx ):
		self.getItems( filebuf )
		if self._items:
			return self._items[idx]
		else:
			raise Exception( 'Got no items.' )

	def _readItems( self, filebuf, start ):
		item_size = self.getItemSize()
		for i in range( self.getNumItems() ):
			sr = self._item_type( filebuf, start + item_size * i )
			self._items.append( sr )

	#@classmethod
	def getTableHeaderSize( cls ):
		return cls.getTableSize()

class NestedStructTable( BaseTable ):
	"""Table that contains a fixed mixture of primitive and named structs. 
	I think in OpenType, the structs always appear last in such a mixed
	situation, so that assumption is reflected here.

	WORK IN PROGRESS
	"""
	def __init__( self, buf, offset = 0 ):
		""" Idea is to override the member access functions, so that
		font structure fields come from an implementation struct,
		which can be replaced on the fly. 
		"""
		raise Exception( "Not implemented" )
		self._offset = offset
		BaseTable.__init__( self, filebuf, offset )
		#print self.__class__
			#FIXME need to calculate offset
		#print "unpacking: " + str( self._structtype )
		for desc in self._field_desc:
			vals = self._layout[self.__class__.__name__].unpack_from( buf, offset )
		structconstructor = self._structtype[0]
		self.__dict__['_struct'] = structconstructor( *vals )
		# Note __dict__ is an auto member--other proper members
		# are items in __dict__.  Here, avoid the use of __setitem__
		# by explicitly placing _struct in __dict__.

	def getItemSize( self ):
		return self._item_type.getTableSize()

	#@classmethod
	def getTableHeaderSize( cls ):
		return cls.getTableSize()

class SimpleArrayTable( VariableSizedTable ):
	""" An array of primitive types (ints, etc).
	Subclasses indicate a primitive type with the _item_type class member.
	"""
	def __init__( self, filebuf, offset ):
		VariableSizedTable.__init__( self, filebuf, offset )
		self._items = ()
		if not hasattr( self, '_item_type' ):
			raise Exception(
			'Subclasses must set _item_type class member' )
		if not FieldDesc.has_type_symbol( self._item_type ):
			raise Exception( '_item_type not a known simple type' )

	def getItems( self, filebuf ):
		if not self._items:
			size = self.getTableSize()
			self._readItems( filebuf, size + self._offset )
		return self._items

	def _readItems( self, filebuf, start ):
		item_size = FieldDesc.size_OT_type( self._item_type )
		item_format = FieldDesc.type_to_format( self._item_type )
		fmt_str = '>' + str( self.getNumItems() ) + item_format
		self._items = struct.unpack_from( fmt_str, filebuf, start )

	def getItem( self, filebuf, idx ):
		self.getItems( filebuf )
		return self._items[ idx ]

	def getTableHeaderSize( cls ):
		return cls.getTableSize()

class TableOffsetArrayTable( SimpleArrayTable ):
	_item_type = 'uint16'
	def __init__( self, filebuf, offset ):
		SimpleArrayTable.__init__( self, filebuf, offset )
		if not getattr( self, '_reference_type' ):
			raise Exception(
			"Subclasses must set _reference_type class member" )

	def getReferencedItems( self, filebuf ):
		return [ self.getReferencedItem( filebuf, i )
				for i in range( self.getNumItems() ) ]	

	def getReferencedItem( self, filebuf, idx ):
		off = self.getItem( filebuf, idx )
		return self._reference_type( filebuf, self._offset + off )

