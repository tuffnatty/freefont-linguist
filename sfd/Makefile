# $Id: Makefile,v 1.8 2010-04-06 19:33:54 Stevan_White Exp $

SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
MSFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd
TTFS=$(SFDS:.sfd=.ttf)
OTFS=$(SFDS:.sfd=.otf)
FF=fontforge -lang=ff -script 
FFPY=fontforge -lang=py -script 

ffversion=`fontforge --version 2> /dev/null | grep '^fontforge' | sed -e 's/^fontforge //'`

TESTFF=if test -z ${ffversion}; then echo Fontforge program is required to build FreeFont; exit 1; fi; if test `fontforge --version 2> /dev/null | grep '^fontforge' | sed -e 's/^fontforge //'` -lt 20080429 ; then echo FontForge version too old; exit 1; fi


.SUFFIXES: $(SUFFIXES) .sfd .ttf .otf

%.otf : %.sfd
	@ $(TESTFF)
	@ ( $(FFPY) ../tools/generate/OpenType $< 2>/dev/stdout 1>/dev/stderr | tail -n +4 ) 2>&1 

%.ttf : %.sfd
	@ $(TESTFF)
	@ ( $(FFPY) ../tools/generate/TrueType $< 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1 

all: ttf otf

ttf: $(TTFS)

otf: $(OTFS)

tests:
	@ $(TESTFF)
	@ ( $(FFPY) ../tools/test/isMonoMono.py $(MSFDS) 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1
	@ ../tools/test/checkGlyphNumbers.py 2>&1
	@ ../tools/test/validate.py 2>&1

clean:
	rm -f $(TTFS) $(OTFS) build.log

distclean:
	rm -f $(TTFS) $(OTFS) build.log
