#!/usr/bin/python
from __future__ import print_function
import re
from sys import stdout, stderr, argv

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
__date__ = "$Date:: 2017$"
__version__ = "$Revision: 0 $"

__doc__ = """
For each Mark Filter (either "Mark Set" or "Mark Class") in the argument
FontForge SFD file, lists all lookup tables using that Mark Filter.

This is to help manage these filters, in the absence of such services in 
current versions of FontForge.
"""
"""

From the FontForge SFD file format doc:

"the lookup flags field is now a 32 bit number, the low order 16 bits being the traditional flags, and the high order being the mark attachment set index, if any"

The term "traditional flags" means the "lookupFlag" field of the
OpenType Lookup table structure.  The LookupFlag bit enumeration is

	0x0001   rightToLeft
	0x0002   ignoreBaseGlyphs
	0x0004   ignoreLigatures
	0x0008   ignoreMarks 
	0x0010   useMarkFilteringSet
	0x00E0   reserved
	0xFF00   markAttachmentType  (does FontForge provide for setting this?)
"""

markset_re = re.compile( '^"([^"]+)"' )

def gather_mark_filters( filename ):
	""" The mark filter definitions appear in the text of the SFD file
	after those of the lookups, so these have to be gathered first.
	"""
	mark_filters = []
	f = open( filename )
	for line in f:
		if line.startswith( '"' ):
			m = markset_re.match( line )
			if m:
				filter_name = m.group(1)
				mark_filters.append( filter_name )
	f.close()
	return mark_filters

lu_fmt = 'Lookup: (\d+) (\d+) (\d+) "([^"]*)"  {"([^"]*)" (.*)}.*$'
lookup_re = re.compile( lu_fmt )

def get_mark_filter_usage( filename, mark_filters ):
	mark_flt_users = {}
	for flt in mark_filters:
		mark_flt_users[flt] = []
	f = open( filename )
	for line in f:
		if line.startswith( "Lookup:" ):
			m = lookup_re.match( line )
			if m:
				lu_type = m.group(1)
				sfd_lu_flags = m.group(2)
				lu_saveas_afm = m.group(3)
				lu_name = m.group(4)
				st_name = m.group(5)
				rest = m.group(6)

				flags = int( sfd_lu_flags )
				mark_flt_i = flags >> 16
				lu_flags = flags & 0xFFFF
				use_mark_filter = lu_flags & 0x0010
				if use_mark_filter:
					mf = mark_filters[mark_flt_i]
					mark_flt_users[mf].append( lu_name )
					#print( bin( lu_flags ), mark_flt_i, mf, lu_name )
	f.close()
	return mark_flt_users

# --------------------------------------------------------------------------
__usage = """Usage:
	list_mark_filters.py sfd_file ...
"""

args = argv[1:]

if len( args ) < 1 or len( args[0].strip() ) == 0:
	print( __usage, file=stderr )
	exit( 0 )

for font_name in args:
	mark_filters = gather_mark_filters( font_name )
	#print( mark_filters )
	mark_flt_users = get_mark_filter_usage( font_name, mark_filters )
	print( "Mark Filter usage in SFD file", font_name )
	for s in mark_filters:
		print( "'{}':".format( s ) )
		for u in mark_flt_users[s]:
			print( "\t", u )
