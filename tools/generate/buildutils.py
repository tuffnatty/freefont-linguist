__license__ = """
This file is part of Gnu FreeFont.

Gnu FreeFont is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Gnu FreeFont is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Gnu FreeFont.  If not, see <http://www.gnu.org/licenses/>. 
"""
__author__ = "Stevan White"
__email__ = "stevan.white@googlemail.com"
__copyright__ = "Copyright 2011, Stevan White"
__date__ = "$Date: 2011-09-12 14:25:06 +0200 (Mon, 12 Sep 2011) $"
__version__ = "$Revision: 1694 $"
__doc__ = """
Common tools used by the generate scripts.
"""

import re

_re_vstr = re.compile( 'Version \$(.*)\$' )

def trim_version_str( font ):
	for n in font.sfnt_names:
		if n[1] == 'Version':
			vstr_match = _re_vstr.match( n[2] )
			if vstr_match:
				trimmed = vstr_match.group( 1 )
				font.appendSFNTName( n[0], n[1], trimmed )
				return trimmed
			return n[2]
	return ''

