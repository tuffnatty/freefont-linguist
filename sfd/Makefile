# $Id: Makefile,v 1.8 2010-04-06 19:33:54 Stevan_White Exp $

SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
MSFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd
TTFS=$(SFDS:.sfd=.ttf)
OTFS=$(SFDS:.sfd=.otf)
WOFFS=$(SFDS:.sfd=.woff)
FF=/usr/local/bin/fontforge 
FFFF=$(FF) -lang=ff -script 
FFPY=$(FF) -lang=py -script 

ffversion=`${FF} --version 2> /dev/null | grep '^fontforge' | sed -e 's/^fontforge //'`

TESTFFEXIST=if test -z ${ffversion}; then echo FontForge program is required to build FreeFont; exit 1; fi

TESTFFOLD=if test ${ffversion} -lt 20080429 ; then echo FontForge version too old; exit 1; fi

TESTFF2012=if test ${ffversion} -eq 20120731 ; then echo FontForge version 20120731 screws up right-to-left kerning tables.  \\nPlease use a different version when building FreeFont.; exit 1; fi

TESTFF=${TESTFFEXIST}; ${TESTFFOLD}; ${TESTFF2012}

GENTT=../tools/generate/TrueType
GENOT=../tools/generate/OpenType
GENWO=../tools/generate/WOFF
# FIXME logic of setting FixedPitch is poor.  
IFP=../tools/generate/tweeks/set_isFixedPitch.py

.SUFFIXES: $(SUFFIXES) .sfd .ttf .otf .woff

%.otf : %.sfd
	@ $(TESTFF)
	@ ( $(FFPY) ${GENOT} $< 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1 
	@ ( $(IFP) $@ 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1

%.ttf : %.sfd
	@ $(TESTFF)
	@ ( $(FFPY) $(GENTT) $< 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1 
	@ ( $(IFP) $@ 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1

%.woff : %.sfd
	@ $(TESTFF)
	@ ( $(FFPY) $(GENWO) $< 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1 

all: ttf otf woff

ttf: $(TTFS)

otf: $(OTFS)

woff: $(WOFFS)

tests:
	@ $(TESTFF)
	@ ( $(FFPY) ../tools/test/isMonoMono.py $(MSFDS) 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1
	@ $(FFPY) ../tools/test/checkGlyphNumbers.py `pwd` $(SFDS) 2>&1
	@ $(FFPY) ../tools/test/validate.py 2>&1

clean:
	rm -f $(TTFS) $(OTFS) $(WOFFS) build.log

distclean:
	rm -f $(TTFS) $(OTFS) $(WOFFS) build.log
