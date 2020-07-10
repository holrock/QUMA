#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: showAllBifFig.cgi                                              *
#_* cgi for creating methylation pattern figure 1                             *
#_* (simple black/white circle figure)                                        *
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
my ($min  );
my ($max  );
my ($mlen );
my ($heigh);
my ($gd   );
my ($font );
my ($white);
my ($black);
my ($ord  );
my ($meth );
my ($pos  );
my ($i    );
my ($x    );
my ($y    );
my ($posdi);
my ($m    );
my ($j    );
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

$data->{eachw} = EACHW
    unless (exists $data->{eachw} && $data->{eachw} =~ /^\d+$/ && $data->{eachw} > 0);
$data->{eachh} = EACHH
    unless (exists $data->{eachh} && $data->{eachh} =~ /^\d+$/ && $data->{eachh} > 0);
$data->{diame} = DIAME
    unless (exists $data->{diame} && $data->{diame} =~ /^\d+$/ && $data->{diame} > 0);
$data->{spos1}  = SPOS
    unless (exists $data->{spos1}  && $data->{spos1} =~ /^-?\d+$/);
$data->{line}  = LINEW
    unless (exists $data->{line}  && $data->{line}  =~ /^\d+$/ && $data->{line}  > 0);

$data->{line}  = int(($data->{diame} + 1)/2)
    if ($data->{line} > int(($data->{diame}+1)/2));

$data->{mistype} ||= MISTYPE;
$data->{mistype} =~ /^[123]$/ or $data->{mistype} = MISTYPE;

@ord = split ',', $data->{pos};
map {$que{$_} = ''} @ord;

$file = DATADIR . $data->{id};
open $fh, $file
    or errorAndExit ('File access error!', 'File access error!', "File access error : $! : $file");

chomp ($line = <$fh>);
@gen = split /\t/, $line;

shift @gen;
$proj  = shift @gen; # project
shift @gen; # group1
shift @gen; # group2
shift @gen; # convdir
$seq = shift @gen;
$len = length $seq;
$cpgn = shift @gen;
@cpg = map {$_} @gen;

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

$y = 0;

if ($data->{showcpg1}) {

    $posdi = $data->{eachh} / POSRATIO;

    if ($data->{revpos1}) {
         $min = $len - $cpg[@cpg-1] - 1 + $data->{spos1};
         $max = $len - $cpg[0]      - 1 + $data->{spos1};
    } else {
         $min = $cpg[0]      + $data->{spos1};
         $max = $cpg[@cpg-1] + $data->{spos1};
    }
    $mlen = length (abs($min)) > length (abs($max)) ? length (abs($min)) : length (abs($max));
    $mlen++ if ($min < 0);

    if ($data->{pospos1}) {
        $y  = int ($posdi + $data->{diame} * FRATIO/2 * $mlen),
    }
}

$y += int (3*$data->{eachh}/4)
    if ($data->{showno1} && ! $data->{cpgno1});

$heigh = $data->{eachh} * @ord;
$heigh += int ($posdi + $data->{diame} * FRATIO/2 * $mlen + 1),
    if ($data->{showcpg1});
$heigh += int (3*$data->{eachh}/4) if ($data->{showno1});
$heigh++ if ($heigh - 2 * int($heigh/2));

if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
    $gd = new GD::SVG::Image ($data->{eachw} * $cpgn, $heigh);
    $font = 'GD::SVG::Font';
} else {
    $gd = new GD::Image ($data->{eachw} * $cpgn, $heigh);
    $font = 'GD';
}

$white = $gd->colorAllocate (255,255,255);
$black = $gd->colorAllocate (  0,  0,  0);

foreach $ord (@ord) {

    $meth = $que{$ord}->[15] == 1 ? reverse $que{$ord}->[13] : $que{$ord}->[13];

    $x = 0;

    for ($i = 0; $i < $cpgn; $i++) {

	$m = chop $meth;

	if ($m eq '0') {

	    if ($data->{line} == 1) {
		$gd->filledArc ($x + int(($data->{eachw}+1)/2), $y + int(($data->{eachh}+1)/2),
			  $data->{diame}, $data->{diame}, 0, 360, $white);

		$gd->arc ($x + int(($data->{eachw}+1)/2), $y + int(($data->{eachh}+1)/2),
			  $data->{diame}, $data->{diame}, 0, 360, $black);
	    } else {
		$gd->filledArc ($x + int(($data->{eachw}+1)/2), $y + int(($data->{eachh}+1)/2),
				$data->{diame}, $data->{diame}, 0, 360, $black);

		$gd->filledArc ($x + int(($data->{eachw}+1)/2), $y + int(($data->{eachh}+1)/2),
				$data->{diame} - $data->{line} * 2, $data->{diame} - $data->{line} * 2, 0, 360, $white);
	    }

	} elsif ($m eq '1') {

	    $gd->filledArc ($x + int(($data->{eachw}+1)/2), $y + int(($data->{eachh}+1)/2),
			    $data->{diame}, $data->{diame}, 0, 360, $black);

	} elsif ($data->{mistype} == 1) {

	    $num = int ($data->{line} * sqrt 2);
	    $x1 = $x + int($data->{eachw}/2 - $data->{diame}/(2*sqrt 2));
	    $x2 = $x + int($data->{eachw}/2 + $data->{diame}/(2*sqrt 2));
	    $y1 = $y + int($data->{eachh}/2 - $data->{diame}/(2*sqrt 2));
	    $y2 = $y + int($data->{eachh}/2 + $data->{diame}/(2*sqrt 2));

	    for ($j = 0; $j < $num; $j++) {
		if ($j % 2) {
		    if (($j + 1) % 4) { # j = 1 + 4n
			$gd->line ($x1 - ($j - 1) / 4,
				   $y1 + ($j + 3) / 4,
				   $x2 - ($j - 1) / 4,
				   $y2 + ($j + 3) / 4,
				   $black);
			$gd->line ($x1 - ($j - 1) / 4, 
				   $y2 - ($j + 3) / 4,
				   $x2 - ($j - 1) / 4,
				   $y1 - ($j + 3) / 4,
				   $black);
		    } else {            # j = 3 + 4n
			$gd->line ($x1 + ($j + 1) / 4,
				   $y1 - ($j + 1) / 4,
				   $x2 + ($j + 1) / 4,
				   $y2 - ($j + 1) / 4,
				   $black);

			$gd->line ($x1 + ($j + 1) / 4, 
				   $y2 + ($j + 1) / 4,
				   $x2 + ($j + 1) / 4,
				   $y1 + ($j + 1) / 4,
				   $black);
		    }
		} else {
		    if ($j % 4) {       # j = 2 + 4n
			$gd->line ($x1 + ($j + 2) / 4,
				   $y1 - ($j - 2) / 4,
				   $x2 + ($j + 2) / 4,
				   $y2 - ($j - 2) / 4,
				   $black);
			$gd->line ($x1 + ($j + 2) / 4, 
				   $y2 + ($j - 2) / 4,
				   $x2 + ($j + 2) / 4,
				   $y1 + ($j - 2) / 4,
				   $black);
		    }  else {           # j = 4n
			$gd->line ($x1 -  $j      / 4,
				   $y1 +  $j      / 4,
				   $x2 -  $j      / 4,
				   $y2 +  $j      / 4,
				   $black);
			$gd->line ($x1 -  $j      / 4, 
				   $y2 -  $j      / 4,
				   $x2 -  $j      / 4,
				   $y1 -  $j      / 4,
				   $black);
		    }
		}
	    }
	} elsif ($data->{mistype} == 2) {

            if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
                $gd->string ($font->gdLargeFont,
                             $x + int(($data->{eachw}+1)/2) - 5,
                             $y + int(($data->{eachh}+1)/2) - 5,
                             $m, $black);

            } else {
                @ret = $gd->stringFT($black, FONTPATH, $data->{diame}, 0,
                                     $x + int ($data->{eachw}/2 - $data->{diame}*1/3),
                                     $y + int ($data->{eachh}/2 + $data->{diame}/2),
                                     $m);
            }
	}
	$x += $data->{eachw};
    }
    $y += $data->{eachh};
}

if ($data->{showno1}) {
   if (! $data->{cpgno1}) {
       $y1 = int(3*$data->{eachh}/4) - int ($data->{eachh}/4);
       $y1 += int ($posdi + $data->{diame} * FRATIO/2 * $mlen)
            if ($data->{showcpg1} && $data->{pospos1});
   } else {
       $y += int(3*$data->{eachh}/4);
       $y1 = $y;
   }
}

$x = int($data->{eachw}/2);

for ($i = 0; $data->{showno1} && $i < $cpgn; $i++, $x+= $data->{eachw}) {

    $j = $data->{revno1} ? $cpgn - $i : $i + 1;

    if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {

        $gd->string ($font->gdSmallFont,
                     $x - 5,
                     $y1 - 10, $j, $black);

    } else {
        @ret = $gd->stringFT($black, FONTPATH, int($data->{diame}/2), 0,
                             $x - int(length($j) * $data->{diame}/5),
                             $y1, $j);
    }
}

if ($data->{showcpg1}) {
   if ($data->{pospos1}) {
       $y  = int ($data->{diame} * FRATIO/2 * $mlen);
   } else {
       $y += int ($data->{diame} * FRATIO/2 * $mlen + $posdi);
   }
}

for ($i = $x = 0; $data->{showcpg1} && $i < $cpgn; $i++, $x+= $data->{eachw}) {

    $pos = $cpg[$i];
    $pos = $len - $pos - 1 if ($data->{revpos1});
    $pos += $data->{spos1};

    if ($min < 0) {
        $pos = "+$pos" if ($pos > 0);
        $pos = " $pos" if ($pos == 0);
    }

    if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
        $gd->stringUp ($font->gdSmallFont,
                       $x + int ($data->{eachw}/2 - 5),
                       $y - 10, $pos, $black);
    } else {
        @ret = $gd->stringFT($black, FONTPATH, int($data->{diame}/2), PI/2,
                             $x + int ($data->{eachw}/2 + $data->{diame}/4),
                             $y, $pos);
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
    $name .= "_bisulfite_fig.";

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
