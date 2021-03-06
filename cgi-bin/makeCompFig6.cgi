#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeCompFig6.cgi                                               *
#_* cgi for creating methylation status comparison graph 6                    *
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

my ($cgi  );
my ($data );
my (@pos  );
my (@val1 );
my (@val2 );
my ($i    );
my (%meth );
my ($gwid );
my ($width);
my ($hight);
my ($gd   );
my ($font );
my ($white);
my ($black);
my ($blue );
my ($x    );
my ($x1   );
my ($x2   );
my ($y1   );
my ($y2   );
my ($j    );
my ($name );
my ($fig  );
my ($size );
local ($_ );

$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;
parCheck ($data);
ipCheck ($data);

if ($data->{down} && $data->{format} && $data->{format} eq 'SVG') {
    use GD::SVG;

} elsif ($data->{down} && $data->{format} && $data->{format} eq 'SVGZ') {
    use GD::SVG;
    use Compress::Zlib;

} else {
    use GD;
}

$data->{proj} ||= '';
$data->{proj} =~ y/&;`'"|*?~<>^()[]{}$\\\n\r//d;
$data->{proj} =~ s/[^\w-]//g;

@pos  = split ',', $data->{pos};
@val1 = split ',', $data->{val1};
@val2 = split ',', $data->{val2};

@pos == @val1
    or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \@pos != \@val1 : " . @pos . " != " . @val1);
@pos == @val2
    or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \@pos != \@val2 : " . @pos . " != " . @val2);

for ($i = 0; $i < @pos; $i++) {
    $pos[$i] =~ /^\d+$/
	or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$pos[$i] = $pos[$i]");
    $meth{$pos[$i]} = {};
    ($meth{$pos[$i]}->{meth1}, $meth{$pos[$i]}->{total1}) = split '\|', $val1[$i];
    ($meth{$pos[$i]}->{meth2}, $meth{$pos[$i]}->{total2}) = split '\|', $val2[$i];
    $meth{$pos[$i]}->{meth1} =~ /^\d+$/
	or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$meth{$pos[$i]}->{meth1} = $meth{$pos[$i]}->{meth1}");
    $meth{$pos[$i]}->{total1} =~ /^\d+$/
	or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$meth{$pos[$i]}->{total1} = $meth{$pos[$i]}->{total1}");
    $meth{$pos[$i]}->{meth2} =~ /^\d+$/
	or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$meth{$pos[$i]}->{meth2} = $meth{$pos[$i]}->{meth2}");
    $meth{$pos[$i]}->{total2} =~ /^\d+$/
	or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$meth{$pos[$i]}->{total2} = $meth{$pos[$i]}->{total2}");

    $meth{$pos[$i]}->{total1} ||= 1;
    $meth{$pos[$i]}->{total2} ||= 1;
    $meth{$pos[$i]}->{ratio1} = $meth{$pos[$i]}->{meth1} / ($meth{$pos[$i]}->{total1});
    $meth{$pos[$i]}->{ratio2} = $meth{$pos[$i]}->{meth2} / ($meth{$pos[$i]}->{total2});
}

$data->{len} =~ /^\d+$/
    or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$data->{len} = $data->{len}");

$gwid  = ($data->{len} - @pos ) * 2 + @pos * GWIDTH;
$width = $gwid + MARGL2 + MARGR + GLEGW;
$hight = HIGHT;

if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
    $gd = new GD::SVG::Image ($width, $hight);
    $font = 'GD::SVG::Font';
} else {
    $gd = new GD::Image ($width, $hight);
    $font = 'GD';
}

$white = $gd->colorAllocate (255,255,255);
$black = $gd->colorAllocate (  0,  0,  0);
$blue  = $gd->colorAllocate (  0,  0,255);

$gd->rectangle (MARGL2 - 1, GMARGH,
		MARGL2 + $gwid,  HIGHT - GMARGB2,
		$black);

$gd->line (MARGL2,
	   int ((HIGHT - GMARGB2 + GMARGH) / 2),
	   MARGL2 + $gwid - 1,
	   int ((HIGHT - GMARGB2 + GMARGH) / 2),
	   $black);

$gd->string ($font->gdSmallFont,
	     LFMARG2, HIGHT - BMARG - FONTH2,
	     'CpG position', $black);
$gd->string ($font->gdSmallFont,
	     MARGL2 - LLABLEN - 1, GMARGH - FONTH2,
	     '100%', $black);
$gd->string ($font->gdSmallFont,
	     MARGL2 - LLABLEN - 1, int ((HIGHT - GMARGB2 + GMARGH) / 2) - FONTH2,
	     '  0%', $black);
$gd->string ($font->gdSmallFont,
	     MARGL2 - LLABLEN - 1, HIGHT - GMARGB2 - FONTH2,
	     '100%', $black);

$gd->string ($font->gdSmallFont,
	     LFMARG2,
	     int ((HIGHT - GMARGB2 +  GMARGH * 3) / 4) - FONTH2,
	     '    Methylated (%)', $black);
 
$gd->string ($font->gdSmallFont,
	     LFMARG2,
	     int ((HIGHT * 3 - GMARGB2 * 3 + GMARGH) / 4) - FONTH2,
	     '  Unmethylated (%)', $black);

$x1 = $width - GLEGW + 5;
$x  = $x1 + int (GWIDTH / 2 + 1);
$x2 = $x1 + GWIDTH;
$y1 = int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.1);
$y2 = int ((HIGHT - GMARGB2 + GMARGH) / 2 - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.4);

$gd->stringUp ($font->gdTinyFont,
	       $x1-3,$y2 - FONTH1,
	       'group1', $black);

$gd->stringUp ($font->gdTinyFont,
	       $x-2,$y2 - FONTH1,
	       'group2', $black);

$gd->line ($x, $y1, $x, $y2, $blue);

for ($j = $x1; $j <= $x-1; $j++) {
    $gd->line ($j, int ((HIGHT - GMARGB2 + GMARGH) / 2),
	       $j,
	       int ((HIGHT - GMARGB2 + GMARGH) / 2 - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.4),
	       $black);
}

$gd->line ($x1,  int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.4),
	   $x-1, int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.4),
	   $black);

$gd->line ($x1, int ((HIGHT - GMARGB2 + GMARGH) / 2),
	   $x1, int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.4),
	   $black);

for ($j = $x+1; $j <= $x2; $j++) {
    $gd->line ($j, int ((HIGHT - GMARGB2 + GMARGH) / 2),
	       $j,
	       int ((HIGHT - GMARGB2 + GMARGH) / 2 - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.1),
	       $black);
}

$gd->line ($x+1, int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.1),
	   $x2,  int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.1),
	   $black);

$gd->line ($x2, int ((HIGHT - GMARGB2 + GMARGH) / 2),
	   $x2, int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * 0.1),
	   $black);

for ($i = 0; $i < @pos; $i++) {

    $x = MARGL2 + ($pos[$i] - $i - 1) * 2 + GWIDTH * $i + int (GWIDTH / 2 + 1);
    $x1 = $x - int (GWIDTH / 2 + 1);
    $x2 = $x1 + GWIDTH;

    $gd->stringUp ($font->gdTinyFont,
		   $x1 + 1, HIGHT - 7,
		   $pos[$i], $black);

    if ($meth{$pos[$i]}->{ratio1} > $meth{$pos[$i]}->{ratio2}) {
	$y1 = int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio2});
	$y2 = int ((HIGHT - GMARGB2 + GMARGH) / 2 - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio1});
    } else {
	$y1 = int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio1});
	$y2 = int ((HIGHT - GMARGB2 + GMARGH) / 2 - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio2});
    } 

    $gd->line ($x, $y1, $x, $y2, $blue);

    for ($j = $x1; $j <= $x-1; $j++) {
	$gd->line ($j, int ((HIGHT - GMARGB2 + GMARGH) / 2),
		   $j,
		   int ((HIGHT - GMARGB2 + GMARGH) / 2 - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio1}),
		   $black);
    }

    $gd->line ($x1,  int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio1}),
	       $x-1, int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio1}),
	       $black);

    $gd->line ($x1, int ((HIGHT - GMARGB2 + GMARGH) / 2),
	       $x1, int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio1}),
	       $black);

    for ($j = $x+1; $j <= $x2; $j++) {
	$gd->line ($j, int ((HIGHT - GMARGB2 + GMARGH) / 2),
		   $j,
		   int ((HIGHT - GMARGB2 + GMARGH) / 2 - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio2}),
		   $black);
    }

    $gd->line ($x+1, int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio2}),
	       $x2,  int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio2}),
	       $black);

    $gd->line ($x2, int ((HIGHT - GMARGB2 + GMARGH) / 2),
	       $x2, int (HIGHT - GMARGB2  - (HIGHT - GMARGB2 - GMARGH) / 2 * $meth{$pos[$i]}->{ratio2}),
	       $black);
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
    $name .= "_$data->{proj}" if ($data->{proj});
    $name .= "_compared_CpG_status_graph6.";

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
