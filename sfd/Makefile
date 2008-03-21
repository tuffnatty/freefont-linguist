# $Id: Makefile,v 1.1 2008-03-21 23:48:56 Stevan_White Exp $

SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
TTFS=$(SFDS:.sfd=.ttf)
FF=fontforge -lang=ff -script 

.SUFFIXES: $(SUFFIXES) .sfd .ttf

%.ttf : %.sfd
	@ $(FF) ../tools/GenerateTrueType $< 2>> build.log

all: ttf

ttf: $(TTFS)

clean:
	rm -f $(TTFS) build.log

distclean:
	rm -f $(TTFS) build.log
