"""
Makes an HTML table showing how many glyphs are in each range in each font,
and tries to collate that with the OS/2 character range support bit flags.

Runs under FontForge.
	fontforge -script ranges.py

This is a hack--in no way authoritative.  
Lots of guesswork; much is wrong; the coding is gross.

See
http://www.w3.org/TR/REC-CSS2/notes.html
http://shlimazl.nm.ru/eng/fonts_ttf.htm
http://www.evertype.com/standards/iso10646/ucs-collections.html

The intervals are partly just the assigned interval, but often I have
listed the ranges that have characters assigned to them.


$Id: ranges.py,v 1.15 2008-05-18 19:17:24 Stevan_White Exp $
"""
__author__ = "Stevan White <stevan.white@googlemail.com>"

import fontforge
import sys
import time


class interval:
	def __init__( self, begin, end ):
		self.begin = begin
		self.end = end

	def len( self ):
		return 1 + self.end - self.begin

	def __str__( self ):
		return '[' + str( self.begin ) + ',' + str( self.end ) + ']'

ulUnicodeRange = [
[0,	'Basic Latin', [interval(0x0020, 0x007E)] ],
[1,	'Latin-1 Supplement',[interval(0x00A0, 0x00FF)] ],
[2,	'Latin Extended-A',	[interval(0x0100, 0x017F)] ],
[3,	'Latin Extended-B',     [interval(0x0180, 0x024F)]],
#Latin Extended C and D?
[4,	'IPA Extensions',     [interval(0x0250, 0x02AF)]],
[5,	'Spacing Modifier Letters',     [interval(0x02B0, 0x02FF)]],
[6,	'Combining Diacritical Marks',     [interval(0x0300, 0x036F)]],
[7,	'Basic Greek',     [interval(0x0370, 0x0377),
			interval(0x037A, 0x037E),
			interval(0x0384, 0x038A),
			interval(0x038C, 0x038C),
			interval(0x038E, 0x03A1),
			interval(0x03A3, 0x03CF)] ],
[8,	'Greek Symbols And Coptic',     [interval(0x03D0, 0x03FF)]],	# unclear.
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
[11,	'Basic Hebrew',    [
			interval(0x05D0, 0x05EA),
			interval(0x05F0, 0x05F4)
	]
	],
[12,	'Hebrew Extended (A and B blocks combined)',    
	[interval(0x0591, 0x05C7),
			interval(0x05D0, 0x05EA),
			interval(0x05F0, 0x05F4)
		]], # See http://webcenter.ru/~kazarn/eng/ululinks.htm
[13,	'Basic Arabic',     [interval(0x0600, 0x0603),
				interval(0x0606, 0x061B),
				interval(0x061E, 0x061F),
				interval(0x0621, 0x0652)
	]
	],
[14,	'Arabic Extended', [interval(0x0653, 0x06FF)]],	# unclear
[15,	'Devanagari',     [interval(0x0901, 0x0939),
			interval(0x093C, 0x094D),
			interval(0x0950, 0x0954),
			interval(0x0958, 0x0972),
			interval(0x097B, 0x097F)
			]],
[16,	'Bengali',     [interval(0x0981, 0x0983),
		interval(0x0985, 0x098C),
		interval(0x098F, 0x0990),
		interval(0x0993, 0x09A8),
		interval(0x09AA, 0x09B0),
		interval(0x09B2, 0x09B2),
		interval(0x09B6, 0x09B9),
		interval(0x09BC, 0x09C4),
		interval(0x09C7, 0x09C8),
		interval(0x09CB, 0x09CE),
		interval(0x09D7, 0x09D7),
		interval(0x09DC, 0x09DD),
		interval(0x09DF, 0x09E3),
		interval(0x09E6, 0x09FA),
	]],
[17,	'Gurmukhi',     [interval(0x0A01, 0x0A03),
		interval(0x0A05, 0x0A0A),
		interval(0x0A0F, 0x0A10),
		interval(0x0A13, 0x0A28),
		interval(0x0A2A, 0x0A30),
		interval(0x0A32, 0x0A33),
		interval(0x0A35, 0x0A36),
		interval(0x0A38, 0x0A39),
		interval(0x0A3C, 0x0A3C),
		interval(0x0A3E, 0x0A42),
		interval(0x0A47, 0x0A48),
		interval(0x0A4B, 0x0A4D),
		interval(0x0A51, 0x0A51),
		interval(0x0A59, 0x0A5C),
		interval(0x0A5E, 0x0A5E),
		interval(0x0A66, 0x0A75),
		]],
[18,	'Gujarati',     [interval(0x0A81, 0x0A83),
		interval(0x0A85, 0x0A8D),
		interval(0x0A8F, 0x0A91),
		interval(0x0A93, 0x0AA8),
		interval(0x0AAA, 0x0AB0),
		interval(0x0AB2, 0x0AB3),
		interval(0x0AB5, 0x0AB9),
		interval(0x0ABC, 0x0AC5),
		interval(0x0AC7, 0x0AC9),
		interval(0x0ACB, 0x0ACD),
		interval(0x0AD0, 0x0AD0),
		interval(0x0AE0, 0x0AE3),
		interval(0x0AE6, 0x0AEF),
		interval(0x0AF1, 0x0AF1)
		]],
[19,	'Oriya',     [interval(0x0B01, 0x0B03),
		interval(0x0B05, 0x0B0C),
		interval(0x0B0F, 0x0B10),
		interval(0x0B13, 0x0B28),
		interval(0x0B2A, 0x0B30),
		interval(0x0B32, 0x0B33),
		interval(0x0B35, 0x0B39),
		interval(0x0B3C, 0x0B44),
		interval(0x0B47, 0x0B48),
		interval(0x0B4B, 0x0B4D),
		interval(0x0B56, 0x0B57),
		interval(0x0B5C, 0x0B5D),
		interval(0x0B5F, 0x0B63),
		interval(0x0B66, 0x0B71),
	]],
[20,	'Tamil',     [interval(0x0B82, 0x0B83),
		interval(0x0B85, 0x0B8A),
		interval(0x0B8E, 0x0B91),
		interval(0x0B92, 0x0B95),
		interval(0x0B99, 0x0B9A),
		interval(0x0B9C, 0x0B9C),
		interval(0x0B9E, 0x0B9F),
		interval(0x0BA3, 0x0BA4),
		interval(0x0BA8, 0x0BAA),
		interval(0x0BAE, 0x0BB9),
		interval(0x0BBE, 0x0BC2),
		interval(0x0BC6, 0x0BC8),
		interval(0x0BCA, 0x0BCD),
		interval(0x0BD0, 0x0BD0),
		interval(0x0BD7, 0x0BD7),
		interval(0x0BE6, 0x0BFA)
	]],
[21,	'Telugu',     [interval(0x0C01, 0x0C03),
		interval(0x0C05, 0x0C0C),
		interval(0x0C0E, 0x0C11),
		interval(0x0C12, 0x0C28),
		interval(0x0C2A, 0x0C33),
		interval(0x0C35, 0x0C39),
		interval(0x0C3d, 0x0C44),
		interval(0x0C46, 0x0C48),
		interval(0x0C4a, 0x0C4d),
		interval(0x0C55, 0x0C56),
		interval(0x0C58, 0x0C59),
		interval(0x0C60, 0x0C63),
		interval(0x0C66, 0x0C6f),
		interval(0x0C78, 0x0C7f),
			]
			],
[22,	'Kannada',     [interval(0x0C82, 0x0C83),
		interval(0x0C85, 0x0C8C),		
		interval(0x0C8E, 0x0C90),		
		interval(0x0C92, 0x0CA8),		
		interval(0x0CAA, 0x0CB3),		
		interval(0x0CB5, 0x0CB9),		
		interval(0x0CBC, 0x0CC4),		
		interval(0x0CC6, 0x0CC8),		
		interval(0x0CCA, 0x0CCD),		
		interval(0x0CD5, 0x0CD6),		
		interval(0x0CDE, 0x0CDE),		
		interval(0x0CE0, 0x0CE3),		
		interval(0x0CE6, 0x0CEF),		
		interval(0x0CF1, 0x0CF2),		
	]],
[23,	'Malayalam',     [interval(0x0D02, 0x0D03),
		interval(0x0D05, 0x0D0C),
		interval(0x0D0E, 0x0D10),
		interval(0x0D12, 0x0D28),
		interval(0x0D2A, 0x0D39),
		interval(0x0D3D, 0x0D44),
		interval(0x0D46, 0x0D48),
		interval(0x0D4A, 0x0D4D),
		interval(0x0D57, 0x0D57),
		interval(0x0D60, 0x0D63),
		interval(0x0D66, 0x0D75),
		interval(0x0D79, 0x0D7F),
	]],
[24,	'Thai',     [interval(0x0E01, 0x0E3A),
			interval(0x0E3F, 0x0E5B)
			]
		],
[25,	'Lao',     [interval(0x0E80, 0x0EFF)]],
[26,	'Basic Georgian',     [interval(0x10D0, 0x10FC)]],	# now these are
[27,	'Georgian Extended', [interval(0x10A0, 0x10CF)]],	# in same range
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
[34,	'Combining Diacritical Marks For Symbols',     [interval(0x20D0, 0x20F0)]],
[35,	'Letterlike Symbols',     [interval(0x2100, 0x214F)]],
[36,	'Number Forms',     [interval(0x2153, 0x2188)]],
[37,	'Arrows',     [interval(0x2190, 0x21FF)]],
[38,	'Mathematical Operators',     [ #FIXME there are subranges
	interval(0x2200, 0x22FF),
	interval(0x2A00, 0x2AFF),	# Supplemental Mathematical Operators
	interval(0x27C0, 0x27EF),	# Miscellaneous Mathematical Symbols-A
	interval(0x2980, 0x29FF)	# Miscellaneous Mathematical Symbols-B
	]
		],
[39,	'Miscellaneous Technical',     [interval(0x2300, 0x23FF)]],
[40,	'Control Pictures',     [interval(0x2400, 0x243F)]],
[41,	'Optical Character Recognition',     [interval(0x2440, 0x245F)]],
[42,	'Enclosed Alphanumerics',     [interval(0x2460, 0x24FF)]],
[43,	'Box Drawing',     [interval(0x2500, 0x257F)]],
[44,	'Block Elements',     [interval(0x2580, 0x259F)]],
[45,	'Geometric Shapes',     [interval(0x25A0, 0x25FF)]],
[46,	'Miscellaneous Symbols',     [
			interval(0x2600, 0x269D),
			interval(0x26A0, 0x26C3)
			]
			],
[47,	'Dingbats',     [interval(0x2701, 0x27BF)]],	#FIXME several intervals
[48,	'CJK Symbols And Punctuation', [interval(0x3000, 0x303F)]],
[49,	'Hiragana', [interval(0x3040, 0x309F)]],
[50,	'Katakana', [interval(0x30A0, 0x30FF)]],
[51,	'Bopomofo', [interval(0x3100, 0x312F)]],
[52,	'Hangul Compatibility Jamo', [interval(0x3130, 0x318F)]],
[53,	'CJK Miscellaneous', [interval(0x3190, 0x319F)]],
[54,	'Enclosed CJK Letters And Months', [interval(0x3200, 0x32FF)]],
[55,	'CJK Compatibility', [interval(0x3300, 0x33FF)]],
[56,	'Hangul', [interval(0x3400, 0x3D2D)]],
[57,	'Hangul Supplementary-A', [interval(0x3D2E, 0x44B7)]],
[58,	'Hangul Supplementary-B', [interval(0x44B8, 0x4DFF)]],
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
[69,	'Specials', [interval(0xFFF0, 0xFFFD)]],
[70, 	'Tibetan', [interval(0x0F00, 0x0FFF)]],
[71, 	'Syriac', [interval(0x0700, 0x070D),
		interval(0x070F, 0x074A),
		interval(0x074D, 0x074F)
	]],
[72, 	'Thaana', [interval(0x0780, 0x07B1)]],
[73, 	'Sinhala', [interval(0x0D80, 0x0DFF)]],
[74, 	'Myanmar', [interval(0x1000, 0x109F)]],
[75, 	'Ethiopic', [
		interval(0x1200, 0x1248),
		interval(0x124A, 0x124D),
		interval(0x1250, 0x1256),
		interval(0x1258, 0x1258),
		interval(0x125A, 0x125D),
		interval(0x1260, 0x1288),
		interval(0x128A, 0x128D),
		interval(0x1290, 0x12B0),
		interval(0x12B2, 0x12B5),
		interval(0x12B8, 0x12BE)
		]
		],
[76,	'Cherokee', [interval(0x13A0, 0x13F4)]],
[77, 	'Unified Canadian Aboriginal Syllabics', [interval(0x1401, 0x14DF)]],
[78, 	'Ogham', [interval(0x1680, 0x169F)]],
[79, 	'Runic', [interval(0x16A0, 0x16F1)]],
[80, 	'Khmer', [interval(0x1780, 0x17FF)]],
[81, 	'Mongolian', [interval(0x1800, 0x18AF)]],	#FIXME ranges
[82, 	'Braille Patterns', [interval(0x2800, 0x28FF)]],
[83, 	'Yi Syllables, Radicals', [interval(0xA000, 0xA0EF),
		interval(0xA490, 0xA4CF)]
		],
[84, 	'Tagalog Hanunoo Buhid Tagbanwa', 
		[interval(0x1700, 0x1714),
		interval(0x1720, 0x1736),
		interval(0x1740, 0x1753),
		interval(0x1750, 0x1773)
		]
		],
[85, 	'Old Italic', [interval(0x10300, 0x10320)]],
[86, 	'Gothic', [interval(0x10330, 0x1034A)]],
[87, 	'Deseret', [interval(0x10400, 0x1044F)]],
[88, 	'Byzantine & Western Musical Symbols', [interval(0x1D000, 0x1D0F5),
			interval(0x1D100, 0x1D1DD)]],
[89, 	'Mathematical Alphanumeric Symbols', [interval(0x1D400, 0x1D4FF)]],
[90, 	'Private Use (plane 15,16)', []],
[91, 	'Variation Selectors', []],
[92, 	'Tags', []],
[93, 	'Reserved for Unicode SubRanges', []],
[94, 	'Reserved for Unicode SubRanges', []],
[95, 	'Reserved for Unicode SubRanges', []],
#[96-127, 	'Reserved for Unicode SubRanges', []]
]

"""
From the OpenType standard 
http://www.microsoft.com/OpenType/OTSpec/os2.htm

0 	Basic Latin
1 	Latin-1 Supplement
2 	Latin Extended-A
3 	Latin Extended-B
4 	IPA Extensions
5 	Spacing Modifier Letters
6 	Combining Diacritical Marks
7 	Greek and Coptic
8 	Reserved for Unicode SubRanges
9 	Cyrillic
  	Cyrillic Supplementary
10 	Armenian
11 	Hebrew
12 	Reserved for Unicode SubRanges
13 	Arabic
14 	Reserved for Unicode SubRanges
15 	Devanagari
16 	Bengali
17 	Gurmukhi
18 	Gujarati
19 	Oriya
20 	Tamil
21 	Telugu
22 	Kannada
23 	Malayalam
24 	Thai
25 	Lao
26 	Georgian
27 	Reserved for Unicode SubRanges
28 	Hangul Jamo
29 	Latin Extended Additional
30 	Greek Extended
31 	General Punctuation
32 	Superscripts And Subscripts
33 	Currency Symbols
34 	Combining Diacritical Marks For Symbols
35 	Letterlike Symbols
36 	Number Forms
37 	Arrows
  	Supplemental Arrows-A
  	Supplemental Arrows-B
38 	Mathematical Operators
  	Supplemental Mathematical Operators
  	Miscellaneous Mathematical Symbols-A
  	Miscellaneous Mathematical Symbols-B
39 	Miscellaneous Technical
40 	Control Pictures
41 	Optical Character Recognition
42 	Enclosed Alphanumerics
43 	Box Drawing
44 	Block Elements
45 	Geometric Shapes
46 	Miscellaneous Symbols
47 	Dingbats
48 	CJK Symbols And Punctuation
49 	Hiragana
50 	Katakana
  	Katakana Phonetic Extensions
51 	Bopomofo
  	Bopomofo Extended
52 	Hangul Compatibility Jamo
3 	Reserved for Unicode SubRanges
54 	Enclosed CJK Letters And Months
55 	CJK Compatibility
56 	Hangul Syllables
57 	Non-Plane 0 *
58 	Reserved for Unicode SubRanges
59 	CJK Unified Ideographs
  	CJK Radicals Supplement
  	Kangxi Radicals
  	Ideographic Description Characters
  	CJK Unified Ideograph Extension A
  	CJK Unified Ideographs Extension B
  	Kanbun
60 	Private Use Area
61 	CJK Compatibility Ideographs
  	CJK Compatibility Ideographs Supplement
62 	Alphabetic Presentation Forms
63 	Arabic Presentation Forms-A
64 	Combining Half Marks
65 	CJK Compatibility Forms
66 	Small Form Variants
67 	Arabic Presentation Forms-B
68 	Halfwidth And Fullwidth Forms
69 	Specials
70 	Tibetan
71 	Syriac
72 	Thaana
73 	Sinhala
74 	Myanmar
75 	Ethiopic
76	Cherokee
77 	Unified Canadian Aboriginal Syllabics
78 	Ogham
79 	Runic
80 	Khmer
81 	Mongolian
82 	Braille Patterns
83 	Yi Syllables
  	Yi Radicals
84 	Tagalog
  	Hanunoo
  	Buhid
  	Tagbanwa
85 	Old Italic
86 	Gothic
87 	Deseret
88 	Byzantine Musical Symbols
  	Musical Symbols
89 	Mathematical Alphanumeric Symbols
90 	Private Use (plane 15)
  	Private Use (plane 16)
91 	Variation Selectors
92 	Tags
93-127 	Reserved for Unicode SubRanges
"""
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

"""
See also
http://developer.apple.com/textfonts/TTRefMan/RM06/Chap6OS2.html
Says 128 bits are split into 96 and 32 bits.
96 is Unicode block, 32 for script sets...

This talks about TrueType and OpenType versions
http://webcenter.ru/~kazarn/eng/fonts_ttf.htm#os2tab
and this says what the ranges of Hebrew, Greek etc are

OK, the right thing is here: the OpenType specs
http://www.microsoft.com/OpenType/OTSpec/os2.htm
"""

def total_intervals( intervals ):
	num = 0
	for i in intervals:
		num += i.len()
	return num

def count_glyphs_in_intervals( font, intervals ):
	num = 0
	for r in intervals:
		# select() will throw up if try to select value 
		# beyond the range of the encoding
		if r.begin < len( font ) and r.begin < len( font ):
			font.selection.select( ( 'ranges', None ),
					r.begin, r.end )
		g = font.selection.byGlyphs
		for e in g:
			num += 1
	return num

def intervals_to_stderr( intervals ):
	for r in intervals:
		print >> sys.stderr, "\t" + str( r )

def collect_range_info( fontSupport, font, os2supportbit, bit, offset ):
	supports = ( os2supportbit & (1 << bit) ) != 0
	index = bit + offset
	rangeName = ulUnicodeRange[index][1]
	intervals = ulUnicodeRange[index][2]
	nglyphs = 0
	try: 
		nglyphs = count_glyphs_in_intervals( font, intervals )
	except ValueError:
		print >> sys.stderr, "Problem with interval in " + font.fontname
		print >> sys.stderr, "\t" + rangeName
		intervals_to_stderr( intervals )
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
	""" Currently searches the first 96 bits of the os2_unicoderanges
	"""

	font = fontforge.open( fontPath )

	r = font.os2_unicoderanges

	fontSupport = FontSupport( font.fontname, short )
	fontSupportList.append( fontSupport )

	for bit in xrange(0,32):
		collect_range_info( fontSupport, font, r[0], bit, 0 )

	for bit in xrange(0,32):
		collect_range_info( fontSupport, font, r[1], bit, 32 )

	for bit in xrange(0,32):
		collect_range_info( fontSupport, font, r[2], bit, 64 )

def print_font_range_table():
	print '<table class="fontrangereport" frame="box" rules="all">'
	print '<caption>'
	print "OS/2 character ranges vs. FreeFont faces " 
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
table_explanation = """
<p>
Ranges for which (FontForge reports that) the font's OS/2 support
bit is set are marked with a bullet.
</p>
<p>
For many ranges, I took the liberty of reducing the set of 
characters considered to the ones listed for the range in the
current Unicode charts, so the number of characters is less than
the width of the range.
</p>
<p>
Note that there is a discrepancy in the Greek Symbols, Hebrew 
Extended and Arabic Extended ranges, between what FontForge 
reports here and in its Font Info window under OS/2 Character 
Ranges. I don't know why, but these ranges are also not well
defined in the TrueType standard.
</p>
<p>
Note the 2 characters from Devanagri.  These are the danda and double-danda
used by other Inidic scripts.
</p>
"""

def print_font_range_report():
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
	print 'Gnu FreeFont support for OpenType OS/2 character ranges'
	print '</h1>'
	print_font_range_table()
	print '<p>'
	print table_explanation
	time.tzset()
	print 'Generated by <code>ranges.py</code> on ' \
			+ time.strftime('%X %x %Z') + '.'
	print '</p>'
	print '</body>'
	print '</html>'

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

print_font_range_report()
