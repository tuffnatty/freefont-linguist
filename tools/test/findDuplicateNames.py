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
__copyright__ = "Copyright 2013, 2017, 2018 Stevan White"
__date__ = "$Date: $"
__version__ = "$Revision: 2589 $"

__doc__ = """
Purpose is to list out any glyphs in the fonts whose names are duplicated.
I don't know how that issue arises, but somehow it does.
Works by direct parsing of the SFD files.
This is a hack.
"""

import fontforge
from sys import argv
from os import path

def findDuplicateNames( fontDir, fontFile ):
	if isinstance( fontFile, ( list, tuple ) ):
		print( "In directory", fontDir )
		for f in fontFile:
			findDuplicateNames( fontDir, f )
		return

	print( "Checking for duplicate glyph names in", fontFile )

	font = fontforge.open( path.join( fontDir, fontFile ) )

	g = font.selection.all()
	g = font.selection.byGlyphs

	names = {}
	for glyph in g:
		if glyph.glyphname in names:
			names[glyph.glyphname].append( glyph.encoding )
		else:
			names[glyph.glyphname] = [ glyph.encoding ]
	print( len( names ) )
	for n in names:
		if len( names[n] ) > 1:
			print( "duplicate", n )
			print( "\t" + names[n] )


# --------------------------------------------------------------------------
args = argv[1:]

if len( args ) < 1 or len( args[0].strip() ) == 0:
	findDuplicateNames( '../../sfd/',
		( 'FreeSerif.sfd', 'FreeSerifItalic.sfd',
		'FreeSerifBold.sfd', 'FreeSerifBoldItalic.sfd',
		'FreeSans.sfd', 'FreeSansOblique.sfd',
		'FreeSansBold.sfd', 'FreeSansBoldOblique.sfd',
		'FreeMono.sfd', 'FreeMonoOblique.sfd',
		'FreeMonoBold.sfd', 'FreeMonoBoldOblique.sfd' ) )
else:
	findDuplicateNames( args[0], args[1:] )

