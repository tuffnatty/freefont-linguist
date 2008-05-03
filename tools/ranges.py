"""
Makes an HTML table showing how many glyphs are in each range in each font,
and tries to collate that with the OS/2 character range support bit flags.

Runs under FontForge.
	fontforge -script ranges.py

$Id: ranges.py,v 1.6 2008-05-03 15:00:32 Stevan_White Exp $
"""
__author__ = "Stevan White <stevan.white@googlemail.com>"

import fontforge
import sys
import time


""" OS/2 bit encoding of Unicode character ranges
Note this is bound to Unicode 1.1.
http://www.w3.org/TR/REC-CSS2/notes.html
http://shlimazl.nm.ru/eng/fonts_ttf.htm

The intervals are partly just the assigned interval, but often I have
listed the ranges that have characters assigned to them.

This is a hack--in no way authoritative.  Lots of guesswork; much is wrong.

See below a list of TrueType OS/2 character ranges I was working from.
"""
class interval:
	def __init__( self, begin, end ):
		self.begin = begin
		self.end = end
	def len( self ):
		return 1 + self.end - self.begin

ulUnicodeRange = [
[0,	'Basic Latin', [interval(0x0020, 0x007E)] ],
[1,	'Latin-1 Supplement',[interval(0x00A0, 0x00FF)] ],
[2,	'Latin Extended-A',	[interval(0x0100, 0x017F)] ],
[3,	'Latin Extended-B',     [interval(0x0180, 0x024F)]],
#extended C and D?
[4,	'IPA Extensions',     [interval(0x0250, 0x02AF)]],
[5,	'Spacing Modifier Letters',     [interval(0x02B0, 0x02FF)]],
[6,	'Combining Diacritical Marks',     [interval(0x0300, 0x036F)]],
[7,	'Basic Greek',     [interval(0x0370, 0x0377),
			interval(0x037A, 0x037E),
			interval(0x0384, 0x038A),
			interval(0x038C, 0x038C),
			interval(0x038E, 0x03A1),
			interval(0x03A3, 0x03CF)] ],
[8,	'Greek Symbols And Coptic',     [interval(0x03D0, 0x03EF)]],	# this is quite unclear.  Range isn't in Unicode 2.0.  
[9,	'Cyrillic',     [
	interval(0x0400, 0x04FF),	# Cyrillic
#	interval(0x0500, 0x0523)	# Cyrillic Supplement
	]	# Cyrillic extended A and B?
	],
[10,	'Armenian',     [interval(0x0531, 0x0556),
			interval(0x0559, 0x055F),
			interval(0x0561, 0x0587),
			interval(0x0589, 0x058A)
			]
	],
[11,	'Basic Hebrew',     [interval(0x0591, 0x05C7),
			interval(0x05D0, 0x05EA),
			interval(0x05F0, 0x05F4)
	]
	],
[12,	'Hebrew Extended (A and B blocks combined)',     [interval(0xFB00, 0xFB4F)]],	#FIXME this isn't right: also this range isn't in Unicode 2.0
[13,	'Basic Arabic',     [interval(0x0600, 0x0603),
				interval(0x0606, 0x061B),
				interval(0x061E, 0x061F),
				interval(0x0621, 0x065E),
				interval(0x0660, 0x066F)
	]
	],
[14,	'Arabic Extended', [interval(0x0670, 0x06FF)]],	#FIXME unclear. range not in Unicode 2.0
	# Syriac?
	#Thaana?
[15,	'Devanagari',     [interval(0x0901, 0x0939),
			interval(0x093C, 0x094D),
			interval(0x0950, 0x0954),
			interval(0x0958, 0x0972),
			interval(0x097B, 0x097F)
			]],
[16,	'Bengali',     [interval(0x0980, 0x09FF)]],
[17,	'Gurmukhi',     [interval(0x0A00, 0x0A7F)]],
[18,	'Gujarati',     [interval(0x0A80, 0x0AFF)]],
[19,	'Oriya',     [interval(0x0B00, 0x0B7F)]],
[20,	'Tamil',     [interval(0x0B80, 0x0BFF)]],
[21,	'Telugu',     [interval(0x0C00, 0x0C7F)]],
[22,	'Kannada',     [interval(0x0C80, 0x0CFF)]],
[23,	'Malayalam',     [interval(0x0D00, 0x0DFF)]],
[24,	'Thai',     [interval(0x0E01, 0x0E3A),
			interval(0x0E3F, 0x0E5B)
			]
		],
[25,	'Lao',     [interval(0x0E80, 0x0EFF)]],
	#Tibetan? Myanmar?
[26,	'Basic Georgian',     [interval(0x10A0, 0x10C5),
			interval(0x10D0, 0x10FC)]],
[27,	'Georgian Extended', [interval(0x2D00, 0x2D25)]],	#??
[28,	'Hangul Jamo',     [interval(0x1100, 0x11FF)]],
[29,	'Latin Extended Additional',     [interval(0x1E00, 0x1EFF)]],
[30,	'Greek Extended',     [interval(0x1F00, 0x1F15),
		interval(0x1F18, 0x1F1D),
		interval(0x1F20, 0x1F45),
		interval(0x1F48, 0x1F4D),
		interval(0x1F50, 0x1F57),
		interval(0x1F59, 0x1F59),
		interval(0x1F5B, 0x1F5B),
		interval(0x1F5D, 0x1F5D),
		interval(0x1F5F, 0x1F7D),
		interval(0x1F80, 0x1FB4),
		interval(0x1FB6, 0x1FC4),
		interval(0x1FC6, 0x1FD3),
		interval(0x1FD6, 0x1FDB),
		interval(0x1FDD, 0x1FEF),
		interval(0x1FF2, 0x1FF4),
		interval(0x1FF6, 0x1FFE)
	]],
[31,	'General Punctuation',     [interval(0x2000, 0x2060)]],
[32,	'Superscripts And Subscripts',     [interval(0x2070, 0x2071),
		interval(0x2074, 0x208E),
		interval(0x2080, 0x2084)
	]
	],
[33,	'Currency Symbols',     [interval(0x20A0, 0x20B5)]],
[34,	'Combining Diacritical Marks For Symbols',     [interval(0x20D0, 0x20FF)]],
[35,	'Letterlike Symbols',     [interval(0x2100, 0x214F)]],
[36,	'Number Forms',     [interval(0x2153, 0x2188)]],
[37,	'Arrows',     [interval(0x2190, 0x21FF)]],
[38,	'Mathematical Operators',     [interval(0x2200, 0x22FF)]],
[39,	'Miscellaneous Technical',     [interval(0x2300, 0x23FF)]],
[40,	'Control Pictures',     [interval(0x2400, 0x243F)]],
[41,	'Optical Character Recognition',     [interval(0x2440, 0x245F)]],
[42,	'Enclosed Alphanumerics',     [interval(0x2460, 0x24FF)]],
[43,	'Box Drawing',     [interval(0x2500, 0x257F)]],
[44,	'Block Elements',     [interval(0x2580, 0x259F)]],
[45,	'Geometric Shapes',     [interval(0x25A0, 0x25FF)]],
[46,	'Miscellaneous Symbols',     [interval(0x2600, 0x269D),
			interval(0x26A0, 0x26C3)]],
[47,	'Dingbats',     [interval(0x2701, 0x27BF)]],	#FIXME several intervals
[48,	'CJK Symbols And Punctuation', [interval(0x3000, 0x303F)]],
[49,	'Hiragana', [interval(0x3040, 0x309F)]],
[50,	'Katakana', [interval(0x30A0, 0x30FF)]],
[51,	'Bopomofo', [interval(0x3100, 0x312F)]],
[52,	'Hangul Compatibility Jamo', [interval(0x3130, 0x318F)]],
[53,	'CJK Miscellaneous', []],
[54,	'Enclosed CJK Letters And Months', [interval(0x3200, 0x32FF)]],
[55,	'CJK Compatibility', [interval(0x3300, 0x33FF)]],
[56,	'Hangul', [interval(0xAC00, 0xD7FF)]],
[57,	'Reserved for Unicode SubRanges', []],
[58,	'Reserved for Unicode SubRanges', []],
[59,	'CJK Unified Ideographs', [interval(0x4E00, 0x9FFF)]],
[60,	'Private Use Area', [interval(0xE800, 0xF8FF)]],
[61,	'CJK Compatibility Ideographs', [interval(0xF900, 0xFAFF)]],
[62,	'Alphabetic Presentation Forms', [
		interval(0xFB00, 0xFB06),
		interval(0xFB13, 0xFB17),
		interval(0xFB1D, 0xFB36),
		interval(0xFB38, 0xFB3C),
		interval(0xFB3E, 0xFB3E),
		interval(0xFB40, 0xFB41),
		interval(0xFB43, 0xFB44),
		interval(0xFB46, 0xFB4F),
		]],
[63,	'Arabic Presentation Forms-A', [interval(0xFB50, 0xFBB1),
				interval(0xFBD3, 0xFD3F),
				interval(0xFD50, 0xFD8F),
				interval(0xFD92, 0xFDC7),
				interval(0xFDF0, 0xFDFD)
				]
		],
[64,	'Combining Half Marks', [interval(0xFE20, 0xFE2F)]],
[65,	'CJK Compatibility Forms', [interval(0xFE30, 0xFE4F)]],
[66,	'Small Form Variants', [interval(0xFE50, 0xFE52),
				interval(0xFE54, 0xFE66),
				interval(0xFE58, 0xFE5B)
				]
		],
[67,	'Arabic Presentation Forms-B', [interval(0xFE70, 0xFE74),
				interval(0xFE76, 0xFEFC),
				interval(0xFEFF, 0xFEFF)
				]
		],
[68,	'Halfwidth And Fullwidth Forms', [interval(0xFF00, 0xFFEF)]],
[69,	'Specials', [interval(0xFFF0, 0xFFFD)]]
]

"""
Overview of the BMP (group=00, plane=00)

======= A-ZONE (alphabetical characters and symbols) =======================
00      (Control characters,) Basic Latin, Latin-1 Supplement (=ISO/IEC 8859-1)
01      Latin Extended-A, Latin Extended-B
02      Latin Extended-B, IPA Extensions, Spacing Modifier Letters
03      Combining Diacritical Marks, Basic Greek, Greek Symbols and Coptic
04      Cyrillic
05      Armenian, Hebrew
06      Basic Arabic, Arabic Extended
07--08  (Reserved for future standardization)
09      Devanagari, Bengali
0A      Gumukhi, Gujarati
0B      Oriya, Tamil
0C      Telugu, Kannada
0D      Malayalam
0E      Thai, Lao
0F      (Reserved for future standardization)
10      Georgian
11      Hangul Jamo
12--1D  (Reserved for future standardization)
1E      Latin Extended Additional
1F      Greek Extended
20      General Punctuation, Super/subscripts, Currency, Combining Symbols
21      Letterlike Symbols, Number Forms, Arrows
22      Mathematical Operators
23      Miscellaneous Technical Symbols
24      Control Pictures, OCR, Enclosed Alphanumerics
25      Box Drawing, Block Elements, Geometric Shapes
26      Miscellaneous Symbols
27      Dingbats
28--2F  (Reserved for future standardization)
30      CJK Symbols and Punctuation, Hiragana, Katakana
31      Bopomofo, Hangul Compatibility Jamo, CJK Miscellaneous
32      Enclosed CJK Letters and Months
33      CJK Compatibility
34--4D  Hangul

======= I-ZONE (ideographic characters) ===================================
4E--9F  CJK Unified Ideographs

======= O-ZONE (open zone) ================================================
A0--DF  (Reserved for future standardization)

======= R-ZONE (restricted use zone) ======================================
E0--F8  (Private Use Area)
F9--FA  CJK Compatibility Ideographs
FB      Alphabetic Presentation Forms, Arabic Presentation Forms-A
FC--FD  Arabic Presentation Forms-A
FE      Combining Half Marks, CJK Compatibility Forms, Small Forms, Arabic-B
FF      Halfwidth and Fullwidth Forms, Specials
"""

def total_intervals( intervals ):
	num = 0
	for i in intervals:
		num += i.len()
	return num

def count_glyphs_in_intervals( font, intervals ):
	num = 0
	for r in intervals:
		font.selection.select( ( 'ranges', None ), r.begin, r.end )
		g = font.selection.byGlyphs
		for e in g:
			num += 1
	return num

def collect_range_info( fontSupport, font, os2supportbit, bit, offset ):
	supports = ( os2supportbit & (1 << bit) ) != 0
	index = bit + offset
	rangeName = ulUnicodeRange[index][1]
	intervals = ulUnicodeRange[index][2]
	nglyphs = count_glyphs_in_intervals( font, intervals )

	fontSupport.setRangeSupport( bit, supports, nglyphs )


class SupportInfo:
	def __init__( self, os2bit, supports, total ):
		self.os2bit = os2bit
		self.supports = supports
		self.total = total

class FontSupport:
	def __init__( self, name, short ):
		self.name = name
		self.short = short
		self.myInfos = []

	def setRangeSupport( self, os2bit, supports, total ):
		self.myInfos.append( SupportInfo( os2bit, supports, total ) )


	def getInfo( self, os2bit ):
		#FIXME this is cheating with the bit
		return self.myInfos[ os2bit ]

fontSupportList = []

def collect_font_range_report( fontPath, short ):

	font = fontforge.open( fontPath )

	r = font.os2_unicoderanges

	fontSupport = FontSupport( font.fontname, short )
	fontSupportList.append( fontSupport )

	for bit in xrange(0,32):
		collect_range_info( fontSupport, font, r[0], bit, 0 )

	for bit in xrange(0,32):
		collect_range_info( fontSupport, font, r[1], bit, 32 )

	for bit in xrange(0,6):
		collect_range_info( fontSupport, font, r[2], bit, 64 )

def print_font_range_report():
	print '<table class="fontrangereport" frame="box" rules="all">'
	print '<caption>'
	print "Unicode 1.1 character ranges vs. FreeFont faces " 
	print '</caption>'
	print '<thead>'
	print '<tr><th>OS/2 character range</th>' 
	print '<th>range<br />total</th>' 
	print '<td></td>' 
	for fsl in fontSupportList:
		print '<th colspan="2">' + fsl.short + '</th>' 
	print '</tr>'
	print '</thead>'
	for r in ulUnicodeRange:
		bit = r[0]
		range_name = r[1]
		intervals = r[2]
		print '<tr><td>' + range_name + '</td>' 
		print '<td class="num">' + str( total_intervals( intervals ) ) \
			+ '</td>'
		print '<td></td>' 
		for fsl in fontSupportList:
			supportInfo = fsl.getInfo( bit )
			supportString = ''
			if supportInfo.supports:
				supportString = '&bull;'
			totalStr = str( supportInfo.total )
			if not supportInfo.total:
				totalStr = '&nbsp;'

			print '<td class="num">' \
				+ totalStr \
				+ '</td><td>'	\
				+ supportString \
				+ '</td>'

		print '</tr>'
	print '</table>'

collect_font_range_report( '../sfd/FreeSerif.sfd', 'Srf' )
collect_font_range_report( '../sfd/FreeSerifItalic.sfd', 'Srf I' )
collect_font_range_report( '../sfd/FreeSerifBold.sfd', 'Srf B' )
collect_font_range_report( '../sfd/FreeSerifBoldItalic.sfd', 'Srf BI' )
collect_font_range_report( '../sfd/FreeSans.sfd', 'Sans' )
collect_font_range_report( '../sfd/FreeSansOblique.sfd', 'Sans O' )
collect_font_range_report( '../sfd/FreeSansBold.sfd', 'Sans B' )
collect_font_range_report( '../sfd/FreeSansBoldOblique.sfd', 'Sans BO' )
collect_font_range_report( '../sfd/FreeMono.sfd', 'Mono' )
collect_font_range_report( '../sfd/FreeMonoOblique.sfd', 'Mono O' )
collect_font_range_report( '../sfd/FreeMonoBold.sfd', 'Mono B' )
collect_font_range_report( '../sfd/FreeMonoBoldOblique.sfd', 'Mono BO' )

print '<html>'
print '<head>'
print '<title>'
print 'Gnu FreeFont character range support'
print '</title>'
print '<style type="text/css">'
print '	td.num { text-align: right }'
print '	th { padding: 0.5em }'
print '	caption { font-size: larger; font-weight: bold; }'
print '</style>'
print '</head>'
print '<body>'
print '<h1>'
print 'Gnu FreeFont support for Unicode 1.1 character ranges'
print '</h1>'
print_font_range_report()
print '<p>'
print "Ranges for which (FontForge reports that) the font's OS/2 support bit is"
print "set are marked with a bullet."
print '</p>'
print '<p>'
print "Why Unicode 1.1?  Because that was the latest version at the time the"
print "OS/2 character range support indicator was included in the TrueType"
print "standard.  This indicator was unfortunately not designed for much"
print "expansion, and unfortunately has not been updated in succeeding standards."
print '</p>'
print '<p>'
print "For many ranges, I took the liberty of reducing the set of characters"
print "considered to the ones listed for the range in the current Unicode"
print "charts, so the number of characters is less than the width of the range."
print '</p>'
print '<p>'
print "Note that there is a discrepancy in the Greek Symbols, Hebrew Extended."
print "and Arabic Extended ranges, between what FontForge reports here and in"
print "its Font Info window under OS/2 Character Ranges."
print "I don't know why, but these ranges are also not well defined in the"
print "TrueType standard."
print '</p>'
print '<p>'
time.tzset()
print 'Generated by <code>ranges.py</code> on ' + time.strftime('%X %x %Z') + '.'
print '</p>'
print '</body>'
print '</html>'
