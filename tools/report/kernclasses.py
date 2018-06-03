#!/usr/bin/fontforge -script 
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
__copyright__ = "Copyright 2009, 2010, 2011, 2017, 2018 Stevan White"
__date__ = "$Date$"
__version__ = "$Revision$"


import fontforge
from sys import stdout as out, stderr as err
from OpenType.UnicodeRanges import *

def get_kern_subtables( font ):
	try:
		tables = []
		for lookup in font.gpos_lookups:
			if font.getLookupInfo( lookup )[0] == 'gpos_pair':
				sts = font.getLookupSubtables( lookup )
				for st in sts:
					if font.isKerningClass( st ):
						tables.append( st )
		return tables
	except EnvironmentError as e:
		print( 'EnvironmentError', e, file=err )
	except TypeError as t:
		print( 'TypeError', t, file=err )
	return None
preamble = """<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">
<head>
<meta charset="UTF-8" />
<title>glyph kerning classes in GNU FreeFont
</title>
<style type="text/css">
	.nonexistent { background-color: red; }
	td { text-align: right; font-family: inherit; }
	.I td { font-style: italic; }
	.B td { font-weight: bold; }
	.BI td { font-weight: bold; font-style: italic; }
	td { line-height: 1; }
	.classes td { text-align: left; vertical-align: top; }
	td span { font-weight: normal; font-style: normal; font-size: smaller; color: lime; }
	td span.pos { color: magenta; }
	td.zero { color: gray; }
</style>
</head>
<body>
"""
postamble="""
</body>
</html>
"""

def print_kerns( fontPath ):
	font = fontforge.open( fontPath )
	print( '<h2>Kerning classes in  ' + font.fontname + '</h2>' )
	weight = ''
	if font.os2_weight > 500:
		weight = 'B'
	style = ''
	if font.italicangle < 0.0:
		style = 'I'
	print( '<div  style="font-family: ' + font.familyname + '" ' 
		+ 'class="' + weight + style + '">' )
	subtables = get_kern_subtables( font )
	for st in subtables:
		print( '<h3>Subtable ' + st + '</h3>' )
		printKernsOfSubtable( font, st )
	print( '</div>' )
	out.flush()

def printKernsOfSubtable( font, subtable ):
	kclass = font.getKerningClass( subtable )
	n = 0
	leftclasses = kclass[0]
	rightclasses = kclass[1]
	kerns = kclass[2]
	nr = len( rightclasses )
	print( '<table class="classes"><tr>' )
	print( '<th>left classes: </th>' )
	print( '<th>right classes: </th>' )
	print( '<tr><td>' )
	for lc in leftclasses:
		if lc:
			for c in lc:
				writeentity( font, c )
		print( "<br />" )
	print( "</td>" )
	print( "<td>" )
	for rc in rightclasses:
		if rc:
			for c in rc:
				writeentity( font, c )
		print( "<br />" )
	print( "</td>" )
	print( "</tr>" )
	print( "</table>" )
	print( "<table>" )
	print( "<tr>" )
	print( "<th></th>" )
	for rc in rightclasses:
		if rc:
			out.write( "<th>" + entitystr( font, rc[0] ) + "</th>" )
	print( "</tr>" )
	for lc in leftclasses:
		m = 0
		if lc:
			print( "<tr>" )
			out.write( "<th>" + entitystr( font, lc[0] ) + "</th>" )
			for rc in rightclasses:
				kern = kerns[ n * nr + m ]
				if rc:
					ccolor = ''
					ncolor = ''
					if kern > 0:
						ncolor = ' class="pos"'
					if kern == 0:
						ccolor = ' class="zero"'
					out.write( '<td' + ccolor + '><span' + ncolor + '>' )
					if kern == 0:
						out.write( '&nbsp;' )
					else:
						out.write( str( kern ) )
					out.write( '</span><br />' )
					printpair( font, lc[0], rc[0] )
					out.write( '</td>' )
				m += 1
			print( "</tr>" )
		n += 1
	print( "</table>" )

def writeentity( font, a ):
	out.write( entitystr( font, a ) )

def entitystr( font, a ):
	s = font.findEncodingSlot( a )
	v = formatted_hex_value( s )
	if s == -1:
		v = '<span class="nonexistent">&nbsp;</span>'
		print( font.fullname, 'Missing glyph: ' + a, file=err )
	elif not codepointIsInSomeRange( s ):
		print( font.fullname, 'Non-unicode: ' + v, file=err )
	return v 

def printpair( font, p, q ):
	writeentity( font, p )
	writeentity( font, q )
	out.write( ' ' )

def formatted_hex_value( n ):
	return '%s%0.4x%s' %( "&#x", n, ";" )

def printlist( lst ):
	s = ''
	delim = ''
	for m in lst:
		s += delim + m
		delim = ' '
	print( s )

print( preamble )
print_kerns( '../../sfd/FreeSerif.sfd' )
print_kerns( '../../sfd/FreeSerifItalic.sfd' )
print_kerns( '../../sfd/FreeSerifBold.sfd' )
print_kerns( '../../sfd/FreeSerifBoldItalic.sfd' )
print_kerns( '../../sfd/FreeSans.sfd' )
print_kerns( '../../sfd/FreeSansOblique.sfd' )
print_kerns( '../../sfd/FreeSansBold.sfd' )
print_kerns( '../../sfd/FreeSansBoldOblique.sfd' )
print_kerns( '../../sfd/FreeMono.sfd' )
print_kerns( '../../sfd/FreeMonoOblique.sfd' )
print_kerns( '../../sfd/FreeMonoBold.sfd' )
print_kerns( '../../sfd/FreeMonoBoldOblique.sfd' )
print( postamble )
