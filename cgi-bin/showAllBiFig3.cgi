#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: showAllBifFig3.cgi                                             *
#_* cgi for creating methylation pattern figure 3                             *
#_* (scaled black/white circle figure)                                        *
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

use CGI::Lite;
use BFSetting;
use BFUtils;

my ($cgi  );
my ($data );
my (@ord  );
my ($file );
my ($fh   );
my (@gen  );
my ($line );
my ($proj );
my ($que  );
my (%que  );
my ($seq  );
my ($len  );
my ($cpgn );
my (@cpg  );
my ($start);
my ($stop );
my ($width);
my ($heigh);
my ($gd   );
my ($white);
my ($black);
my ($ord  );
my ($meth );
my ($i    );
my ($j    );
my ($lwide);
my ($x    );
my ($y    );
my ($cy   );
my ($m    );
my ($num  );
my ($x1   );
my ($x2   );
my ($y1   );
my ($y2   );
my ($fig  );
my ($size );
my ($name );
my (@ret  );
local ($_ );

$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;
parCheck ($data);
ipCheck ($data);
$data->{pos}
    or errorAndExit ('No data to show', 'No data to show', "No data to show : $data->{pos}");
$data->{pos} =~ /^\d+(,\d+)*$/
    or errorAndExit ('Invalid access', 'Invalid access', "Invalid POS value : $data->{pos}");

if ($data->{down} && $data->{format} && $data->{format} eq 'SVG') {
    use GD::SVG;

} elsif ($data->{down} && $data->{format} && $data->{format} eq 'SVGZ') {
    use GD::SVG;
    use Compress::Zlib;

} else {
    use GD;
}

$data->{eachh} = EACHH4
    unless (exists $data->{eachh} && $data->{eachh} =~ /^\d+$/ && $data->{eachh} > 0);
$data->{diame} = DIAME4
    unless (exists $data->{diame} && $data->{diame} =~ /^\d+$/ && $data->{diame} > 0);
$data->{line}  = LINEW4
    unless (exists $data->{line}  && $data->{line}  =~ /^\d+$/ && $data->{line}  > 0);
$data->{center} = CLINEW2
    unless (exists $data->{center}  && $data->{center}  =~ /^\d+$/ && $data->{center}  > 0);
$data->{bscale} = BSCALE
    unless (exists $data->{bscale} && $data->{bscale} =~ /^\d+$/ && $data->{bscale} > 0);

$data->{line}  = int(($data->{diame} + 1)/2)
    if ($data->{line} > int(($data->{diame}+1)/2));

@ord = split ',', $data->{pos};
map {$que{$_} = ''} @ord;

$file = DATADIR . $data->{id};
open $fh, $file
    or errorAndExit ('File access error!', 'File access error!', "File access error : $! : $file");

chomp ($line = <$fh>);
@gen = split /\t/, $line;

shift @gen;
$proj = shift @gen; # project
shift @gen; # group1
shift @gen; # group2
shift @gen; # convdir
$seq  = shift @gen;
$len  = length $seq;
$cpgn = shift @gen;
@cpg  = map {$_} @gen;

$proj ||= '';
$proj =~ y/&;`'"|*?~<>^()[]{}$\\\n\r//d;
$proj =~ s/[^\w-]//g;

$cpgn
    or errorAndExit ('No CpG data to show', 'No CpG data to show', "No CpG data to show : $data->{pos}");

while ($line = <$fh>) {

    chomp $line;

    $que = [split /\t/, $line];
    next unless (exists $que{$que->[0]});
    $que{$que->[0]} = $que;
}

close $fh;

$start = $stop = 0;
$start = int(($data->{diame} + 1)/2) - 1 - $cpg[0] * $data->{bscale}
    if ($cpg[0] * $data->{bscale} < int(($data->{diame}+1)/2) - 1);

$stop = ($len - 2 - $cpg[$cpgn-1]) * $data->{bscale} + int(($data->{diame}+1)/2) - 1
    if (($len - 2 - $cpg[$cpgn-1]) * $data->{bscale} < int(($data->{diame}+1)/2) - 1);

$width  = $start + $len * $data->{bscale} + FIGMRG2 * 2 + $stop;
$heigh  = $data->{eachh} * @ord;
$heigh += $data->{eachh} if ($data->{showcpg});

if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
    $gd = new GD::SVG::Image ($width, $heigh);
} else {
    $gd = new GD::Image ($width, $heigh);
}

$white = $gd->colorAllocate (255,255,255);
$black = $gd->colorAllocate (  0,  0,  0);

$x = FIGMRG2 + $start;

$lwide = $data->{bscale};

if ($data->{showcpg}) {

    $cy = int(($data->{eachh} + 1)/2) - int(($data->{center} - 1)/2);
    $cy += $data->{eachh} * @ord unless ($data->{pospos3});

    for ($i = 0; $i < $data->{center}; $i++) {
        $gd->line ($x,
                   $cy + $i,
                   $width - 1 - FIGMRG2 - $stop, 
                   $cy + $i,
                   $black);
    }

    $cy = int(($data->{eachh} + 1)/2) - int(($data->{diame} - 1)/2);
    $cy += $data->{eachh} * @ord unless ($data->{pospos3});

    for ($i = 0; $i < @cpg; $i++) {
        $x = FIGMRG2 + $start + $cpg[$i] * $data->{bscale} - int(($lwide-1)/2);
        for ($j = 0; $j < $lwide; $j++) {
            $gd->line ($x + $j, $cy,
                       $x + $j, $cy + $data->{diame} - 1,
                       $black);
        }
    }
}

$y = 0;
$y = $data->{eachh} if ($data->{showcpg} && $data->{pospos3});

foreach $ord (@ord) {

    $x = FIGMRG2 + $start;
    $meth = $que{$ord}->[15] == 1 ? reverse $que{$ord}->[13] : $que{$ord}->[13];

    $cy = $y + int(($data->{eachh} + 1)/2) - int(($data->{center} - 1)/2);

    for ($i = 0; $i < $data->{center}; $i++) {
        $gd->line ($x,
                   $cy + $i,
                   $width - 1 - FIGMRG2 - $stop, 
                   $cy + $i,
                   $black);
    }

    for ($i = 0; $i < $cpgn; $i++) {

	$m = chop $meth;
        $x = FIGMRG2 + $start + $cpg[$i] * $data->{bscale};

	if ($m eq '0') {

	    if ($data->{line} == 1) {
		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
			  $data->{diame}, $data->{diame}, 0, 360, $white);

		$gd->arc ($x, $y + int(($data->{eachh}+1)/2),
			  $data->{diame}, $data->{diame}, 0, 360, $black);
	    } else {
		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
				$data->{diame}, $data->{diame}, 0, 360, $black);

		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
				$data->{diame} - $data->{line} * 2, $data->{diame} - $data->{line} * 2, 0, 360, $white);
	    }

	} elsif ($m eq '1') {

	    $gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
			    $data->{diame}, $data->{diame}, 0, 360, $black);

	}
    }
    $y += $data->{eachh};
}

if ($data->{down} && $data->{format} && $data->{format} eq 'SVG') {
    $fig = groupSVG ($gd->svg);

} elsif ($data->{down} && $data->{format} && $data->{format} eq 'SVGZ') {
    $fig = Compress::Zlib::memGzip (groupSVG ($gd->svg))

} else {
    $fig = $gd->png;
}

$size = length $fig;

if ($data->{down}) {
    $name = substr $data->{id}, 0, 12;
    $name .= "_$proj" if ($proj);
    $name .= "_bisulfite_fig3.";

    if ($data->{format} && $data->{format} eq 'SVG') {
        $name .= "svg";
    } elsif ($data->{format} && $data->{format} eq 'SVGZ') {
        $name .= "svgz";
    } else {
        $name .= "png";
    }

    print qq{Content-Disposition: attachment; filename="$name"\n};
    print qq{Content-Length: $size\n};    
}

if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
    print qq{Content-Type: image/svg+xml\n};
} else {
    print qq{Content-Type: image/png\n};
}

print qq{Status: 200 OK\n\n};
print $fig;

###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
