#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeCompFig7.cgi                                               *
#_* cgi for creating methylation status comparison graph 7                    *
#_* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
#_* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
#_*                                                                           *
#_* 2008/02/20 First open source version                                      *
#_* 2010/11/12 'fisherExactTest' updated                                      *
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
my ($gwid );
my ($ref  );
my ($pval );
my ($width);
my ($hight);
my ($gd   );
my ($font );
my ($white);
my ($black);
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

$ref = {};

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
    $meth{$pos[$i]}->{ratio1} = $meth{$pos[$i]}->{meth1} / $meth{$pos[$i]}->{total1};
    $meth{$pos[$i]}->{ratio2} = $meth{$pos[$i]}->{meth2} / $meth{$pos[$i]}->{total2};
    $pval = fisherExactTest ($ref,
                             $meth{$pos[$i]}->{meth1},($meth{$pos[$i]}->{total1}-$meth{$pos[$i]}->{meth1}),
			     $meth{$pos[$i]}->{meth2},($meth{$pos[$i]}->{total2}-$meth{$pos[$i]}->{meth2}));


    $meth{$pos[$i]}->{pval} = $pval <= 0.01 ? 2 :
	                      $pval <= 0.1  ? 1 :
			                      0 ;
}

$data->{len} =~ /^\d+$/
    or errorAndExit ('Parameter error!', 'Parameter error!', "Parameter error! : \$data->{len} = $data->{len}");

$gwid  = ($data->{len} - @pos ) * 2 + @pos * GWIDTH;
$width = $gwid + MARGL2 + GLEGW;
$hight = HIGHT2;

if ($data->{down} && $data->{format} && ($data->{format} eq 'SVG' || $data->{format} eq 'SVGZ')) {
    $gd = new GD::SVG::Image ($width, $hight);
    $font = 'GD::SVG::Font';
} else {
    $gd = new GD::Image ($width, $hight);
    $font = 'GD';
}

$white = $gd->colorAllocate (255,255,255);
$black = $gd->colorAllocate (  0,  0,  0);

my $mid;
my $bot = HIGHT2 - GMARGB2;
my $top = GMARGH;
my $qu1;  # int(($top + $mid)/2)
my $qu3;  # int(($bot + $mid)/2);

$mid = (HIGHT2 - GMARGB2 + GMARGH)/2;
$qu1 = (HIGHT2 - GMARGB + GMARGH*3)/4;
$qu3 = (HIGHT2*3 - GMARGB2*3 + GMARGH*3)/4;

$gd->rectangle (MARGL2-1,$top,MARGL2+$gwid,$bot,$black);
$gd->line (MARGL2,int($mid),MARGL2+$gwid-1,int($mid),$black);
$gd->line (MARGL2,int($qu1),MARGL2+$gwid-1,int($qu1),$black);
$gd->line (MARGL2,int($qu3),MARGL2+$gwid-1,int($qu3),$black);

$gd->string ($font->gdSmallFont,
	     LFMARG2, HIGHT2 - BMARG - FONTH2,
	     'CpG position', $black);

$gd->string ($font->gdTinyFont,
	     MARGL2- LLABLEN -1, $top - FONTH1,
	     '100%', $black);
$gd->string ($font->gdTinyFont,
	     MARGL2- LLABLEN -1, int($mid) - FONTH1,
	     '100%', $black);
$gd->string ($font->gdTinyFont,
	     MARGL2- LLABLEN -1, $bot - FONTH1,
	     '100%', $black);

$gd->string ($font->gdTinyFont,
	     MARGL2- LLABLEN -1, int($qu1) - FONTH1,
	     '  0%', $black);
$gd->string ($font->gdTinyFont,
	     MARGL2- LLABLEN -1, int($qu3) - FONTH1,
	     '  0%', $black);

$gd->string ($font->gdTinyFont,
	     LFMARG2, int(($qu1+$top)/2) - FONTH1,
	     '      Methylated (%)', $black);
$gd->string ($font->gdTinyFont,
	     LFMARG2, int(($qu1+$mid)/2) - FONTH1,
	     '    Unmethylated (%)', $black);
$gd->string ($font->gdTinyFont,
	     LFMARG2, int(($qu3+$mid)/2) - FONTH1,
	     '      Methylated (%)', $black);
$gd->string ($font->gdTinyFont,
	     LFMARG2, int(($qu3+$bot)/2) - FONTH1,
	     '    Unmethylated (%)', $black);

$gd->stringUp ($font->gdTinyFont,
	       LFMARG2, int(($qu1+$mid)/2),
	       'group1', $black);
$gd->stringUp ($font->gdTinyFont,
	       LFMARG2, int(($qu3+$bot)/2),
	       'group2', $black);

$gd->stringUp ($font->gdTinyFont,
	     $width - GLEGW + 2, $bot,
	     ' * : p-value < 0.1', $black);
$gd->stringUp ($font->gdTinyFont,
	     $width - GLEGW + 11, $bot,
	     ' **: p-value < 0.01', $black);

for ($i = 0; $i < @pos; $i++) {

    $x = MARGL2 + ($pos[$i] - $i - 1) * 2 + GWIDTH * $i +  int (GWIDTH / 2 + 1);
    $x1 = $x - int (GWIDTH / 2 + 1);
    $x2 = $x1 + GWIDTH;

    $gd->stringUp ($font->gdTinyFont,
		   $x1 + 1, HIGHT2 - 7,
		   $pos[$i], $black);

    for ($j = $x1; $j <= $x2; $j++) {
	$gd->line ($j, int($qu1),
		   $j, int($qu1+($top-$qu1)*$meth{$pos[$i]}->{ratio1}),
		   $black);
    }

    $gd->rectangle ($x1, int($qu1),
		    $x2, int($mid-($mid-$qu1)*$meth{$pos[$i]}->{ratio1}),
		    $black);

    for ($j = $x1; $j <= $x2; $j++) {
	$gd->line ($j, int($qu3),
		   $j, int($qu3+($mid-$qu3)*$meth{$pos[$i]}->{ratio2}),
		   $black);
    }

    $gd->rectangle ($x1, int($qu3),
		    $x2, int($bot-($bot-$qu3)*$meth{$pos[$i]}->{ratio2}),
		    $black);

    if ($meth{$pos[$i]}->{pval} == 1) {
	$gd->string ($font->gdTinyFont,
		     $x1 + 4, $top - FONTH1 -3,
		     '*', $black);

    } elsif ($meth{$pos[$i]}->{pval} == 2) {
	$gd->string ($font->gdTinyFont,
		     $x1 + 2, $top - FONTH1 -3,
		     '**', $black);
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
    $name .= "_compared_CpG_status_graph7.";

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
