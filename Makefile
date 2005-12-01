# $Id: Makefile,v 1.1 2005-12-01 15:03:24 peterlin Exp $

ADMIN=README AUTHORS CREDITS COPYING ChangeLog
SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
TTFS=$(SFDS:.sfd=.ttf)
DATE=$(shell date +"%Y%m%d")
RELEASE=freefont-$(DATE)
VPATH=sfd
BUILDDIR=$(PWD)
TMPDIR=$(BUILDDIR)/$(RELEASE)
ZIPFILE=$(RELEASE).zip
TARFILE=$(RELEASE).tar.gz

.sfd.ttf:
	cd $(BUILDDIR)/sfd
	$(BUILDDIR)/tools/GenerateTrueType $<

.SUFFIXES: $(SUFFIXES) .sfd .ttf

all: zip tar

ttf: $(SFDS)
	cd $(BUILDDIR)/sfd
	for SFD in $(SFDS); do $(BUILDDIR)/tools/GenerateTrueType $(SFD); done

zip: $(TTFS)
	rm -rf $(TMPDIR) $(ZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) $(TTFS) $(TMPDIR)
	zip -r $(ZIPFILE) $(RELEASE)/

tar: $(TTFS)
	rm -rf $(TMPDIR) $(ZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) $(TTFS) $(TMPDIR)
	tar czf $(TARFILE) $(RELEASE)/

clean:
	rm -rf $(TMPDIR) $(ZIPFILE)

distclean:
	rm -rf $(TMPDIR) $(ZIPFILE) $(TTFS)
