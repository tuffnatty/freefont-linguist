#!/usr/bin/env python
from __future__ import print_function
import re
from sys import stdout, stderr
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
__copyright__ = "Copyright 2012, 2017 Stevan White"
__date__ = "$Date: 2011-09-12 14:25:06 +0200 (Mon, 12 Sep 2011) $"
__version__ = "$Revision: 1694 $"

sfdfile = open( "in-font.sfd" )	# the input font SFD file

__doc__ = """
To move all references to a couple of glyphs a bit horizontally.
Pretty primitive.
Operates directly on a FontForge SFD file (because I couldn't find a FontForge
interface that allowed moving references... why?)
So have to find  "encoding" info for glyph.

StartChar: grave
Encoding: 96 96 64

StartChar: acute
Encoding: 180 180 113

The references to the glyph look like this:

Refer: 113 180 S 1 0 0 1 239 212 0

Refer: 113 180 N 1 0 0 1 99 2 0

Refer: 64 96 N 1 0 0 1 82 212 0

Don't know what the N and S stand for.
In all cases, the next numbers were 1 0 0 1.  Probably identity matrix.
My guess is, the next are horizontal and vertical offsets.
The next is sometimes 0 sometimes 2.
"""
refStart = 'Refer: 64 96 '	# recognize references to certain character
refTrans = ' 1 0 0 1 '
re_ref = re.compile( refStart + '(N|S)' + refTrans + '([-0-9]*) ([-0-9]*) (\d*)' )
re_charname = re.compile( 'StartChar: (.*)' )

charname = ''

for line in sfdfile:
	charname_match = re_charname.match( line )
	if charname_match:
		charname = charname_match.group( 0 )
	refer_match = re_ref.match( line )
	if refer_match:
		g = refer_match.groups()
		print( charname, g, file=stderr )
		dx = 79	# amount to slide horizontally
		gnew = ( g[0], int( g[1] ) + dx, g[2], g[3] )	
		newline = ( refStart + '%s' + refTrans + '%s %s %s\n' ) % gnew
		stdout.write( newline )
	else:
		stdout.write( line )

