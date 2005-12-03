# $Id: Makefile,v 1.2 2005-12-03 09:25:44 peterlin Exp $

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
ZIPFILE=freefont-ttf-$(DATE).zip
TARFILE=freefont-ttf-$(DATE).tar.gz
SRCTARFILE=freefont-sfd-$(DATE).tar.gz

.sfd.ttf:
	cd $(BUILDDIR)/sfd
	$(BUILDDIR)/tools/GenerateTrueType $<

.SUFFIXES: $(SUFFIXES) .sfd .ttf

all: zip tar srctar

ttf: $(SFDS)
	cd $(BUILDDIR)/sfd
	for SFD in $(SFDS); do $(BUILDDIR)/tools/GenerateTrueType $(SFD); done

zip: $(TTFS)
	rm -rf $(TMPDIR) $(ZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) $(TTFS) $(TMPDIR)
	zip -r $(ZIPFILE) $(RELEASE)/

tar: $(TTFS)
	rm -rf $(TMPDIR) $(TARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) $(TTFS) $(TMPDIR)
	tar czf $(TARFILE) $(RELEASE)/

srctar: $(SFDS)
	rm -rf $(TMPDIR) $(SRCTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.sfd $(TMPDIR)
	tar czf $(SRCTARFILE) $(RELEASE)/

clean:
	rm -rf $(TMPDIR) $(ZIPFILE) $(TARFILE) $(SRCTARFILE)

distclean:
	rm -rf $(TMPDIR) $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(TTFS)
