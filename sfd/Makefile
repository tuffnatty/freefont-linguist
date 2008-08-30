# $Id: Makefile,v 1.3 2008-08-30 11:02:59 Stevan_White Exp $

SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
TTFS=$(SFDS:.sfd=.ttf)
OTFS=$(SFDS:.sfd=.otf)
FF=fontforge -lang=ff -script 

.SUFFIXES: $(SUFFIXES) .sfd .ttf .otf

%.otf : %.sfd
	@ $(FF) ../tools/GenerateOpenType $< 2>> build.log

%.ttf : %.sfd
	@ $(FF) ../tools/GenerateTrueType $< 2>> build.log

all: ttf otf

ttf: $(TTFS)

otf: $(OTFS)

tests:
	@ ../tools/isMonoMono.py; ../tools/validate.py

clean:
	rm -f $(TTFS) $(OTFS) build.log

distclean:
	rm -f $(TTFS) $(OTFS) build.log
