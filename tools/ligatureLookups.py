#!/usr/bin/fontforge -script 
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
__copyright__ = "Copyright 2009, 2010, Stevan White"
__date__ = "$Date: 2010-09-14 13:02:02 $"
__version__ = "$Revision: 1.4 $"

__doc__ = """
ligatureLookups

	fontforge -script ligatureLookups font_file_path...

Output is HTML showing all the ligature lookups in the font.

To display the ligature, the HTML entities for the component Unicode charaters
are printed together.  Then to show the components sparately they, are printed
with intervening spaces.

Most web browsers do not display any character unless it is Unicode. 
It may replace a sequence of Unicode characters by a ligature, however.

Some of the ligatures in Indic ranges expand to (are made of) non-Unicode
characters, which themselves are ligatures.  Ultimately, they all should
resolve to Unicode characters, although there isn't any real limit to how many 
steps it may take.

The resulting string of Unicode characters can then be put into HTML, which
should be properly rendered by a browser.

"""

import fontforge
import sys

def get_ligature_lookups( font ):
	try:
		tables = []
		for lookup in font.gsub_lookups:
			if font.getLookupInfo( lookup )[0] == 'gsub_ligature':
				sts = font.getLookupSubtables( lookup )
				for st in sts:
					tables.append( st )
		return tables
	except EnvironmentError, ( e ):
		print >> sys.stderr, 'EnvironmentError ' + str( e )
	except TypeError, ( t ):
		print >> sys.stderr, 'TypeError ' + str( t )
	return None

def makePreamble():
	return """<?xml version="1.0" encoding="utf-8"?>
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
	<title>Ligatures</title>
	<style type="text/css">
		.nonchar { background-color: red; }
		table, tr, td { font-family: inherit; }
		table, tr, td { font-style: inherit; }
		table, tr, td { font-weight: inherit; }
		td { text-align: right; }
		td { line-height: 1; }
		.ligatures td { width: 2em; }
		.ligatures th { text-align: left; font-family: freemono, monospace; }
	</style>
	</head>
	<body>
	"""
postamble="""
</body>
</html>
"""

def print_ligatures( fontPath ):
	subtables = []
	font = fontforge.open( fontPath )

	style = ''
	if font.italicangle != 0.0:
		style = "font-style: italic; "
	weight = ''
	if font.weight == 'Bold':
		weight = "font-weight: bold; "

	print  '<div style="font-family: \'' + font.familyname + '\'; ' \
			+ style + weight + '\">'
	print  '<h2>Ligatures in  ' + font.fontname + '</h2>'

	subtable_names = get_ligature_lookups( font )
	for subtable_name in subtable_names:
		subtables.append( makeLigatureSubtable( font, subtable_name ) )
	for subtable in subtables:
		printLigaturesOfSubtable( font, subtable, subtables )
	print  '</div>'
	sys.stdout.flush()

class Ligature:
	def __init__( self, glyph ):
		self.glyph = glyph
		self.parts = []
	def setParts( self, parts ):
		self.parts = parts
	def append( self, part ):
		self.parts.append( part )

class LigatureSubtable:
	def __init__( self, tablename, name ):
		self.tablename = tablename
		self.name = name
		self.ligatures = []
	def append( self, ligature ):
		self.ligatures.append( ligature )
	def findLigatureGlyph( self, g ):
		for p in self.ligatures:
			if g == p.glyph.encoding:
				return p
		return False

def findLigatureGlyph( g, subtables ):
	for s in subtables:
		lig = s.findLigatureGlyph( g )
		if lig:
			return lig
	return False

"""
From FontForge Python scripting doc

glyph.getPosSub( lookup-subtable-name )

Returns any positioning/substitution data attached to the glyph controlled by the lookup-subtable. If the name is "*" then returns data from all subtables.

The data are returned as a tuple of tuples. 
  The first element of the subtuples is the name of the lookup-subtable.
  The second element will be one of the strings:
  "Position", "Pair", "Substitution", "AltSubs", "MultSubs","Ligature".
...
   Ligature data will be followed by several strings each containing the name of a ligature component glyph.


BUT...
this info is attached to glyphs...
which glyph is it attached to?  ones in the range, or the ligatures?
how to get the glyphs in the range referred to by the lookup??

Evidently, the library has stuff arranged internally to do the search
efficiently in the backwards direction, from glyph to subtable.

font.getLookupInfo gets a feature-script-lang-tuple, which in principle
should be able to resolve a glyph list... but can't see how to use it...

"""
def makeLigatureSubtable( font, subtable_name ):
	subtable = LigatureSubtable( "", subtable_name )
	for g in font.glyphs():
		ligs = g.getPosSub( subtable_name )
		if ligs:
			ligature = Ligature( g )
			for lr in ligs:
				if len( lr ) < 3 or lr[1] != 'Ligature':
					print >> sys.stderr, 'non-ligature: ' + g.glyphname
					break
				i = 2
				while i < len( lr ):
					ligature.append( lr[i] )
					i += 1

			subtable.append( ligature )
	return subtable

def printLigaturesOfSubtable( font, subtable, subtables ):
	print '<table class="ligatures" rules="groups">'
	print '<caption>' + subtable.name + '</caption>'
	print '<colgroup>'
	print '<col style="width: 50ex" />'
	print '</colgroup>'
	print '<colgroup>'
	print '<col style="width: 4ex" />'
	print '</colgroup>'
	for lig in subtable.ligatures:
		print '<tr>'
		sys.stdout.write( '<th>' )

		if lig.glyph.unicode > -1:
			s = font.findEncodingSlot( lig.glyph.unicode )
			sys.stdout.write( '%s%0.4x%s' %( "U+", s, " " ) )
		else:
			sys.stdout.write( '%s%0.4x%s' %( "#", lig.glyph.encoding, " " ) )
		sys.stdout.write( lig.glyph.glyphname )
		sys.stdout.write( '</th>' )

		sys.stdout.write( '<td>' )
		for p in lig.parts:
			printnestedentity( font, subtable, p, subtables )
		sys.stdout.write( '</td>' )

		for p in lig.parts:
			sys.stdout.write( '<td>' )
			printnestedentity( font, subtable, p, subtables )
			sys.stdout.write( '</td>' )
		print '</tr>'
	print "</table>"

"""
Expands each ligature, then checks each component to see if it's Unicode. 
If not, it looks through all the ligature tables to expand it,
and so on recursively until only Unicode characters remain.
"""
def printnestedentity( font, subtable, a, subtables ):
	s = font.findEncodingSlot( a )
	if s >= 0xe000 and s <= 0xf8ff:
		lig = findLigatureGlyph( s, subtables )
		if lig:
			#print >> sys.stderr, 'Nested glyph found: ' + a
			for p in lig.parts:
				printnestedentity( font, subtable, p, subtables )
		else:
			print >> sys.stderr, 'No nested glyph: ' + a
			sys.stdout.write( '<span class="nonchar">&nbsp;</span>' )
	else:
		printentity( font, a )

def printentity( font, a ):
	s = font.findEncodingSlot( a )
	if s == -1:
		print >> sys.stderr, 'Missing glyph: ' + a
		sys.stdout.write( '<span class="nonchar">&nbsp;</span>' )
	else:
		sys.stdout.write( formatted_hex_value( s ) )

def formatted_hex_value( n ):
	return '%s%0.4x%s' %( "&#x", n, ";" )

args = sys.argv[1:]

if len( args ) < 1 or len( args[0].strip() ) == 0:
	sys.exit( 0 )

print makePreamble()
for font_name in args:
	print_ligatures( font_name )
print postamble
