#!/usr/bin/perl
# Meant to convert a CVS log dump into something like a ChangeLog.
#
# Code is very ad-hoc, largely because both the CVS log and ChangeLog
# formats are not perfectly clear or fixed themselves, and because
# they were neither designed for intput.
#
# Note:
#       attempts to collect single commits of different files into one entry
# 	strips paths off of file names
# See http://en.wikipedia.org/wiki/Changelog
use strict;

package RevisionEntry;

sub new
{
	my $type = shift;
	my $date = shift;
	my $author = shift;

	my $self = {
		FILES => [],
		DATE => $date,
		AUTHOR => $author,
		TEXT => []
	};
	return bless $self, $type
}

sub addText
{
	my $self = shift;
	my $text = shift;

	push @{$self->{TEXT}}, $text;
}
sub addFile
{
	my $self = shift;
	my $fileName = shift;

	$fileName =~ s/.*\///;
	$fileName =~ s/,v//;

	push @{$self->{FILES}}, $fileName;
}

1;


my %revEntries = ();

sub readRCSFileEntry
{
	my $fileName = shift;
	my $curRev = '';

	LINE: while( <> )
	{
		if( /^========+$/ )
		{
			return 0;
		}
		elsif( /^date: ([^;]+);.* author: ([^;]+);.* lines: [+-]\d* [+-]\d*;(?:\s*commitid: ([^;]+);)?/ )
		{
			# Older CVS entries don't have unique commitid.
			# So just go by date (although in one commit, different
			# files have slightly different times).
			if( $3 )
			{
				$curRev = $3;
			}
			else
			{
				$curRev = $1;
			}
			if( exists $revEntries{$curRev} )
			{
				$revEntries{$curRev}->addFile( $fileName );
				# skip to end of the revision entry
				while( <> )
				{
					$curRev = '';
					next LINE if( /^---------+$/
						|| /^========+$/ );
				}
				last LINE;
			}
			else
			{
				my $re = RevisionEntry->new( $1, $2 );
				$re->addFile( $fileName );
				$revEntries{$curRev} = $re;
			}
		}
		elsif( /^---------+$/ )
		{
			$curRev = '';
		}
		elsif( $curRev )
		{
			$revEntries{$curRev}->addText( $_ );
		}
	}
	return 1;
}

RCSFILE: while( <> )
{
	if( /^RCS file: (.*)$/ )
	{
		last RCSFILE if readRCSFileEntry( $1 );
	}
}

# sort function comparison subroutine
sub by_reverse_date { $b->{DATE} cmp $a->{DATE}; }

sub ouput_changelog()
{
	my $lastDate = '';
	foreach my $v (sort by_reverse_date values( %revEntries ) )
	{
		my $date = $v->{DATE};
		$date =~ /([\d\-]+)/;
		if( $1 ne $lastDate )
		{
			print $1 . ' ' . $v->{AUTHOR} . "\n";
			$lastDate = $1;
		}
		print "\t* ";
		my $delim = '';
		foreach my $f (@{$v->{FILES}})
		{
			print "$delim$f";
			$delim = ', ';
		}
		print ":\n\n";
		foreach my $f (@{$v->{TEXT}})
		{
			print "\t$f";
		}
		print "\n";
	}
}

ouput_changelog();
