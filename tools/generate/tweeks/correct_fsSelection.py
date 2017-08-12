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
__copyright__ = "Copyright 2017 Stevan White"
__date__ = "$Date: 2015/06/02 21:02:21 $"
__version__ = "$Revision: 1.9 $"

__doc__ = """Sets the OpenType 'OS/2' table fsSelection bitfield:
	USE_TYPO_METRICS bit to True.
	ITALIC bit to True for Italic or Oblique faces (per the docs).
	OBLIQUE bit to True for Oblique faces (per the docs).

	A cludge to work around some misunderstandings in FontForge.
"""
from sys import argv, stdout, stderr
from OpenType.fontdirectory import getDirectoryEntriesByTag
from OpenType.requiredtables import OS_2Table

argc = len( argv )

if argc > 1:
	filePath = argv[argc - 1]
	if not filePath:
		print( "Usage: python correct_fsSelection <filename>", file=stdout )
		sys.exit( 1 )

try:
	#FIXME this is very clumsy, reading the whole file in and writing it
	# to set a single bit.  The structure is there to do it better,
	# I just ran out of time.

	infile = open( filePath, 'r+b' )
	buf = bytearray( infile.read() )

	entries_by_tag = getDirectoryEntriesByTag( buf )


	entry = entries_by_tag[ 'OS/2' ]
	pt = OS_2Table( buf, entry.offset )
	# big-endian: bit 0 is at the beginning
	ITALIC           = 0b0000000000000001
	USE_TYPO_METRICS = 0b0000000010000000
	OBLIQUE          = 0b0000001000000000
	pt.fsSelection = pt.fsSelection | USE_TYPO_METRICS
	# Offical OpenType docs say of the ITALIC flag:
	# "Font contains italic or oblique characters"
	if "Italic" in filePath or "Oblique" in filePath:
		pt.fsSelection = pt.fsSelection | ITALIC
	# "Font contains oblique characters"
	if "Oblique" in filePath:
		pt.fsSelection = pt.fsSelection | OBLIQUE
	ts = pt.getTableSize()
	ptbuf = bytearray( ts )
	pt.writeInto( ptbuf )
	pt = OS_2Table( ptbuf, 0 )
	off = entry.offset

	pt.writeInto( buf, off )

	infile.close()

	outfile = open( filePath, 'wb' )
	#print( "Correcting OS/2 fsSelection bits in file", filePath )
	outfile.write( str( buf ) )
	outfile.flush()
except Exception as e:
	print( "correct_fsSelection, file ", filePath, file=stderr )
	print( e, file=stderr )
	exit( 1 )
exit( 0 )
