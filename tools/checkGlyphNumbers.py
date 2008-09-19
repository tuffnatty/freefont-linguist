#!/usr/local/bin/fontforge -script 
"""
For most unicode ranges, glyph slot numbers should be the same as the
Unicode value.
The Private Use ranges are the exception: those characters should have a
definate non-Unicode number: -1

This script checks that this is the case, and prints out a warning
whenever it isn't.
"""
__author__ = "Stevan White <stevan.white@googlemail.com>"

import fontforge
import sys

problem = False

def checkGlyphNumbers( dir, fontFile ):
	print "Checking slot numbers in " + fontFile
	font = fontforge.open( dir + fontFile )

	g = font.selection.all()
	g = font.selection.byGlyphs

	valid = True
	for glyph in g:
		if  glyph.encoding < 0xE800 or glyph.encoding > 0xF8FF:
			if glyph.encoding != glyph.unicode:
				print "Glyph at slot " + str( glyph.encoding ) \
					+ " has wrong Unicode"
				problem = True
		else:
			if glyph.unicode != -1:
				print "Glyph at slot " + str( glyph.encoding ) \
					+ " is Private Use but has Unicode"
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
