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
__copyright__ = "Copyright 2011, 2012, 2018 Stevan White"
__date__ = "$Date::                           $"
__version__ = "$Revision$"
__doc__ = """
Common tools used by the generate scripts.
"""

import os
import re

import fontforge


_re_vstr = re.compile( r'\$Revision: (\d*)\s*\$(.*)' )

def trim_version_str( font ):
	""" SVN automatically puts a revision number between dollar signs
	in the sfd file's Version string.
	However the OpenType standard recommends
		Version n.m
	Where n and m are decimal numbers.
	"""
	vstr_match = _re_vstr.match( font.version )
	otstdized = ''
	if vstr_match:
		trimmed = vstr_match.group( 1 )
		rest = vstr_match.group( 2 )
		otstdized = '0412.' + trimmed + rest
		font.version = otstdized
		#font.appendSFNTName( n[0], n[1], otstdized )
		return trimmed
	return otstdized


def init_hinting():
	fontforge.setPrefs( 'HintBoundingBoxes', 1 )
	fontforge.setPrefs( 'DetectDiagonalStems', 1 )
	fontforge.setPrefs( 'HintDiagonalEnds', 1 )
	fontforge.setPrefs( 'HintDiagonalInter', 1 )


def rehint( f, sfd_filename ):
	# BlueFuzz is not recommended by Adobe but used by FontForge's autohinter
	f.private['BlueFuzz'] = 1

	f.selection.all()
	f.autoHint()

	# Now guess the magic values and autohint again
	f.private.guess( 'StemSnapH' )
	f.private.guess( 'StemSnapV' )
	f.private.guess( 'StdHW' )
	f.private.guess( 'StdVW' )

	# Some fonts don't have OtherBlues specified
	if 'OtherBlues' not in f.private:
		f.private.guess( 'OtherBlues' )

	# At this moment, makes sense to save and re-open the file. The results are
	# better in this case, probably due to some memory corruption in FontForge.
	tmp_name = 'hinted0-' + sfd_filename
	f.save( tmp_name )
	f.close()
	f = fontforge.open( tmp_name )
	os.unlink( tmp_name )

	f.selection.all()
	f.autoHint()

	# Again, save and re-open the file.
	tmp_name = 'hinted1-' + sfd_filename
	f.save( tmp_name )
	f.close()
	f = fontforge.open( tmp_name )
	os.unlink( tmp_name )

	return f
