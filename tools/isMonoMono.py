#!/usr/local/bin/fontforge -script
"""
Diagnostic tool that checks that fonts are really monospace.

Allows characters to have 0 width though (note this is controversial)

"""
__author__ = "Stevan White <stevan.white@googlemail.com>"

import fontforge
import sys

problem = False

def ismonomono( fontPath ):
	print "Checking " + fontPath + " is monospaced"
	font = fontforge.open( fontPath )

	g = font.selection.all()
	g = font.selection.byGlyphs

	nonzero = 0

	for e in g:
		if nonzero == 0:
			if e.width > 0:
				nonzero = e.width
		else:
			if e.width > 0 and e.width != nonzero:
				print str( e ) + ' width not equal to ' \
						+ str( nonzero )
				problem = True

ismonomono( '../sfd/FreeMono.sfd' )
ismonomono( '../sfd/FreeMonoOblique.sfd' )
ismonomono( '../sfd/FreeMonoBold.sfd' )
ismonomono( '../sfd/FreeMonoBoldOblique.sfd' )

if problem:
	sys.exit( 1 )
else:
	sys.exit( 0 )
