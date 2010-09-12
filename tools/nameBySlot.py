"""
For use from the FontForge Script Menu.
Add it to the Scripts Menu using the Preferences dialog.

Sets the name and unicode values of the selected range of slots to 
the encoding, that is
	Name:	uniXXXX
	Unocode:	u+XXXX
where XXXX is the 4-digit hex value for the slot encoding.

Careful! it changes the falue whether it was previously set or not.

Detailed info is printed to standard output (see by launching FontForge
from a console).
"""
__author__ = "Stevan White <stevan.white@googlemail.com>"
__date__ = "$Date: 2010-09-12 18:42:44 $"
__version__ = "$Revision: 1.2 $"

import fontforge

def explain_error_and_quit( e ):
	if e:
		print 'Error: ', e
	exit( 1 )

try:
	glyphs = fontforge.activeFont().selection.byGlyphs
	for g in glyphs:
		if g.encoding <= 0xFFFF:
			newname = 'uni%0.4x' %( g.encoding )
		elif g.encoding <= 0xFFFFF:
			newname = 'uni%0.5x' %( g.encoding )
		elif g.encoding <= 0xFFFFFF:
			newname = 'uni%0.6x' %( g.encoding )
		elif g.encoding <= 0xFFFFFFF:
			newname = 'uni%0.7x' %( g.encoding )
		elif g.encoding <= 0xFFFFFFFF:
			newname = 'uni%0.8x' %( g.encoding )
		print "naming " + str( g.glyphname ) + ' as ' + newname
		g.glyphname =  newname
		g.unicode = g.encoding
except ValueError, e:
	explain_error_and_quit( e )

