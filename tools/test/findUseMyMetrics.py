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
__copyright__ = "Copyright 2016, 2018 Stevan White"
__date__ = "$Date: $"
__version__ = "$Revision: 3050 $"

__doc__ = """
Many applications, especially on Windows, have bugs regarding the TrueType
flag USE_MY_METRICS.

If a glyph reference is rotated, and the flag is set for it, these
applications behave as if the advance width of the containing glyph 
were negative.

This seems to be endemic on Windows -- it seems to be a deep problem,
likely in Cleartype itself.  And the behaviour is inconsistent...

Official statement from MS in OpenType spec:
Note that the behavior of the USE_MY_METRICS operation is undefined for
rotated composite components.

"""

#FIXME Tragically, the FontForge Python function useRefsMetrics always
# returns true, regardless the value of the USE_MY_METRICS flag 
# for that reference.
# Therefore this script parses the SFD file directly.

from sys import argv, exit
import re
from os import path

problem = False

class glyphref:
	def __init__( self, codept ):
		self.codept = codept
		self.tmatrix = ()
		self.offset = ()
		self.use_my_metrics = False

class glyph:
	def __init__( self, name ):
		self.name = name.strip()
		self.codept = -1
		self.refs = []
	def setCodept( self, codept ):
		self.codept = codept

	def ref_with_use_my_metrics( self ):
		for r in self.refs:
			if r.use_my_metrics:
				return r
		return None
	def __str__( self ):
		return self.name + " [" + str( hex( self.codept ) ) + "]"

encoding_re = re.compile( "Encoding: (\d+) (\d+) (\d+)" )
_flt_re = "-?\d+(?:/.\d*)?"
_rre = ( "Refer: (\d+) (\d+) ([NS])"
	+ " (" + _flt_re + " " + _flt_re + " " + _flt_re + " " + _flt_re + ")"
	+ " (" + _flt_re + " " + _flt_re + ")"
	+ " (\d+)"
)
refer_re = re.compile( _rre )
_flt_grp = "(" + _flt_re + ")"
_tmx = _flt_grp + " " + _flt_grp + " " + _flt_grp + " " + _flt_grp 
tmatrix_re = re.compile( _tmx )
_off = _flt_grp + " " + _flt_grp
offset_re = re.compile( _tmx )

def checkUseMyMetrics( fontDir, fontFile ):
	if isinstance( fontFile, ( list, tuple ) ):
		print( "In directory " + fontDir )
		for fontName in fontFile:
			if fontName.endswith( '.sfd' ):
				checkUseMyMetrics( fontDir, fontName )
			else:
				print( "Argument must be a FontForge SFD file." )
				exit( 1 )
		return

	print( "Checking for rotated references with use_my_metrics in "
		+ fontFile )
	sfd_file = open( path.join( fontDir, fontFile ) )

	glyphs = collectGlyphsAndRefs( sfd_file )

	for glyphname in glyphs:
		g = glyphs[glyphname]
		r = g.ref_with_use_my_metrics()
		if r:
			if r.tmatrix[0] != 1.0 or r.tmatrix[1] != 0.0:
				print( g )
				problem = True

def collectGlyphsAndRefs( sfd_file ):
	glyphs = {}
	curglyph = None
	for line in sfd_file:
		if line.startswith( "StartChar: " ):
			hlen = len( "StartChar: " )
			glyphname = line[hlen:]
			curglyph = glyph( glyphname )
		elif line.startswith( "Encoding" ):
			m = encoding_re.match( line )
			if m and curglyph:
				curglyph.codept = int( m.group( 1 ) )
		elif line.startswith( "Refer" ):
			m = refer_re.match( line )
			if m:
				index = int( m.group( 1 ) )
				codept = int( m.group( 2 ) )
				ref = glyphref( codept )
				selected = m.group( 3 ) == "S"
				tm = tmatrix_re.match( m.group( 4 ) )
				if tm:
					ref.tmatrix = ( float( tm.group( 1 ) ),
						float( tm.group( 2 ) ),
						float( tm.group( 3 ) ),
						float( tm.group( 4 ) ) )
				om = offset_re.match( m.group( 5 ) )
				if om:
					ref.offset = ( float( om.group( 1 ) ),
						float( om.group( 2 ) ) )
				flags = int( m.group( 6 ) )
				ref.use_my_metrics = flags & 1

				if curglyph:
					curglyph.refs.append( ref )
		elif line.startswith( "EndChar" ):
			if curglyph:
				glyphs[curglyph.name] = curglyph
			curglyph = None
	return glyphs


# --------------------------------------------------------------------------
args = argv[1:]

if len( args ) < 1 or len( args[0].strip() ) == 0:
	checkUseMyMetrics( '../../sfd/',
		( 'FreeSerif.sfd', 'FreeSerifItalic.sfd',
		'FreeSerifBold.sfd', 'FreeSerifBoldItalic.sfd',
		'FreeSans.sfd', 'FreeSansOblique.sfd',
		'FreeSansBold.sfd', 'FreeSansBoldOblique.sfd',
		'FreeMono.sfd', 'FreeMonoOblique.sfd',
		'FreeMonoBold.sfd', 'FreeMonoBoldOblique.sfd' ) )
else:
	checkUseMyMetrics( args[0], args[1:] )

if problem:
	exit( 1 )
