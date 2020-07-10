#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeCompFig2.cgi                                               *
#_* cgi for creating methylation status comparison graph 2                    *
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
my (@val1 );
my (@val2 );
my ($i    );
my (%meth );
my ($width);
my ($hight);
my ($gd   );
my ($font );
my ($white);
my ($black);
my ($green);
my ($magen);
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
$green = $gd->colorAllocate (  0,255,  0);
$magen = $gd->colorAllocate (255,  0,255);

$gd->line (MARGL,
	   HIGHT - BMARG,
	   MARGL + $data->{len} * 2 - 1,
	   HIGHT - BMARG,
	   $black);

$gd->rectangle (MARGL - 1, GMARGH,
		MARGL + $data->{len} * 2, HIGHT - GMARGB,
		$black);
$gd->string   ($font->gdTinyFont,
	       LFMARG, HIGHT - BMARG - FONTH1,
	       'CpG position', $black);
$gd->string   ($font->gdTinyFont,
	       MARGL - LLABLEN - 1, GMARGH - FONTH1,
	       '100%', $black);
$gd->string   ($font->gdTinyFont,
	       MARGL - LLABLEN - 1, HIGHT - GMARGB - FONTH1,
	       '  0%', $black);
$gd->string   ($font->gdTinyFont,
	       LFMARG, HIGHT - GMARGB - FONTH1 - 60,
	       'group1', $green);
$gd->string   ($font->gdTinyFont,
	       LFMARG, HIGHT - GMARGB - FONTH1 - 40,
	       'group2', $magen);
$gd->stringUp ($font->gdTinyFont,
	       MARGL - LLABLEN - LLABMRG - 1 + 20, HIGHT - GMARGB - FONTH1 - 10,
	       'Methylated (%)', $black);

for ($i = 0; $i < @pos; $i++) {

    $gd->line (MARGL + $pos[$i] * 2 - 2,
	       HIGHT - BMARG - HLINE,
	       MARGL + $pos[$i] * 2 - 2,
	       HIGHT - BMARG + HLINE,
	       $black);

    $gd->line (MARGL + $pos[$i] * 2 - 1,
	       HIGHT - BMARG - HLINE,
	       MARGL + $pos[$i] * 2 - 1,
	       HIGHT - BMARG + HLINE,
	       $black);

    $gd->line (MARGL + $pos[$i] * 2 - 2,
	       HIGHT - GMARGB,
	       MARGL + $pos[$i] * 2 - 2,
	       int (HIGHT - GMARGB - (HIGHT - GMARGB - GMARGH) * $meth{$pos[$i]}->{ratio1}),
	       $green);

    $gd->line (MARGL + $pos[$i] * 2 - 1,
	       HIGHT - GMARGB,
	       MARGL + $pos[$i] * 2 - 1,
	       int (HIGHT - GMARGB - (HIGHT - GMARGB - GMARGH) * $meth{$pos[$i]}->{ratio2}),
	       $magen);

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
    $name .= "_compared_CpG_status_graph2.";

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
