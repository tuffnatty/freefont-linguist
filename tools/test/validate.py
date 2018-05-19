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
__copyright__ = "Copyright 2009, 2010, Stevan White"
__date__ = "$Date:: 2013-04-09 12:44:41 +0200#$"
__version__ = "$Revision: 1.5 $"

__doc__ = """
Runs the FontForge validate function on all the font faces.
Prints report on standard output.
Returns 1 if problems found 0 otherwise.
"""

import fontforge
from sys import argv, exit
from os import path

problem = False

""" Haven't really figured out why TT limit warniings are turndd on,
	or where the limits are set.
"""
def countPointsInLayer( layer ):
	problem = True
	p = 0
	for c in layer:
		p += len( c )
	return p

def printProblemLine( e, msg ):
	print( "\t" + e.glyphname, msg  )

def dealWithValidationState( state, e ):
	if state & 0x2:
		printProblemLine( e, "has open contour" )
	if state & 0x4:
		printProblemLine( e, "intersects itself" )
	if state & 0x8:
		printProblemLine( e, "is drawn in wrong direction" )
	if state & 0x10:
		printProblemLine( e, "has a flipped reference" )
	if state & 0x20:
		printProblemLine( e, "is missing extrema" )
	if state & 0x40:
		printProblemLine( e, "is missing a reference in a table" )
	if state & 0x80:
		printProblemLine( e, "has more than 1500 pts" )
	if state & 0x100:
		printProblemLine( e, "has more than 96 hints" )
	if state & 0x200:
		printProblemLine( e, "has invalid PS name" )
	"""
	# Not meaningfully set for non-TrueType fonts )
	if state & 0x400:
		printProblemLine( e, "has more points than allowed by TT: " + str( countPointsInLayer( e.layers[1] ) ) )
	if state & 0x800:
		printProblemLine( e, "has more paths than allowed by TT" )
	if state & 0x1000:
		printProblemLine( e, "has more points in composite than allowed by TT" )
	if state & 0x2000:
		printProblemLine( e, "has more paths in composite than allowed by TT" )
	if state & 0x4000:
		printProblemLine( e, "has instruction longer than allowed" )
	if state & 0x8000:
		printProblemLine( e, "has more references than allowed" )
	if state & 0x10000:
		printProblemLine( e, "has references deeper than allowed" )
	if state & 0x20000:
		print e.glyphname + "fpgm or prep tables longer than allowed" )
	"""

def validate( directory, fontFile ):
	fontpath = path.join( directory, fontFile )
	try:
		font = fontforge.open( fontpath )
		print( "Validating", fontFile )

		g = font.selection.all()
		g = font.selection.byGlyphs

		valid = True
		for e in g:
			state = e.validate()
			if state != 0:
				dealWithValidationState( state, e )
		font.validate
	except Exception as e:
		problem = True
		print( "Problem validating", fontpath )
		print( e )

def validateFiles( directory, filelist ):
	for f in filelist:
		filename, extension = path.splitext( f )
		for ext in ( '.sfd', '.otf', '.ttf', '.woff' ):
			validate( directory, filename + ext )
# --------------------------------------------------------------------------
args = argv[1:]

if len( args ) < 1 or len( args[0].strip() ) == 0:
	validateFiles( '../../sfd/',
		( 'FreeSerif.sfd', 'FreeSerifItalic.sfd',
		'FreeSerifBold.sfd', 'FreeSerifBoldItalic.sfd',
		'FreeSans.sfd', 'FreeSansOblique.sfd',
		'FreeSansBold.sfd', 'FreeSansBoldOblique.sfd',
		'FreeMono.sfd', 'FreeMonoOblique.sfd',
		'FreeMonoBold.sfd', 'FreeMonoBoldOblique.sfd' )
		)
else:
	validateFiles( args[0], args[1:] )


if problem:
	exit( 1 )
