#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeCpGFig2.cgi                                                *
#_* cgi for creating methylation status graph 2                               *
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
my (@pos  );
my (@val  );
my ($i    );
my (%meth );
my ($width);
my ($hight);
my ($gd   );
my ($font );
my ($white);
my ($black);
my ($gray );
my ($mag  );
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

@pos = split ',', $data->{pos};
@val = split ',', $data->{val};

@pos == @val
    or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \@pos != \@val : " . @pos . " != " . @val);

for ($i = 0; $i < @pos; $i++) {
    $pos[$i] =~ /^\d+$/
	or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$pos[$i] = $pos[$i]");
    $meth{$pos[$i]} = {};
    ($meth{$pos[$i]}->{meth}, $meth{$pos[$i]}->{total}) = split '\|', $val[$i];
    $meth{$pos[$i]}->{meth} =~ /^\d+$/
	or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$meth{$pos[$i]}->{meth} = $meth{$pos[$i]}->{meth}");
    $meth{$pos[$i]}->{total} =~ /^\d+$/
	or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$meth{$pos[$i]}->{total} = $meth{$pos[$i]}->{total}");
    $meth{$pos[$i]}->{total} ||= 1;
    $meth{$pos[$i]}->{ratio} = $meth{$pos[$i]}->{meth} / ($meth{$pos[$i]}->{total});
}

$data->{len} =~ /^\d+$/
    or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$data->{len} = $data->{len}");

$width = $data->{len} * 2 + MARGL + MARGR;

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
$gray  = $gd->colorAllocate (128,128,128);
$mag   = $gd->colorAllocate (255,  0,255);

$gd->line (MARGL,
	   HIGHT - BMARG,
	   MARGL + $data->{len} * 2 - 1,
	   HIGHT - BMARG,
	   $black);

$gd->rectangle (MARGL - 1, GMARGH,
	   MARGL + $data->{len} * 2, HIGHT - GMARGB,
	   $black);

$gd->string   ($font->gdSmallFont,
	       LFMARG, HIGHT - BMARG - FONTH2,
	       'CpG position', $black);
$gd->string   ($font->gdSmallFont,
	       MARGL - LLABLEN - 1, GMARGH - FONTH2,
	       '100%', $black);
$gd->string   ($font->gdSmallFont,
	       MARGL - LLABLEN - 1, HIGHT - GMARGB - FONTH2,
	       '  0%', $black);
$gd->stringUp ($font->gdSmallFont,
	       MARGL - LLABLEN - LLABMRG - 1, HIGHT - GMARGB - FONTH2 - 3,
	       'Methylated (%)', $black);

for ($i = 0; $i < @pos; $i++) {

    $gd->line (MARGL + $pos[$i] * 2 - 1,
	       HIGHT - BMARG - HLINE,
	       MARGL + $pos[$i] * 2 - 1,
	       HIGHT - BMARG + HLINE,
	       $black);

    if ($meth{$pos[$i]}->{ratio}) {
	$gd->line (MARGL + $pos[$i] * 2 - 2,
		   HIGHT - GMARGB - 1,
		   MARGL + $pos[$i] * 2 - 2,
		   int (HIGHT - GMARGB - (HIGHT - GMARGB - GMARGH) * $meth{$pos[$i]}->{ratio}),
		   $gray);

	$gd->line (MARGL + $pos[$i] * 2 - 1,
		   HIGHT - GMARGB - 1,
		   MARGL + $pos[$i] * 2 - 1,
		   int (HIGHT - GMARGB - (HIGHT - GMARGB - GMARGH) * $meth{$pos[$i]}->{ratio}),
		   $gray);

	$gd->line (MARGL + $pos[$i] * 2,
		   HIGHT - GMARGB - 1,
		   MARGL + $pos[$i] * 2,
		   int (HIGHT - GMARGB - (HIGHT - GMARGB - GMARGH) * $meth{$pos[$i]}->{ratio}),
		   $gray);
    } else {
	$gd->line (MARGL + $pos[$i] * 2 - 2,
		   HIGHT - GMARGB,
		   MARGL + $pos[$i] * 2,
		   HIGHT - GMARGB,
		   $mag);
	$gd->line (MARGL + $pos[$i] * 2 - 2,
		   HIGHT - GMARGB - 1,
		   MARGL + $pos[$i] * 2,
		   HIGHT - GMARGB - 1,
		   $mag);
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
    $name .= "_CpG_status_graph2.";

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
