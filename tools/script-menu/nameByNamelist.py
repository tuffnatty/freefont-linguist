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
__copyright__ = "Copyright 2013, Stevan White"
__date__ = "$Date:: 2013-04-09 12:44:41 +0200#$"
__version__ = "$Revision: 1.3 $"

__doc__ = """
For use from the FontForge Script Menu.
Add it to the Scripts Menu using the Preferences dialog.

User must provide the full path to a FontForge Namelist file (as produced
by Encodint -> Save Namelist of Font) in the variable nameListFilePath.

Sets the name and unicode values of the selected range of slots to the
encoding equalt to the slot number, and a name looked up in a Namelist
file provided by the user.

If the encoding of a selected glyph is not represented in the file, or
if glyph at the slot has the same name as indicated by the file, nothing
is changed.

Careful! it changes values whether they were previously set or not.

Detailed info is printed to standard output (see by launching FontForge
from a console).
"""
import fontforge

nameListFilePath = '/home/swhite/.FontForge/FreeSerif.nam'

def readNameList( filename ):
	f = open( filename )
	slotName = {}
	for line in f:
		( slot, name ) = line.split()
		slotval = int( slot, 16 )
		slotName[slotval] = name
	return slotName

def explain_error_and_quit( e ):
	if e:
		print 'Error: ', e
	exit( 1 )

try:
	print( 'Re-naming glyphs according to name list ' + nameListFilePath )
	slotName = readNameList( nameListFilePath )
	glyphs = fontforge.activeFont().selection.byGlyphs
	for g in glyphs:
		if g.encoding in slotName:
			newname = slotName[g.encoding]
			if g.glyphname == newname:
				print( "glyph at " + hex( g.encoding )
					+ ' already named ' + newname )
			else:

				print( "naming " + str( g.glyphname )
					+ ' as ' + newname )
				g.glyphname = newname
				g.unicode = g.encoding
		else:
			print ( "slot value " + hex( g.encoding )
				+ ' not found in name list')
except ValueError, e:
	explain_error_and_quit( e )

