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
import unicodedata

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

def rprt( glyph, problem ):
	print( "Glyph at slot", glyph.encoding, problem )
markanch = ( 'mark', 'basemark' )
baseanch = ( 'base', 'ligature' )

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
		gclass = glyph.glyphclass
		if inPrivateUseRange( glyph ):
			if gclass == 'automatic':
				rprt( glyph,
					" in private use range, marked 'automatic'." )
				problem = True
			elif( glyph.width == 0
			and not gclass in ('mark', 'component', 'noclass' ) ):
				rprt( glyph,
					" is zero width but isn't a mark or component" )
				problem = True
		else:
			if gclass == 'automatic':
				guni = glyph.unicode
				comb = False
				if guni > 32:
					gu = unichr( guni )
					comb = unicodedata.combining( gu )
				for a in glyph.anchorPoints:
					atype = a[1]
					if comb:
						if atype in baseanch:
							rprt( glyph,
							"is combining but has base anchor"
							+ a[0] )
							problem = True
					else:
						if atype in markanch:
							rprt( glyph,
							"isn't combining but has a mark anchor"
							+ a[0] )
							problem = True

			else:
				if isException( glyph ):
					rprt( glyph,
						"has exceptonal Glyph Class" )
				else:
					rprt( glyph,
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
