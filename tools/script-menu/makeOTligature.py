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
__copyright__ = "Copyright 2015, 2018 Stevan White"
__date__ = "$Date::                           $"
__version__ = "$Revision$"

__doc__ = """
For use from the FontForge Script Menu.
Add it to the Scripts Menu using the Preferences dialog.

Sets the OpenType glyph class of the selected range of slots to 'baseligature'

Detailed info is printed to standard output (see by launching FontForge
from a console).
"""
import fontforge

def explain_error_and_quit( e ):
	if e:
		print( 'Error:', e )
	exit( 1 )

try:
	glyphs = fontforge.activeFont().selection.byGlyphs
	for g in glyphs:
		print( "setting", g.glyphname, 'glyph class to', 'baseligature' )
		g.glyphclass = 'baseligature'
except ValueError, e:
	explain_error_and_quit( e )

