#!/usr/bin/env ../utility/fontforge-interp.sh
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
__copyright__ = "Copyright 2016 Stevan White"
__date__ = "$Date:: 2015-05-17 14:48:22 +0200#$"
__version__ = "$Revision: 3050 $"

__doc__ = """
For glyphs in Unicode ranges, the OpenType Glyph Class should usually be 
left automatic, to be determined from the standards.

For glyphs in non-Unicode blocks, it may be important to set the Glyph Class.
(Mark Positoning depends on this, for example.)

This script checks that Unicode glyphs all have Glyph Class "automatic",
and that a zero-width glyph in any other block is *not* "automatic".
"""

import fontforge
import sys

problem = False

def isException( glyph ):
	e = glyph.encoding
	# Malayalam vowels are Mark to allow positioning of subsequent marks.
	return ( e in range( 0x0D3E, 0X0D40 +1 )
                or e in range( 0x0D46, 0x0D4C + 1 ) 
                or e in range( 0x0D57, 0x0D57 + 1 )
                )

def inPrivateUseRange( glyph ):
	e = glyph.encoding

	return ( ( e >= 0xE000 and e <= 0xF8FF )
	    or ( e >= 0xFF000 and e <= 0xFFFFD )
	    or ( e >= 0x100000 and e <= 0x10FFFD ) )

def isSpecialTrueType( glyph ):
	""" Fontforge treats three control characters as the special 
	TrueType characters recommended by that standard
	"""
	e = glyph.encoding

	return e == 0 or e == 1 or e == 0xD

from os import path
def checkOTGlyphClass( fontDir, fontFile ):
	if isinstance( fontFile, ( list, tuple ) ):
		print( "In directory " + fontDir )
		for fontName in fontFile:
			checkOTGlyphClass( fontDir, fontName )
		return

	print( "Checking OpenType Glyph Class in " + fontFile )
	font = fontforge.open( path.join( fontDir, fontFile ) )

	g = font.selection.all()
	g = font.selection.byGlyphs

	valid = True
	for glyph in g:
		if inPrivateUseRange( glyph ):
			if glyph.glyphclass == 'automatic':
				print( "Glyph at slot " + str( glyph.encoding )
					+ " in private use range, marked 'automatic'." )
				problem = True
			elif( glyph.width == 0
			and not glyph.glyphclass in ('mark', 'component', 'noclass' ) ):
				print( "Glyph at slot " + str( glyph.encoding )
					+ " is zero width but isn't a mark or component" )
				problem = True
		else:
			if glyph.glyphclass != 'automatic':
				if isException( glyph ):
					print( "Glyph at slot",
						str( glyph.encoding ),
						"has exceptonal Glyph Class" )
				else:
					print( "Glyph at slot",
						str( glyph.encoding ),
						"has non-automatic Glyph Class" )
				problem = True

# --------------------------------------------------------------------------
args = sys.argv[1:]

if len( args ) < 1 or len( args[0].strip() ) == 0:
	checkOTGlyphClass( '../../sfd/',
		( 'FreeSerif.sfd', 'FreeSerifItalic.sfd',
		'FreeSerifBold.sfd', 'FreeSerifBoldItalic.sfd',
		'FreeSans.sfd', 'FreeSansOblique.sfd',
		'FreeSansBold.sfd', 'FreeSansBoldOblique.sfd',
		'FreeMono.sfd', 'FreeMonoOblique.sfd',
		'FreeMonoBold.sfd', 'FreeMonoBoldOblique.sfd' ) )
else:
	checkOTGlyphClass( args[0], args[1:] )

if problem:
	sys.exit( 1 )
