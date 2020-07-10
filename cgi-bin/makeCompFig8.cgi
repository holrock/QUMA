#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeCompFig8.cgi                                               *
#_* cgi for creating methylation status comparison graph 8                    *
#_* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
#_* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
#_*                                                                           *
#_* 2009/01/05 First open version                                             *
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
my ($posdi);
my ($mlen );
my ($width);
my ($heigh);
my ($gd   );
my ($font );
my ($white);
my ($black);
my ($yN   );
my ($y1   );
my ($y2   );
my ($yP   );
my ($x    );
my (@ret  );
my ($fig  );
my ($name );
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

    $meth{$pos[$i]}->{meth1}  ||= 0;
    $meth{$pos[$i]}->{meth2}  ||= 0;
    $meth{$pos[$i]}->{total1} ||= 1;
    $meth{$pos[$i]}->{total2} ||= 1;
    $meth{$pos[$i]}->{ratio1} = int(360 * $meth{$pos[$i]}->{meth1} / $meth{$pos[$i]}->{total1});
    $meth{$pos[$i]}->{ratio2} = int(360 * $meth{$pos[$i]}->{meth2} / $meth{$pos[$i]}->{total2});
}

$data->{len} =~ /^\d+$/
    or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$data->{len} = $data->{len}");

$posdi = EACHH4 / POSRATIO;
$mlen = length ($pos[@pos-1]);

$width  = @pos * DIAME4 +
    ($data->{len} - 2*@pos) * BSCALE + FIGMRG2 * 2 + 70;
$heigh  = EACHH4 * 2 +
    int ($posdi + DIAME4 * FRATIO/2 * $mlen + 1 + 3*EACHH4/4);
$heigh++ if ($heigh - 2 * int($heigh/2));

if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
    $gd = new GD::SVG::Image ($width, $heigh);
    $font = 'GD::SVG::Font';
} else {
    $gd = new GD::Image ($width, $heigh);
    $font = 'GD';
}

$white = $gd->colorAllocate (255,255,255);
$black = $gd->colorAllocate (  0,  0,  0);

$yN = int(EACHH4/2);
$y1 = int ((5*EACHH4+2)/4);
$y2 = int ((9*EACHH4+2)/4);
$yP  = int (11*EACHH4/4) + int (DIAME4 * FRATIO/2 * $mlen + $posdi);

$x = FIGMRG2 + 70;

for ($i = 0; $i < CLINEW2; $i++) {
    $gd->line ($x,
               $y1 - int((CLINEW2 - 1)/2) + $i,
               $width - 1 - FIGMRG2, 
               $y1 - int((CLINEW2 - 1)/2) + $i,
               $black);

    $gd->line ($x,
               $y2 - int((CLINEW2 - 1)/2) + $i,
               $width - 1 - FIGMRG2, 
               $y2 - int((CLINEW2 - 1)/2) + $i,
               $black);
}

if ($data->{down} && $data->{format} &&
    ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {

    $gd->string ($font->gdSmallFont,
		 3,
		 $y1 - 5, 'group1', $black);

    $gd->string ($font->gdSmallFont,
		 3,
		 $y2 - 5, 'group2', $black);

} else {

    @ret = $gd->stringFT($black, FONTPATH, int(DIAME4/2), 0,
			 3,
			 $y1 + 6, 'group1');

    @ret = $gd->stringFT($black, FONTPATH, int(DIAME4/2), 0,
			 3,
			 $y2 + 6, 'group2');
}

for ($i = 0; $i < @pos; $i++) {

    $x = FIGMRG2 + $i*DIAME4 + ($pos[$i] - 2*$i) * BSCALE +
	int((DIAME4-1)/2) + 70;

    if ($meth{$pos[$i]}->{ratio1} == 360) {
	$gd->filledArc ($x, $y1,
			DIAME4, DIAME4, 0, 360, $black);

    } else {

	if (LINEW4 == 1) {

	    $gd->filledArc ($x, $y1,
			    DIAME4, DIAME4,
			    0, 360, $black);

	    $gd->filledArc ($x, $y1,
			    DIAME4, DIAME4,
			    270 + $meth{$pos[$i]}->{ratio1}, 630, $white);

	    $gd->arc ($x, $y1,
		      DIAME4, DIAME4, 0, 360, $black);

	} else {
	    $gd->filledArc ($x, $y1,
			    DIAME4, DIAME4,
			    0, 360, $black);

	    $gd->filledArc ($x, $y1,
			    DIAME4 - LINEW4 * 2,
			    DIAME4 - LINEW4 * 2,
			    270 + $meth{$pos[$i]}->{ratio1}, 630, $white);
	}
    }


    if ($meth{$pos[$i]}->{ratio2} == 360) {
	$gd->filledArc ($x, $y2,
			DIAME4, DIAME4, 0, 360, $black);

    } else {

	if (LINEW4 == 1) {

	    $gd->filledArc ($x, $y2,
			    DIAME4, DIAME4,
			    0, 360, $black);

	    $gd->filledArc ($x, $y2,
			    DIAME4, DIAME4,
			    270 + $meth{$pos[$i]}->{ratio2}, 630, $white);

	    $gd->arc ($x, $y2,
		      DIAME4, DIAME4, 0, 360, $black);

	} else {
	    $gd->filledArc ($x, $y2,
			    DIAME4, DIAME4,
			    0, 360, $black);

	    $gd->filledArc ($x, $y2,
			    DIAME4 - LINEW4 * 2,
			    DIAME4 - LINEW4 * 2,
			    270 + $meth{$pos[$i]}->{ratio2}, 630, $white);
	}
    }

    if ($data->{down} && $data->{format} &&
	($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {

        $gd->string ($font->gdSmallFont,
                     $x - 5,
                     $yN - 10, $i + 1, $black);

        $gd->stringUp ($font->gdSmallFont,
                       $x - DIAME4 +  int(3 * DIAME4/4) - 1,
                       $yP - 10, $pos[$i], $black);

    } else {

        @ret = $gd->stringFT($black, FONTPATH, int(DIAME4/2), 0,
                             $x - int(length($i + 1) * DIAME4/5),
                             $yN, $i + 1);

        @ret = $gd->stringFT($black, FONTPATH, int(DIAME4/2), PI/2,
                             $x - int(DIAME4/2) +  int(3 * DIAME4/4) - 1,
			     $yP, $pos[$i]);
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
    $name .= "_$data->{proj}" if ($data->{proj});
    $name .= "_compared_CpG_status_graph8.";

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
