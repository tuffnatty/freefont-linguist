# $Id: Makefile,v 1.5 2008-03-21 21:51:54 Stevan_White Exp $

ADMIN=README AUTHORS CREDITS COPYING ChangeLog INSTALL
SFDS=FreeMonoBoldOblique.sfd FreeMonoBold.sfd FreeMonoOblique.sfd FreeMono.sfd \
FreeSansBoldOblique.sfd FreeSansBold.sfd FreeSansOblique.sfd FreeSans.sfd \
FreeSerifBoldItalic.sfd FreeSerifBold.sfd FreeSerifItalic.sfd FreeSerif.sfd
TTFS=$(SFDS:.sfd=.ttf)
DATE=$(shell date +"%Y%m%d")
RELEASE=freefont-$(DATE)
VPATH=sfd	# make's search path for dependencies
BUILDDIR=$(PWD)
TMPDIR=$(BUILDDIR)/$(RELEASE)
ZIPFILE=freefont-ttf-$(DATE).zip
TARFILE=freefont-ttf-$(DATE).tar.gz
SRCTARFILE=freefont-sfd-$(DATE).tar.gz
ZIPSIG=freefont-ttf-$(DATE).zip.sig
TARSIG=freefont-ttf-$(DATE).tar.gz.sig
SRCTARSIG=freefont-sfd-$(DATE).tar.gz.sig
SIGS=$(ZIPSIG) $(TARSIG) $(SRCTARSIG)
FF=fontforge -lang=ff -script 

.SUFFIXES: $(SUFFIXES) .sfd .ttf

%.ttf : %.sfd
	@ $(FF) tools/GenerateTrueType $< 2>> build.log

all: ttf

ttf: $(TTFS)

package: tar srctar

zip: $(TTFS)
	rm -rf $(TMPDIR) $(ZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) $(TMPDIR)
	cp -a $(TTFS) $(TMPDIR)
	zip -r $(ZIPFILE) $(RELEASE)/

tar: $(TTFS)
	rm -rf $(TMPDIR) $(TARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) $(TMPDIR)
	cp -a $(TTFS) $(TMPDIR)
	tar czf $(TARFILE) $(RELEASE)/

srctar: $(SFDS)
	rm -rf $(TMPDIR) $(SRCTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.sfd $(TMPDIR)
	tar czf $(SRCTARFILE) $(RELEASE)/

clean:
	rm -rf $(TMPDIR) 
	rm -f $(TTFS) $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(SIGS) build.log

distclean:
	rm -rf $(TMPDIR) 
	rm -f $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(SIGS) $(TTFS) build.log
