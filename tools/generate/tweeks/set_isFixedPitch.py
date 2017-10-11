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
__copyright__ = "Copyright 2012, 2015 Stevan White"
__date__ = "$Date: 2015/06/02 21:02:21 $"
__version__ = "$Revision: 1.9 $"

__doc__ = """Sets the OpenType 'post' table flag 'isFixedPitch' to True.
	A cludge to work around some misunderstandings in FontForge.
"""
from sys import argv, stdout as out, stderr as err, exit
from OpenType.fontdirectory import getDirectoryEntriesByTag
from OpenType.requiredtables import postTable, headTable
from OpenType.checksum import get_file32Bit_checkSumAdjustment

argc = len( argv )

if argc > 1:
	filePath = argv[argc - 1]
	if not filePath:
		print( "Usage: python set_isfixedpitch <filename>", file=err )
		exit( 1 )

try:
	#FIXME this is very clumsy, reading the whole file in and writing it
	# to set a single bit.  The structure is there to do it better,
	if not "Mono" in filePath:
		exit( 1 )

	infile = open( filePath, 'r+b' )
	buf = bytearray( infile.read() )

	entries_by_tag = getDirectoryEntriesByTag( buf )

	entry = entries_by_tag[ 'post' ]
	t = postTable( buf, entry.offset )
	# ======================= TEST
	#print( "post checksum-orig", hex( entry.checkSum ) )
	cs = t.getChecksum()
	#print( "post checksum-calc", hex( cs ) )
	# =======================
	t.isFixedPitch = True

	t.writeInto( buf, entry.offset )
	# =======================

	entry.checkSum = t.getChecksum()
	entry_off = entry.getOffset()	# offset to directory entry itself
	entry.writeInto( buf, entry_off )	# write into dir. entry buffer

	infile.close()

	print( "Setting 'post' flag 'isFixedPitch'", filePath )

	entry = entries_by_tag[ 'head' ]
	ht = headTable( buf, entry.offset )
	ht.checkSumAdjustment = 0
	entry.checkSum = ht.getChecksum()
	ht.writeInto( buf, entry.offset )

	outfile = open( filePath, 'wb' )
	outfile.write( str( buf ) )
	outfile.flush()

	csa = get_file32Bit_checkSumAdjustment( filePath )
	outfile = open( filePath, 'wb' )
	ht.checkSumAdjustment = csa
	ht.writeInto( buf, entry.offset )
	outfile.write( str( buf ) )
	outfile.flush()

except Exception as e:
	print( "set_isfixedpitch, file ", filePath, file=err )
	print( e, file=err )
	print( "set_isfixedpitch, file ", filePath, file=out )
	print( e, file=out )
	exit( 1 )
exit( 0 )
