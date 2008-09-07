# $Id: Makefile,v 1.4 2008-09-07 21:07:25 Stevan_White Exp $

SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
TTFS=$(SFDS:.sfd=.ttf)
OTFS=$(SFDS:.sfd=.otf)
FF=fontforge -lang=ff -script 

.SUFFIXES: $(SUFFIXES) .sfd .ttf .otf

%.otf : %.sfd
	@ fontforge -script ../tools/GenerateOpenType.py $< 2>> build.log

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
