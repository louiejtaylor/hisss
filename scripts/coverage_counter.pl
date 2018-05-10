#!/usr/local/bin/perl

use strict;
use warnings;

my %Contigs2Percent;
while(my $line = <STDIN>) {
    chomp $line;
    if ($line !~ /^genome/) {
	my ($contig, $nucl_covered, $count, $length, $coverage)= split(/\t/, $line);
	if (!exists $Contigs2Percent{$contig}) {
	    $Contigs2Percent{$contig} = "1"; 
	}
	if ($nucl_covered == 0) {
	    $Contigs2Percent{$contig} = 1 - $coverage
	}
    }
}

while ( my ($key, $value) = each(%Contigs2Percent) ) {
    print "$key\t$value\n";
}


