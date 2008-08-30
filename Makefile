# $Id: Makefile,v 1.10 2008-08-30 11:02:59 Stevan_White Exp $

ADMIN=README AUTHORS CREDITS COPYING ChangeLog INSTALL
DATE=$(shell date +"%Y%m%d")
RELEASE=freefont-$(DATE)
BUILDDIR=$(PWD)
TMPDIR=$(BUILDDIR)/$(RELEASE)
OTFZIPFILE=freefont-otf-$(DATE).zip
TTFZIPFILE=freefont-ttf-$(DATE).zip
TTFTARFILE=freefont-ttf-$(DATE).tar.gz
SRCTARFILE=freefont-sfd-$(DATE).tar.gz
ZIPSIG=freefont-ttf-$(DATE).zip.sig
TARSIG=freefont-ttf-$(DATE).tar.gz.sig
SRCTARSIG=freefont-sfd-$(DATE).tar.gz.sig
SIGS=$(ZIPSIG) $(TARSIG) $(SRCTARSIG)

all: ttf otf

ttf: 
	( cd sfd; $(MAKE) ttf )

otf: 
	( cd sfd; $(MAKE) otf )


package: ttftar otfzip srctar

ttfzip: ttf
	rm -rf $(TMPDIR) $(TTFZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.ttf $(TMPDIR)
	zip -r $(TTFZIPFILE) $(RELEASE)/

otfzip: otf
	rm -rf $(TMPDIR) $(OTFZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.otf $(TMPDIR)
	zip -r $(OTFZIPFILE) $(RELEASE)/

ttftar: ttf
	rm -rf $(TMPDIR) $(TTFTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.ttf $(TMPDIR)
	tar czf $(TTFTARFILE) $(RELEASE)/

srctar:
	rm -rf $(TMPDIR) $(SRCTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.sfd $(TMPDIR)
	tar czf $(SRCTARFILE) $(RELEASE)/

tests:
	( cd sfd; $(MAKE) tests )

clean:
	rm -rf $(TMPDIR) 
	rm -f $(TTFZIPFILE) $(TTFTARFILE) $(OTFTARFILE) $(SRCTARFILE) $(SIGS) 
	( cd sfd; $(MAKE) clean )

distclean:
	rm -rf $(TMPDIR) 
	rm -f $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(SIGS)
	( cd sfd; $(MAKE) distclean )
