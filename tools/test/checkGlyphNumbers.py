#!/usr/bin/fontforge -script 
__license__ = """
This file is part of Gnu FreeFont.

Gnu FreeFont is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Gnu FreeFont is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Gnu FreeFont.  If not, see <http://www.gnu.org/licenses/>. 
"""
__author__ = "Stevan White"
__email__ = "stevan.white@googlemail.com"
__copyright__ = "Copyright 2009, 2010, Stevan White"
__date__ = "$Date$"
__version__ = "$Revision$"

__doc__ = """
For most unicode ranges, glyph slot numbers should be the same as the
Unicode value.
The Private Use ranges are the exception: those characters should have a
definate non-Unicode number: -1

This script checks that this is the case, and prints out a warning
whenever it isn't.
"""

import fontforge
import sys

problem = False

def inPrivateUseRange( glyph ):
	e = glyph.encoding

	return ( ( e >= 0xE800 and e <= 0xF8FF )
	    or ( e >= 0xFF000 and e <= 0xFFFFD )
	    or ( e >= 0x100000 and e <= 0x10FFFD ) )

def isSpecialTrueType( glyph ):
	""" Fontforge treats three control characters as the special 
	TrueType characters recommended by that standard
	"""
	e = glyph.encoding

	return e == 0 or e == 1 or e == 0xD

def checkGlyphNumbers( dir, fontFile ):
	print "Checking slot numbers in " + fontFile
	font = fontforge.open( dir + fontFile )

	g = font.selection.all()
	g = font.selection.byGlyphs

	valid = True
	for glyph in g:
		if isSpecialTrueType( glyph ):
			# FIXME really should complain if it DOESNT exist
			pass
		elif inPrivateUseRange( glyph ):
			if glyph.unicode != -1:
				print "Glyph at slot " + str( glyph.encoding ) \
					+ " is Private Use but has Unicode"
				problem = True
		else:
			if glyph.encoding != glyph.unicode:
				print "Glyph at slot " + str( glyph.encoding ) \
					+ " has wrong Unicode"
				problem = True

checkGlyphNumbers( '../sfd/', 'FreeSerif.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeSerifItalic.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeSerifBold.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeSerifBoldItalic.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeSans.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeSansOblique.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeSansBold.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeSansBoldOblique.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeMono.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeMonoOblique.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeMonoBold.sfd' )
checkGlyphNumbers( '../sfd/', 'FreeMonoBoldOblique.sfd' )

if problem:
	sys.exit( 1 )
