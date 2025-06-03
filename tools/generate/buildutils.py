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
import string

import fontforge

import icu


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


def script( g ):
    uni = g if isinstance( g, int ) else g.unicode
    return icu.Script.getScript( chr( uni ) ).getName() if uni != -1 else None

def classify( f ):
    scripts = {}
    for g in f:
        if f[g].unicode >= 0x21 and f[g].unicode <= 0x24F:
            # Enforce most common Common glyphs to the common hint group
            sc = "Latin"
        else:
            sc = script( f[g] )
        name = f[g].glyphname
        if sc:
            if f[g].unicode == -1: print( f"{name} is {sc}" )
        elif name.startswith( 'arab_' ):
            sc = "Arabic"
        elif name.startswith( 'bn_' ):
            sc = "Bengali"
        elif 'cyr_' in name or name.endswith( 'cyr' ) or name.startswith( 'slovo' ):
            sc = "Cyrillic"
        elif name.startswith( ( 'dev_', 'indic_' ) ) or name.endswith( '_dev' ) or name in ( 'sign_purnavirama', 'sign_deerghvirama' ):
            sc = "Devanagari"
        elif name.startswith( 'geo_' ):
            sc = "Georgian"
        elif name.startswith( 'gk_' ):
            sc = "Greek"
        elif name.startswith( 'guj_' ):
            sc = "Gujarathi"
        elif name.startswith( 'gur_' ):
            sc = "Gurmukhi"
        elif name.startswith( 'hanunoo_' ):
            sc = "Hanunoo"
        elif name.startswith( 'kan_' ):
            sc = "Kannada"
        elif name.startswith( 'mal_' ) or name.endswith( '_mal' ) or name in ( 'NameMe.59916', 'NameMe.60158' ):
            sc = "Malayalam"
        elif name.startswith( 'mj_' ):
            sc = "Mahjongg"
        elif name.startswith( 'ori_' ) or name.endswith( '_ori' ):
            sc = "Oriya"
        elif name.startswith( 'sinh_' ) or name.endswith( '_sinh' ):
            sc = "Sinhala"
        elif name.startswith( 'taml_' ) or name.endswith( '_tam' ):
            sc = "Tamil"
        elif name.startswith( 'thaana_' ):
            sc = "Thaana"
        elif 'thai' in name:
            sc = "Thai"
        elif name.startswith( 'braille_' ):
            sc = "Braille"
        elif name.startswith( ( 'mus_', 'pedal_', 'quarter_' ) ) or name.endswith( '_clef_old' ):
            sc = "Musical"
        elif name.startswith( ( 'math_', 'dnom_', 'ipa_tone_', 'mod_tone_', 'clock_', 'clockface' ) ) or name in ( 'zeroslashed', 'vert_bar_short' ) or name.endswith( ( '_bb_it', 'bbit' ) ):
            sc = "Common"
        elif '.cmb' in name or name.startswith( ( 'underline', 'overline', 'enclosing', 'macron' ) ):
            sc = "Inherited"
        elif name.startswith( ( 'lat_', 'ord_', 'old.', 'oldprop.', 'sc.', 'ss.', 'sub.', 'sup.', 'dotlessi' ) ):
            sc = "Latin"
        elif 'latin' in name or name.lower() in ( 'ae', 'aeacute', 'aemacron', 'aeturned', 'aeturnsup', 'engsami', 'tz.lig', 'lig.de_es', 'ij_acute' ):
            sc = "Latin"
        elif name in ( '.notdef', '.null', 'nonmarkingreturn' ):
            sc = "Empty"
        elif name.startswith( 'uni' ) and all( _ in string.hexdigits for _ in name[3:] ):
            sc = script( int( name[3:], 16 ) )
        elif f[g].glyphclass == 'mark':
            sc = "Inherited"
        if not sc:
            for ( ref, *_ ) in f[g].references:
                sc = script( f[ref] )
                if f[ref].unicode > 126 and sc in ('Common', 'Inherited'):
                    sc = None
                if sc:
                    break
            if not sc:
                sc = "---"
        scripts.setdefault( sc, [] ).append( f[g].glyphname )
    return scripts


def rehint( f, autoinstr, sfd_filename ):
    scripts = classify( f )
    for sc in scripts:
        print( f"{sc}: {len(scripts[sc])}" )
        if sc == "---":
            print( repr( scripts[sc] ) )
            assert False
    chunks = []
    chunks.append( scripts.pop( "Latin", [] ) +
                   scripts.pop( "Inherited", [] ) +
                   scripts.pop( "Cyrillic", [] ) +
                   scripts.pop( "Empty", [] ) +
                   scripts.pop( "Unknown", [] ) )
    chunks.append( scripts.pop( "Common", [] ) )
    for sc in scripts:
        chunks.append( scripts[sc] )
    for chunk in chunks:
        f = rehint_glyphs( f, autoinstr, sfd_filename, chunk )
    return f


def rehint_glyphs( f, autoinstr, sfd_filename, glyphs ):
	# BlueFuzz is not recommended by Adobe but used by FontForge's autohinter
	f.private['BlueFuzz'] = 1

	f.selection.select( *glyphs )
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

	f.selection.select( *glyphs )
	f.autoHint()

	# Again, save and re-open the file.
	tmp_name = 'hinted1-' + sfd_filename
	f.save( tmp_name )
	f.close()
	f = fontforge.open( tmp_name )
	os.unlink( tmp_name )

	if autoinstr:
		f.selection.select( *glyphs )
		f.autoInstr()

	return f
