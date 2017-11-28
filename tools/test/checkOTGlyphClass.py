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
__copyright__ = "Copyright 2016, 2017 Stevan White"
__date__ = "$Date:: 2015-05-17 14:48:22 +0200#$"
__version__ = "$Revision: 3050 $"

__doc__ = """
For glyphs in Unicode ranges, the OpenType Glyph Class should usually be 
left automatic, to be determined from the standards.

For glyphs in non-Unicode blocks, it may be important to set the Glyph Class.
(Mark Positoning depends on this, for example.)

This script checks that Unicode glyphs all have Glyph Class "automatic",
and that a zero-width glyph in any other block is *not* "automatic".
Then it checks that mark anchors belong to glyphs meant to be combining
and that base anchors belown to base glyphs.
"""

import fontforge
import sys
import unicode_data

problem = False

def isException( glyph ):
	e = glyph.encoding
	# Malayalam vowels are Mark to allow positioning of subsequent marks.
	return ( e in range( 0x0D3E, 0X0D40 + 1 )
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
zeroWidthOK = ('mark', 'component', 'noclass' )

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
		comb = False
		if inPrivateUseRange( glyph ):
			comb = ( gclass == "mark" )
			if gclass == 'automatic':
				rprt( glyph,
					" in private use range, marked 'automatic'." )
				problem = True
			if glyph.width == 0 and not gclass in zeroWidthOK:
				rprt( glyph,
					" is zero width but isn't a mark or component" )
				problem = True
		else:
			guni = glyph.unicode
			if guni > 32:	# bug in unichr() ?
				gu = unichr( guni )
				try:
					#unicode_data.name( gu )
					comb = unicode_data.is_combining_character( gu )
				except Exception as e:
					#FIXME unicodedata woefully out of date
					#print( "NOT FOUND in unicodedata", glyph.glyphname )
					gclass = glyph.glyphclass
					comb = ( gclass == "mark" )
					print( "WOHAH", e )
					raise( e)
					
			if gclass != 'automatic':
				if isException( glyph ):
					#rprt( glyph,
					#	"has exceptonal Glyph Class" )
					pass
				else:
					rprt( glyph,
						"has non-automatic Glyph Class" )
				problem = True
		for a in glyph.anchorPoints:
			aname = a[0]
			atype = a[1]
			if comb:
				if atype in baseanch:
					rprt( glyph,
					"is combining but has base anchor "
					+ aname )
					problem = True
			else:
				if atype in markanch:
					rprt( glyph,
					"isn't combining but has mark anchor "
					+ aname )
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

#print( unicode_data.unidata_version )
if problem:
	sys.exit( 1 )
