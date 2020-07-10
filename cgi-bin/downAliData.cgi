#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: downAlignData.cgi                                              *
#_* cgi for downloading alignment data                                        *
#_* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
#_* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
#_*                                                                           *
#_* 2008/02/20 First open source version                                      *
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

use 5.6.0;
use strict;
use warnings;

use FindBin;
use lib $FindBin::Bin;
use CGI::Lite;
use BFSetting;
use BFUtils;


use constant BODY    => q{========================================================================
                     Alignment results No.%3d
========================================================================
--------------------------
Summary of information
--------------------------
%sBisulfite sequence name                    %s
Conversion                                 %s => %s conversion
(conversion of %s strand of the genomic sequence)
Length of bisulfite sequence               %d
Length of target genome sequence           %d
Aligned region of bisulfite sequence       %d - %d
Alignment direction                        %s
Number of CpGs                             %d
Number of methylated CpGs                  %d
Percent methylated                         %.1f %%
Number of unconverted CpHs (CpA/CpT/CpC)   %d
Number of CpHs (CpA/CpT/CpC)               %d
Percent converted CpHs (CpA/CpT/CpC)       %.1f %%
Number of mismatches (include gaps)        %d
Number of gaps                             %d
Alignment length                           %d
Percent identity                           %.1f %%
Methylation pattern                        %s
(U: unmethylated, M: methylated, A,C,G,T,N: mismatch,%s -: gap)

--------------------------
Target genome sequence
--------------------------
%s
--------------------------
Bisulfite sequence
--------------------------
%s
--------------------------
Alignment
--------------------------
'*' : Methylated CpG
'#' : Unmethylated CpG%s
'!' : Unconverted CpH
':' : Converted CpH
'|' : Match
' ' : Mismatch
--------------------------
%s
};

use constant GROUP => q{
Bisulfite sequence group                   %d};

my ($lc     );
my ($cgi    );
my ($data   );
my ($file   );
my ($fh     );
my ($line   );
my (@gen    );
my ($proj   );
my ($pro    );
my ($grp1   );
my ($grp2   );
my ($grp    );
my (@data   );
my ($gseq   );
my ($glen   );
my ($que    );
my ($cpgn   );
my (%cpg    );
my ($cpgh   );
my ($qseq   );
my ($qlen   );
my ($gAli   );
my ($qAli   );
my ($dir    );
my ($gdir   );
my ($len    );
my ($start  );
my ($g      );
my ($stop   );
my ($qstart );
my ($qstop  );
my ($i      );
my ($j      );
my ($k      );
my ($l      );
my ($q      );
my ($nextb  );
my ($prevb  );
my ($m      );
my ($gout   );
my ($ali    );
my ($qout   );
my ($output );
my ($bbase  );
my ($abase  );
my ($cpg    );
my ($cph    );
my ($meth   );
my ($out    );
my ($name   );
my ($cchk   );
my ($help   );
local ($!   );
local ($_   );
local ($1   );

$lc = LINE;
$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;
ipCheck ($data);

if (exists $data->{pos}) {
    $data->{pos} =~ /^\d+$/
	or errorAndExit ('Invalid access',
			 'Invalid access',
			 "Invalid POS value : $data->{pos}");
}

$data->{cpgcheck} = 0
    unless (exists $data->{cpgcheck} && $data->{cpgcheck} eq 'on');

$file = DATADIR . $data->{id};
open $fh, $file
    or errorAndExit ("Server Error!",
		     "Server Error!",
		     "open file error : $! : $file");

chomp ($line = <$fh>);
@gen = split /\t/, $line;
while ($line = <$fh>) {
    chomp $line;
    push @data, [split /\t/, $line];
}
close $fh;

shift @gen;
$proj = shift @gen;
$proj ||= '';
$proj =~ s/"//g;
$pro  = '';
$pro  = qq{Project name                               $proj\n} if ($proj);
$grp1 = shift @gen;
$grp1 ||= '';
$grp1 =~ s/"//g;
$grp2 = shift @gen;
$grp2 ||= '';
$grp2 =~ s/"//g;
shift @gen; # convdir
$gseq = shift @gen;
$glen = length $gseq;
$gseq =~ s/(\w{1,$lc})/$1\n/g;
$gseq = ">genome sequence\n$gseq";
$cpgn = shift @gen;
%cpg  = map {$_ => 1} @gen;

$cchk = $data->{cpgcheck} ?  ' +: not CpG site,' : '';
$help = $data->{cpgcheck} ?  "\n'+' : Not CpG site at this bisulfite sequence" : '';

foreach $que (sort {$a->[16] && $b->[16] ? $a->[17] <=> $b->[17] : 0} sort {$a->[1] cmp $b->[1]} @data) {

    next if (exists $data->{pos} && $que->[0] != $data->{pos});

    $qseq = $que->[2];
    $qlen = length $qseq;
    $qseq =~ s/(\w{1,$lc})/$1\n/g;
    $qseq = ">$que->[1]\n$qseq";
    $qAli = $que->[3];
    $gAli = $que->[4];
    $dir  = $que->[14];
    $gdir = $que->[15];

    $len  = length $qAli;

    for ($start = 0; $start < $len; $start++) {
	$g = substr $gAli, $start, 1;
	last unless ($g eq '-');
    }

    for ($stop = $len - 1; $stop >= 0; $stop--) {
	$g = substr $gAli, $stop, 1;
	last unless ($g eq '-');
    }

    if ($dir * $gdir == 1) {
	$qstart = $start;
	$qstop  = $qlen - $len + $stop ;

    } else {
	$qstart = $len  - $stop - 1;
	$qstop  = $qlen - $start - 1;
    }

    $output = '';

    if ($gdir == 1) {
        ($bbase, $abase) = ('C', 'T');
    } else {
        ($bbase, $abase) = ('G', 'A');
    }

    for ($j = $k = $l = 0, $prevb = '', $i = $start; $i <= $stop; $i++) {

        $nextb = '';
	$j = $i - $start + 1;
	$g = substr $gAli, $i, 1;
	$q = substr $qAli, $i, 1;
	$k++ unless ($g eq '-');
	$l++ unless ($q eq '-');

	if ($j % 60 == 1) {
	    $k++ if ($g eq '-');
	    $l++ if ($q eq '-');
	    $gout = 'Genome'   .' 'x(3 + 6 - length($k))."$k  ";
	    $ali  =             ' 'x(9 + 6 + 2);
	    $qout = 'Bisulfite'.' 'x(0 + 6 - length($l))."$l  ";
	    $k-- if ($g eq '-');
	    $l-- if ($q eq '-');
	}

	$gout .= $g;
	$qout .= $q;

	if ($g eq $bbase) {
	    $cpg = 0;

	    if ($gdir == 1 && $cpg{$k-1}) {
	        for ($m = $i+1; $m <= $stop; $m++) {
		    $nextb = substr $qAli, $m, 1;
		    last unless ($nextb eq '-');
	        }
		$cpg = 1;
            } elsif ($gdir != 1 && $cpg{$k-2}) {
		$cpg = 1;
	    }

	    if ($q eq $bbase) {
		if ($cpg) {
		    if (!$data->{cpgcheck} ||
		        $gdir == 1 && $nextb && $nextb eq 'G' ||
		        $gdir != 1 && $prevb && $prevb eq 'C') {
		        $ali .= '*';
		    } else {
		        $ali .= '+';
		    }
		} else {
		    $ali .= '!';
		}
	    } elsif ($q eq $abase) {
		if ($cpg) {
		    if (!$data->{cpgcheck} ||
		        $gdir == 1 && $nextb && $nextb eq 'G' ||
		        $gdir != 1 && $prevb && $prevb eq 'C') {
		        $ali .= '#';
                    } else {
		        $ali .= '+';
		    }
		} else {
		    $ali .= ':';
		}
	    } else {
		$ali .= ' ';
	    }
	} elsif ($g eq $q) {
	    $ali .= '|';
	} else {
	    $ali .= ' ';
	}

	if ($j % 60 == 0) {
	    $gout .= "\n";
	    $ali  .= "\n";
	    $qout .= "\n";

	    $output .= $gout . $ali . $qout . "\n";
	    $gout = $ali = $qout = '';
	}
        $prevb = $q unless ($q eq '-');
    }

    if ($j % 60 > 1) {
	$gout .= "\n";
	$ali  .= "\n";
	$qout .= "\n";
	$output .= $gout . $ali . $qout;
	$gout = $ali = $qout = '';
    }

    $dir  = $dir * $gdir == 1 ? 'forward' : 'reverse';
    $gdir = $gdir == 1 ? 'forward' : 'reverse';
    $cph  = $que->[10] + $que->[11];
    $cpg  = $que->[13] =~ y/01//;
    $meth = $que->[13];
    $meth =~ y/MRWSYKVHDB/mrwsykvhdb/;
    $meth =~ y/01/UM/;
    $cpgh = $cpg ? 100 * $que->[9]/$cpg : 0;
    $name  = $que->[1];
    $name .= sprintf GROUP, $que->[17] if ($que->[16]);

    $grp = '';
    if ($que->[16]) {
        if ($que->[17] == 1) {
	    $grp = $grp1 if ($grp1);
        } else {
	    $grp = $grp2 if ($grp2);
        }
    } elsif ($grp1) {
        $grp = $grp1;
    }
    $grp = qq{Sequence gorup name                        $grp\n} if ($grp);
    $out .= sprintf (BODY, $que->[0], $pro . $grp, $name, $bbase, $abase, $gdir,
                     $qlen, $glen,
		     $qstart + 1, $qstop + 1, $dir, $cpg,
		     $que->[9], $cpgh, $que->[10], $cph, $que->[12],
		     $que->[6], $que->[8], $que->[5], $que->[7],
		     $meth, $cchk, $gseq, $qseq, $help, $output);
}

$out =~ s/\n/\r\n/g;
$len = length $out;
$name  = substr $data->{id}, 0, 12;
$name .= "_$proj" if ($proj);
if (exists $data->{pos}) {
    $name .= sprintf "_alignment_data_%03d.txt", $data->{pos};
} else {
    $name .= "_all_alignment_data.txt";
}

print qq{Content-Disposition: attachment; filename="$name"
Content-Length: $len
Content-Type: text/plain
Status: 200 OK

$out};

###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
