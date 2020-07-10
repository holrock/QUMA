#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: showAllBifFig4.cgi                                             *
#_* cgi for creating methylation pattern figure 4                             *
#_* (scaled but not acuurately black/white circle figure)                     *
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
my (%que  );
my ($file );
my ($fh   );
my (@gen  );
my ($line );
my ($proj );
my ($seq  );
my ($len  );
my ($cpgn );
my (@cpg  );
my ($que  );
my ($y    );
my ($posdi);
my ($min  );
my ($max  );
my ($mlen );
my ($width);
my ($heigh);
my ($gd   );
my ($font );
my ($white);
my ($black);
my ($ord  );
my ($x    );
my ($meth );
my ($cy   );
my ($i    );
my ($m    );
my (%num  );
my ($ratio);
my ($y1   );
my ($j    );
my (@ret  );
my ($pos  );
my ($fig  );
my ($size );
my ($name );
local ($_ );

$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;
parCheck ($data);
ipCheck ($data);
$data->{pos}
    or errorAndExit ('No data to show', 'No data to show',
		     "No data to show : $data->{pos}");
$data->{pos} =~ /^\d+(,\d+)*$/
    or errorAndExit ('Invalid access', 'Invalid access',
		     "Invalid POS value : $data->{pos}");

if ($data->{down} && $data->{format} && $data->{format} eq 'SVG') {
    use GD::SVG;

} elsif ($data->{down} && $data->{format} && $data->{format} eq 'SVGZ') {
    use GD::SVG;
    use Compress::Zlib;

} else {
    use GD;
}

$data->{eachh} = EACHH4
    unless (exists $data->{eachh}  &&
	    $data->{eachh} =~ /^\d+$/ && $data->{eachh} > 0);
$data->{diame} = DIAME4
    unless (exists $data->{diame}  &&
	    $data->{diame} =~ /^\d+$/ && $data->{diame} > 0);
$data->{line}  = LINEW4
    unless (exists $data->{line}   &&
	    $data->{line}  =~ /^\d+$/ && $data->{line}  > 0);
$data->{center} = CLINEW2
    unless (exists $data->{center} &&
	    $data->{center}  =~ /^\d+$/ && $data->{center}  > 0);
$data->{bscale} = BSCALE
    unless (exists $data->{bscale} &&
	    $data->{bscale} =~ /^\d+$/ && $data->{bscale} > 0);
$data->{spos4}  = SPOS
    unless (exists $data->{spos4}  && $data->{spos4} =~ /^-?\d+$/);

$data->{line}  = int(($data->{diame} + 1)/2)
    if ($data->{line} > int(($data->{diame}+1)/2));

@ord = split ',', $data->{pos};
map {$que{$_} = ''} @ord;

$file = DATADIR . $data->{id};
open $fh, $file
    or errorAndExit ('File access error!', 'File access error!',
		     "File access error : $! : $file");

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
    or errorAndExit ('No CpG data to show',
		     'No CpG data to show',
		     "No CpG data to show : $data->{pos}");

while ($line = <$fh>) {

    chomp $line;

    $que = [split /\t/, $line];
    next unless (exists $que{$que->[0]});
    $que{$que->[0]} = $que;
}

close $fh;

$y = 0;

if ($data->{showcpg4}) {

    $posdi = $data->{eachh} / POSRATIO;

    if ($data->{revpos4}) {
         $min = $len - $cpg[@cpg-1] - 1 + $data->{spos4};
         $max = $len - $cpg[0]      - 1 + $data->{spos4};
    } else {
         $min = $cpg[0]      + $data->{spos4};
         $max = $cpg[@cpg-1] + $data->{spos4};
    }
    $mlen = length (abs($min)) > length (abs($max)) ?
	length (abs($min)) : length (abs($max));
    $mlen++ if ($min < 0);

    if ($data->{pospos4}) {
        $y  = int ($posdi + $data->{diame} * FRATIO/2 * $mlen),
    }
}

$y += int (3*$data->{eachh}/4)
    if ($data->{showno4} && ! $data->{cpgno4});

$width  = $cpgn * $data->{diame} +
    ($len - 2*$cpgn) * $data->{bscale} + FIGMRG2 * 2;
$heigh  = $data->{eachh} * @ord;
$heigh  = $data->{eachh} if ($data->{circle4});

$heigh += int ($posdi + $data->{diame} * FRATIO/2 * $mlen + 1)
    if ($data->{showcpg4});
$heigh += int (3*$data->{eachh}/4) if ($data->{showno4});
$heigh++ if ($heigh - 2 * int($heigh/2));

if ($data->{down} && $data->{format} &&
    ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
    $gd = new GD::SVG::Image ($width, $heigh);
    $font = 'GD::SVG::Font';
} else {
    $gd = new GD::Image ($width, $heigh);
    $font = 'GD';
}

$white = $gd->colorAllocate (255,255,255);
$black = $gd->colorAllocate (  0,  0,  0);


foreach $ord (@ord) {

    last if ($data->{circle4});

    $x = FIGMRG2;
    $meth = $que{$ord}->[15] == 1 ? reverse $que{$ord}->[13] : $que{$ord}->[13];

    $cy = $y + int(($data->{eachh} + 1)/2) - int(($data->{center} - 1)/2);

    for ($i = 0; $i < $data->{center}; $i++) {
        $gd->line ($x,
                   $cy + $i,
                   $width - 1 - FIGMRG2, 
                   $cy + $i,
                   $black);
    }

    for ($i = 0; $i < $cpgn; $i++) {

	$m = chop $meth;
        $x = FIGMRG2 + $i*$data->{diame} +
	    ($cpg[$i] - 2*$i) * $data->{bscale} +
	    int(($data->{diame}-1)/2);

	if ($m eq '0') {

	    if ($data->{line} == 1) {
		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
			  $data->{diame}, $data->{diame}, 0, 360, $white);

		$gd->arc ($x, $y + int(($data->{eachh}+1)/2),
			  $data->{diame}, $data->{diame}, 0, 360, $black);
	    } else {
		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
				$data->{diame}, $data->{diame},
				0, 360, $black);

		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
				$data->{diame} - $data->{line} * 2,
				$data->{diame} - $data->{line} * 2,
				0, 360, $white);
	    }

	} elsif ($m eq '1') {

	    $gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
			    $data->{diame}, $data->{diame}, 0, 360, $black);

	}
    }
    $y += $data->{eachh};
}

if ($data->{circle4}) {

    $x = FIGMRG2;
    $cy = $y + int(($data->{eachh} + 1)/2) - int(($data->{center} - 1)/2);

    for ($i = 0; $i < $data->{center}; $i++) {
        $gd->line ($x,
                   $cy + $i,
                   $width - 1 - FIGMRG2, 
                   $cy + $i,
                   $black);
    }

    foreach $ord (@ord) {

        $meth = $que{$ord}->[15] == 1 ? reverse $que{$ord}->[13] : $que{$ord}->[13];

	for ($i = 0; $i < $cpgn; $i++) {

	    $m = chop $meth;

	    if ($m eq '0') {
		$num{$i}->{T}++;
	    } elsif ($m eq '1') {
		$num{$i}->{T}++;
		$num{$i}->{M}++;
	    }
	}
    }

    for ($i = 0; $i < $cpgn; $i++) {

        $x = FIGMRG2 + $i*$data->{diame}+
	    ($cpg[$i] - 2*$i) * $data->{bscale} +
	    int(($data->{diame}-1)/2);

	$num{$i}->{T} ||= 1;
	$num{$i}->{M} ||= 0;
	$ratio = int(360 * $num{$i}->{M}/$num{$i}->{T});

	if ($ratio == 360) {
	    $gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
			    $data->{diame}, $data->{diame}, 0, 360, $black);

	} else {

	    if ($data->{line} == 1) {

		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
				$data->{diame}, $data->{diame},
				0, 360, $black);

		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
				$data->{diame}, $data->{diame},
				270 + $ratio, 630, $white);

		$gd->arc ($x, $y + int(($data->{eachh}+1)/2),
			  $data->{diame}, $data->{diame}, 0, 360, $black);

	    } else {
		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
				$data->{diame}, $data->{diame},
				0, 360, $black);

		$gd->filledArc ($x, $y + int(($data->{eachh}+1)/2),
				$data->{diame} - $data->{line} * 2,
				$data->{diame} - $data->{line} * 2,
				270 + $ratio, 630, $white);
	    }
	}
    }

    $y += $data->{eachh};
}

if ($data->{showno4}) {
   if (! $data->{cpgno4}) {
       $y1 = int(3*$data->{eachh}/4) - int ($data->{eachh}/4);
       $y1 += int ($posdi + $data->{diame} * FRATIO/2 * $mlen)
            if ($data->{showcpg4} && $data->{pospos4});
   } else {
       $y += int(3*$data->{eachh}/4);
       $y1 = $y;
   }
}

for ($i = 0; $data->{showno4} && $i < $cpgn; $i++) {

    $j = $data->{revno4} ? $cpgn - $i : $i + 1;

    $x = FIGMRG2 + $i*$data->{diame} + ($cpg[$i] - 2*$i) * $data->{bscale}
         + int(($data->{diame}-1)/2);

    if ($data->{down} && $data->{format} &&
	($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
        $gd->string ($font->gdSmallFont,
                     $x - 5,
                     $y1 - 10, $j, $black);

    } else {
        @ret = $gd->stringFT($black, FONTPATH, int($data->{diame}/2), 0,
                             $x - int(length($j) * $data->{diame}/5),
                             $y1, $j);
    }
}

if ($data->{showcpg4}) {
   if ($data->{pospos4}) {
       $y  = int ($data->{diame} * FRATIO/2 * $mlen);
   } else {
       $y += int ($data->{diame} * FRATIO/2 * $mlen + $posdi);
   }
}

for ($i = 0; $data->{showcpg4} && $i < $cpgn; $i++) {

    $x = FIGMRG2 + $i*$data->{diame} + ($cpg[$i] - 2*$i) * $data->{bscale}
         + int(3 * $data->{diame}/4) - 1;

    $pos = $cpg[$i];
    $pos = $len - $pos - 1 if ($data->{revpos4});
    $pos += $data->{spos4};

    if ($min < 0) {
        $pos = "+$pos" if ($pos > 0);
        $pos = " $pos" if ($pos == 0);
    }

    if ($data->{down} && $data->{format} &&
	($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
        $gd->stringUp ($font->gdSmallFont,
                       $x - int ($data->{diame}/2),
                       $y - 10, $pos, $black);
    } else {
        @ret = $gd->stringFT($black, FONTPATH, int($data->{diame}/2), PI/2,
                             $x, $y, $pos);
    }
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
    $name .= "_bisulfite_fig4.";

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

if ($data->{down} && $data->{format} &&
    ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
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
