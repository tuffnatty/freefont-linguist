#!/usr/bin/env python
# coding: utf-8

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
__copyright__ = "Copyright 2012 Stevan White"
__date__ = "$Date:: 2013-04-09 12:58:21 +0200#$"
__version__ = "$Revision: 2527 $"

__doc__ = """
Check for font feature tables which won't be activated because they lack a
script-language that was listed in another table.

For example
-----------
table A specified to activate when
	latn{'dflt'}
table B specified to activate when
	latn{'dflt', 'ESP '}
Then table A will *not* be activated for Spanish text.

The deal is, "dflt" languages which haven't been listed *anywhere* among *any*
of the tables of the current font.  (For better or worse that's how it is."

This fact may be used to disable an otherwise general table for a specific
language, by simply creating another table that specifies the language, and
not listing the language explicitly in the first table.

Unfortunately, in fonts that deal with multiple features with multiple
languages, this can get very tricky, and often results in features being
*accidentally* disabled.

This script looks for tables which are specified for language 'dflt', then
checks if the inclusion of a language in some other table disables any of them.
"""
from sys import argv, exit, stderr, stdout
import re

def explain_error_and_quit( e='' ):
	if e:
		print >> stderr, 'Error: ', e
	print >> stderr, "Usage:"
	print >> stderr, "       checkTableLangs sfd-file-path"
	exit( 1 )

filename = argv[1] if len( argv ) > 1 else ''
if not filename:
	explain_error_and_quit()

try:
	of = open( filename, 'r' )
except Exception as e:
	explain_error_and_quit( e )

f = open( filename )

"""
Typical line:
Lookup: 6 0 0 "'ccmp' iogonek glyph decompos. in Latin"  {"'ccmp' iogonek glyph decomp in Latin-1"  } ['ccmp' ('latn' <'dflt' > ) ]
"""
	
lookup_re = re.compile( "^Lookup: (\d) (\d) (\d) (.*)$" )
data_re = re.compile( '''^"(.+)"\s+{(.+)}\s+\[(.+)\]''' )
dquot_names_re = re.compile( '"([^"]+)"' )
squot_names_re = re.compile( "'([^']+)'" )
type_scriptlangs_re = re.compile( "'([^']{4})'\s+<([^<]*)>" )

def collect_lookups_from_sfd( f ):
	lookups = {}
	firstline = True
	for line in f:
		if firstline:
			if not line.startswith( "SplineFontDB: " ):
				explain_error_and_quit(
				"doesn't look like FontForge SFD file." )
			firstline = False

		m = lookup_re.match( line )
		if m:
			data = m.group( 4 )
			dm = data_re.match( data )
			if dm:
				parse_lookup( dm, lookups )
	return lookups

def parse_lookup( dm, lookups ):
	tableName = dm.group( 1 )
	subtableNames = dm.group( 2 )
	scriptNames = dm.group( 3 )
	lookups[tableName] = {}
	#if subtableNames:
	#	names = dquot_names_re.findall( subtableNames )
	if scriptNames:
		scn = type_scriptlangs_re.findall( scriptNames )
		for s in scn:
			script = s[0]
			langs = s[1]
			lngs = set( squot_names_re.findall( langs ) )
			if not script in lookups[tableName]:
				lookups[tableName][script] = set()
			lookups[tableName][script] |= lngs

def printall():
	for tn in lookups:
		print tn
		for script in lookups[tn]:
			print '\t', script, ', '.join( lookups[tn][script] )

#printall()

def reverse_script_table( lookups ):
	""" just reverse the table-script relationship """
	scriptTable = {}
	for (name, script_data) in lookups.items():
		for script in script_data:
			if script not in scriptTable:
				scriptTable[script] = set()
			scriptTable[script].add( name )
	return scriptTable

def tables_with_dflt_entry( lookups ):
	""" tables with a 'dflt' entry, associated script of the entry """
	tablesWdflt = {}
	scriptTable = reverse_script_table( lookups )
	for (script,names) in scriptTable.items():
		for name in names:
			allLangs = []
			lngs = lookups[name][script]
			if 'dflt' in lngs:
				tablesWdflt[name] = script
	return tablesWdflt

def disabled_tables( lookups ):
	disabled = {}
	scriptTable = reverse_script_table( lookups )
	tablesWdflt = tables_with_dflt_entry( lookups )
	dfltLang = set( ['dflt'] )
	for name in tablesWdflt:
		script = tablesWdflt[name]
		explicit = lookups[name][script] - dfltLang
		tablesBesidesThisOne = scriptTable[script] - set( [name] )
		for other in tablesBesidesThisOne:
			otherExplicit = lookups[other][script] - dfltLang
			conflict = otherExplicit - explicit
			if conflict:
				if not name in disabled:
					disabled[name] = []
				disabled[name].append( ( other, conflict ) )
	return disabled

lookups = collect_lookups_from_sfd( f )
disabled = disabled_tables( lookups )

for feat in disabled:
	print "feature", '"' + feat + '"', "shadowed"
	for ( other, langs ) in disabled[feat]:
		print "\t", list( langs ), 'by "' + other + '"'

