# $Id: Makefile,v 1.13 2010-09-22 06:09:49 Stevan_White Exp $

ADMIN=README AUTHORS CREDITS COPYING ChangeLog INSTALL
DATE=$(shell date +"%Y%m%d")
RELEASE=freefont-$(DATE)
BUILDDIR=$(PWD)
TMPDIR=$(BUILDDIR)/$(RELEASE)
OTFZIPFILE=freefont-otf-$(DATE).zip
TTFZIPFILE=freefont-ttf-$(DATE).zip
WOFFZIPFILE=freefont-woff-$(DATE).zip
OTFTARFILE=freefont-otf-$(DATE).tar.gz
TTFTARFILE=freefont-ttf-$(DATE).tar.gz
WOFFTARFILE=freefont-woff-$(DATE).tar.gz
SRCTARFILE=freefont-sfd-$(DATE).tar.gz
ZIPSIG=freefont-ttf-$(DATE).zip.sig
TARSIG=freefont-ttf-$(DATE).tar.gz.sig
SRCTARSIG=freefont-sfd-$(DATE).tar.gz.sig
SIGS=$(ZIPSIG) $(TARSIG) $(SRCTARSIG)

all: ttf otf woff

ttf: 
	@ ( cd sfd; $(MAKE) ttf )

otf: 
	@ ( cd sfd; $(MAKE) otf )

woff: 
	@ ( cd sfd; $(MAKE) woff )


package: ttftar otfzip otftar woffzip wofftar srctar

ttfzip: ttf
	rm -rf $(TMPDIR) $(TTFZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.ttf $(TMPDIR)
	cp -a notes/usage.txt $(TMPDIR)/USAGE
	zip -r $(TTFZIPFILE) $(RELEASE)/

otfzip: otf
	rm -rf $(TMPDIR) $(OTFZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.otf $(TMPDIR)
	cp -a notes/usage.txt $(TMPDIR)/USAGE
	zip -r $(OTFZIPFILE) $(RELEASE)/

woffzip: woff
	rm -rf $(TMPDIR) $(WOFFZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) notes/webfont_guidelines.txt sfd/*.woff $(TMPDIR)
	cp -a notes/usage.txt $(TMPDIR)/USAGE
	zip -r $(WOFFZIPFILE) $(RELEASE)/

ttftar: ttf
	rm -rf $(TMPDIR) $(TTFTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.ttf $(TMPDIR)
	cp -a notes/usage.txt $(TMPDIR)/USAGE
	tar czvf $(TTFTARFILE) $(RELEASE)/

otftar: otf
	rm -rf $(TMPDIR) $(OTFTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.otf $(TMPDIR)
	cp -a notes/usage.txt $(TMPDIR)/USAGE
	tar czvf $(OTFTARFILE) $(RELEASE)/

wofftar: woff
	rm -rf $(TMPDIR) $(WOFFTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) notes/webfont_guidelines.txt sfd/*.woff $(TMPDIR)
	cp -a notes/usage.txt $(TMPDIR)/USAGE
	tar czvf $(WOFFTARFILE) $(RELEASE)/

srctar:
	rm -rf $(TMPDIR) $(SRCTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.sfd $(TMPDIR)
	cp -ra $(ADMIN) notes $(TMPDIR)
	tar czvf $(SRCTARFILE) $(RELEASE)/

tests:
	( cd sfd; $(MAKE) tests )

clean:
	rm -rf $(TMPDIR) 
	rm -f $(TTFZIPFILE) $(TTFTARFILE) $(OTFTARFILE) $(WOFFZIPFILE) $(WOFFTARFILE) $(SRCTARFILE) $(SIGS) 
	( cd sfd; $(MAKE) clean )

distclean:
	rm -rf $(TMPDIR) 
	rm -f $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(SIGS)
	( cd sfd; $(MAKE) distclean )
