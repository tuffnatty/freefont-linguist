# $Id$

SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
MSFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd
TTFS=$(SFDS:.sfd=.ttf)
OTFS=$(SFDS:.sfd=.otf)
WOFFS=$(SFDS:.sfd=.woff)
FFBIN=/usr/local/bin/fontforge
FFLIBS=/usr/local/lib/fontforge_22_02_2011
FFBIN=/usr/local/bin/fontforge_22_02_2011
FFLIBS=/usr/local/lib/fontforge-new
FFBIN=/usr/local/bin/fontforge-new
FFBIN=/usr/bin/fontforge
FFLIBS=/usr/lib/fontforge
FFLIBS=/usr/local/lib/fontforge_31_07_2012
FFBIN=/usr/local/bin/fontforge_31_07_2012
FF=LD_LIBRARY_PATH=${FFLIBS} ${FFBIN}
# newer versions need flag --quiet for pretty output, but others choke on it
FFFF=$(FF) -lang=ff -script 
FFPY=$(FF) --quiet -lang=py -script 
FFPY=$(FF) -lang=py -script 

# my distro version perversely lost the Version line!
ffver=`${FF} --version 2>&1 \
	| grep -E "Version|libfontforge" \
	| sed -e "s/^libfontforge //" \
	| sed -e "s/^ Version: //" \
	2>/dev/null`

TESTFFVER=if test -z "$(ffver)"; then \
	echo Could not find version of FontForge program; exit 1; fi

TESTFFEXIST=if [ ! -f "$(FFBIN)" ] && [ ! -h "$(FFBIN)" ]; then \
	echo Fontforge program not found at $(FFBIN); exit 1; fi

TESTFFOLD=if [ "${ffver}" -lt 20080429 ]; then \
	echo FontForge version $(ffver) too old; exit 0; fi

TESTFF=${TESTFFVER}; ${TESTFFEXIST}; ${TESTFFOLD}

GENTT=../tools/generate/TrueType
GENOT=../tools/generate/OpenType
GENWO=../tools/generate/WOFF
# FIXME logic of setting FixedPitch is poor.  
IFP=../tools/generate/tweeks/set_isFixedPitch.py
CFS=../tools/generate/tweeks/correct_fsSelection.py

.SUFFIXES: $(SUFFIXES) .sfd .ttf .otf .woff

%.otf : %.sfd
	@ $(TESTFF)
	@ ( $(FFPY) ${GENOT} $< 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1 
	@ ( $(IFP) $@ 3>&1 1>&2 2>&3 | tail -n +4 ) 
	@ ( $(CFS) $@ 3>&1 1>&2 2>&3 | tail -n +4 ) 

%.ttf : %.sfd
	@ $(TESTFF)
	@ ( $(FFPY) $(GENTT) $< 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1 
	@ ( $(IFP) $@ 3>&1 1>&2 2>&3 | tail -n +4 ) 
	@ ( $(CFS) $@ 3>&1 1>&2 2>&3 | tail -n +4 ) 

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
	@ $(FFPY) ../tools/test/checkOTGlyphClass.py `pwd` $(SFDS) 2>&1
	@ $(FFPY) ../tools/test/validate.py `pwd` $(SFDS) 2>&1

clean:
	rm -f $(TTFS) $(OTFS) $(WOFFS) build.log

distclean:
	rm -f $(TTFS) $(OTFS) $(WOFFS) build.log
