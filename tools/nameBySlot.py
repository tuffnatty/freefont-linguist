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
__date__ = "$Date: 2008-05-20 06:37:04 $"
__version__ = "$Revision: 1.1 $"

import fontforge

def explain_error_and_quit( e ):
	if e:
		print 'Error: ', e
	exit( 1 )

try:
	glyphs = fontforge.activeFont().selection.byGlyphs
	for g in glyphs:
		newname = 'uni%0.4x' %( g.encoding )
		print "naming " + str( g.glyphname ) + ' as ' + newname
		g.glyphname =  newname
		g.unicode = g.encoding
except ValueError, e:
	explain_error_and_quit( e )

