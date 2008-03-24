# $Id: Makefile,v 1.2 2008-03-24 11:59:49 Stevan_White Exp $

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

clean:
	rm -f $(TTFS) $(OTFS) build.log

distclean:
	rm -f $(TTFS) $(OTFS) build.log
