#!/usr/bin/perl
# $Id: LigatureList.pl,v 1.1 2002-03-05 19:19:43 peterlin Exp $
#
# Using the output of George Williams' showttf program, we produce a
# readable list of GSUB (Glyph Substitute) ligatures from an OpenType
# font.

if ($#ARGV >= 0) {
    $ttffile = $ARGV[0];
    open(SHOWTTF, "showttf $ttffile |");
} else {
    die "Usage: $0 ttffile\n";
}

while (<SHOWTTF>) {
    chomp;
    if (/^ Glyph /) {
	@fld = split (' ', $_, 9999);
	$unichar = sprintf("uni%s", substr($fld[3],2,4));
	$glyph[$fld[1]] = $unichar;
    }
    if (/Ligature glyph/) {
	print $_,"\n";
    }
}
