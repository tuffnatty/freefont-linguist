# $Id: Makefile,v 1.7 2008-03-23 18:11:32 Stevan_White Exp $

ADMIN=README AUTHORS CREDITS COPYING ChangeLog INSTALL
DATE=$(shell date +"%Y%m%d")
RELEASE=freefont-$(DATE)
BUILDDIR=$(PWD)
TMPDIR=$(BUILDDIR)/$(RELEASE)
ZIPFILE=freefont-ttf-$(DATE).zip
TARFILE=freefont-ttf-$(DATE).tar.gz
SRCTARFILE=freefont-sfd-$(DATE).tar.gz
ZIPSIG=freefont-ttf-$(DATE).zip.sig
TARSIG=freefont-ttf-$(DATE).tar.gz.sig
SRCTARSIG=freefont-sfd-$(DATE).tar.gz.sig
SIGS=$(ZIPSIG) $(TARSIG) $(SRCTARSIG)

all: ttf

ttf: 
	( cd sfd; $(MAKE) ttf )

package: tar srctar

zip: ttf
	rm -rf $(TMPDIR) $(ZIPFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.ttf $(TMPDIR)
	zip -r $(ZIPFILE) $(RELEASE)/

tar: ttf
	rm -rf $(TMPDIR) $(TARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.ttf $(TMPDIR)
	tar czf $(TARFILE) $(RELEASE)/

srctar:
	rm -rf $(TMPDIR) $(SRCTARFILE)
	mkdir $(TMPDIR)
	cp -a $(ADMIN) sfd/*.sfd $(TMPDIR)
	tar czf $(SRCTARFILE) $(RELEASE)/

clean:
	rm -rf $(TMPDIR) 
	rm -f $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(SIGS) 
	( cd sfd; $(MAKE) clean )

distclean:
	rm -rf $(TMPDIR) 
	rm -f $(ZIPFILE) $(TARFILE) $(SRCTARFILE) $(SIGS)
	( cd sfd; $(MAKE) distclean )
