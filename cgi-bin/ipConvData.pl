#!/usr/bin/perl -s
#_*****************************************************************************
#_*                                                                           *
#_* File name: ipConvData.pl                                                  *
#_* perl script to make IP address conver file                                *
#_* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
#_* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
#_*                                                                           *
#_* 2011/01/29 First open source version                                      *
#_*                                                                           *
#_*****************************************************************************
#_*                                                                           *
#_* This program is free software: you can redistribute it and/or modify      *
#_* it under the terms of the GNU General Public License as published by      *
#_* the Free Software Foundation, either version 3 of the License, or         *
#_* (at your option) any later version.                                       *
#_*                                                                           *
#_* This program is distributed in the hope that it will be useful,           *
#_* but WITHOUT ANY WARRANTY; without even the implied warranty of            *
#_* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             *
#_* GNU General Public License for more details.                              *
#_*                                                                           *
#_* You should have received a copy of the GNU General Public License         *
#_* along with this program.  If not, see <http://www.gnu.org/licenses/>.     *
#_*                                                                           *
#_*****************************************************************************

use 5.8.0;
use strict;
use warnings;

our ($num);
our ($out);
my ($ip  );
my ($af  );
my ($be  );
my (@af  );
my (@be  );
my (%conv);
my ($host);
my ($f   );
my (@in  );
local ($_);
local ($1);
local ($2);
local ($3);
local ($a);
local ($b);

$num or die "usage :$0 -num=MinCountOfError [-out=pathOfIPConvFile.txt: output for IPConvFile.txt] httpd_error.log\n";

while (<>) {
    chomp;

    /\[error\] \[client (\d+\.\d+\.\d+\.\d+)\] Invalid ID or different IP : (\w*) : (\w*) at BFUtils\.pm/ or next;
    $ip = $1;
    $be = substr $2, -8;
    $af = $3;
    @be = $be =~ /.{2}/g;
    $be = join ".", map {hex} @be;
    @af = $af =~ /.{2}/g;
    $af = join ".", map {hex} @af;
    if (($be cmp $af) > 0) {
	$conv{"$be\t$af"}++;
    } else {
	$conv{"$af\t$be"}++;
    }
}

if ($out) {
    open $f, $out or die "$out:$!";

    while (<$f>) {
	chomp;
	@in = split /\t/;
	if (($in[0] cmp $in[1]) > 0) {
	    $conv{"$in[0]\t$in[1]"}+= $num;
	} else {
	    $conv{"$in[1]\t$in[0]"}+= $num;
	}
    }
    close $f;

    open $f, ">$out" or die "$out:$!";

}

foreach $ip (sort {$conv{$b} <=> $conv{$a}} grep {$conv{$_} >= $num} keys %conv) {
    ($be, $af) = split /\t/, $ip;
    $host = `host $be`;
    print "$be\t$af\t$conv{$ip}\t$host";
    print $f "$be\t$af\n" if ($be && $af && $out);
}

close $f if ($out);
###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################

