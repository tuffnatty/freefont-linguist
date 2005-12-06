# $Id: Makefile,v 1.3 2005-12-06 10:52:07 peterlin Exp $

ADMIN=README AUTHORS CREDITS COPYING ChangeLog INSTALL
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
ZIPSIG=freefont-ttf-$(DATE).zip.sig
TARSIG=freefont-ttf-$(DATE).tar.gz.sig
SRCTARSIG=freefont-sfd-$(DATE).tar.gz.sig
SIGS=$(ZIPSIG) $(TARSIG) $(SRCTARSIG)

.sfd.ttf:
	cd $(BUILDDIR)/sfd
	$(BUILDDIR)/tools/GenerateTrueType $<

.SUFFIXES: $(SUFFIXES) .sfd .ttf

all: tar srctar

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
	rm -rf $(TMPDIR) $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(SIGS)

distclean:
	rm -rf $(TMPDIR) $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(SIGS) $(TTFS)
