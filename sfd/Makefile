# $Id: Makefile,v 1.5 2008-09-22 14:29:30 Stevan_White Exp $

SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
MSFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd
TTFS=$(SFDS:.sfd=.ttf)
OTFS=$(SFDS:.sfd=.otf)
FF=fontforge -lang=ff -script 
FFPY=fontforge -lang=py -script 

.SUFFIXES: $(SUFFIXES) .sfd .ttf .otf

%.otf : %.sfd
	@ ( $(FFPY) ../tools/GenerateOpenType $< 2>/dev/stdout 1>/dev/stderr | tail -n +4 ) 2>&1 

%.ttf : %.sfd
	@ ( $(FF) ../tools/GenerateTrueType $< 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1 

all: ttf otf

ttf: $(TTFS)

otf: $(OTFS)

tests:
	@ ( $(FFPY) ../tools/isMonoMono.py $(MSFDS) 3>&1 1>&2 2>&3 | tail -n +4 ) 3>&1 1>&2 2>&3 2>&1
	@ ../tools/checkGlyphNumbers.py 2>&1
	@ ../tools/validate.py 2>&1

clean:
	rm -f $(TTFS) $(OTFS) build.log

distclean:
	rm -f $(TTFS) $(OTFS) build.log
