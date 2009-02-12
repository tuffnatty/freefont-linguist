#!/usr/bin/fontforge -script 

"""
Check for glyphs with back layers.

Haven't see this actually work...

"""
__author__ = "Stevan White <stevan.white@googlemail.com>"

import fontforge
import sys

problem = False

def ismonomono( fontPath ):
	print "Checking " + fontPath
	font = fontforge.open( fontPath )

	g = font.selection.all()
	g = font.selection.byGlyphs

	nonzero = 0

	for e in g:
		if e.layer_cnt != 2:
			print e

ismonomono( '../sfd/FreeSerif.sfd' )
ismonomono( '../sfd/FreeSerifItalic.sfd' )
ismonomono( '../sfd/FreeSerifBold.sfd' )
ismonomono( '../sfd/FreeSerifBoldItalic.sfd' )
ismonomono( '../sfd/FreeSans.sfd' )
ismonomono( '../sfd/FreeSansOblique.sfd' )
ismonomono( '../sfd/FreeSansBold.sfd' )
ismonomono( '../sfd/FreeSansBoldOblique.sfd' )
ismonomono( '../sfd/FreeMono.sfd' )
ismonomono( '../sfd/FreeMonoOblique.sfd' )
ismonomono( '../sfd/FreeMonoBold.sfd' )
ismonomono( '../sfd/FreeMonoBoldOblique.sfd' )

if problem:
	sys.exit( 0 )
else:
	sys.exit( 1 )
