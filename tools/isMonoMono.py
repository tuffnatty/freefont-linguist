#!/usr/bin/fontforge -script
"""
Diagnostic tool that checks that fonts are really monospace.

Allows characters to have 0 width though (note this is controversial)

Also: in order for box-drawing characters to connect properly, it is 
important that the glyphs all lie between 800 and -200EM vertically.
"""
__author__ = "Stevan White <stevan.white@googlemail.com>"

import fontforge
import sys

problem = False

def ismonomono( fontfilename ):
	print "Checking character bounding boxes: " + fontfilename
	font = fontforge.open( fontfilename )

	g = font.selection.all()
	g = font.selection.byGlyphs

	nonzero = 0

	for e in g:
		if nonzero == 0:
			if e.width > 0:
				nonzero = e.width
		else:
			if e.width > 0 and e.width != nonzero:
				print '  ' + e.glyphname + ' width is not ' \
						+ str( nonzero )
				problem = True

		( xmin, ymin, xmax, ymax ) = e.boundingBox()
		if ymin < -200 or ymax > 800:
			print '  ' + e.glyphname + ' goes between ' \
				+ str( ymin )  + ' and ' + str( ymax )

scriptname = sys.argv[0];
argc = len( sys.argv )

if argc > 1:
	for i in range( 1, argc ):
		ismonomono( sys.argv[i] )

if problem:
	sys.exit( 1 )
else:
	sys.exit( 0 )
