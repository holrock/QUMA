#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeMAli.cgi                                                   *
#_* cgi for downloading alignment data                                        *
#_* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
#_* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
#_*                                                                           *
#_* 2008/12/24 First version                                                  *
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

use constant QHEAD => [qw (pos    name   qseq   qAli gAli
			   aliLen aliMis perc   gap  menum
			   unconv conv   pconv  val  dir
			   gdir static group)];

use constant HTML => q{Content-type:text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="en">
 <HEAD>
  <META HTTP-EQUIV="Content-Type" content="text/html; charset=ISO-8859-1">
  <META HTTP-EQUIV="Content-Script-Type" content="text/javascript">
  <META HTTP-EQUIV="Content-Style-Type" content="text/css">
  <LINK REV="MADE" HREF="mailto:yuichi@kumaki.jp">
  <LINK REL="INDEX" HREF="}.HL.qq{/top/index.html">
  <TITLE>Multiple alignment</TITLE>
 </HEAD>
 <BODY style="background-color:#FFFFFF">
  <TABLE ALIGN="center" border="0" cellspacing="0" cellpadding="0" summary="title table">
   <TR style="background-color:#3333CC">
    <TD><IMG src="}.HL.q{/images/spacer.gif" width="500" height="3" alt="space"></TD>
   </TR>
   <TR>
    <TD align="center" style="color:#333399;font-size:x-large;font-weight:bold;font-style:italic">
    Multiple alignment
    </TD>
   </TR>
   <TR style="background-color:#3333CC">
    <TD><IMG src="}.HL.q{/images/spacer.gif" width="500" height="3" alt="space"></TD>
   </TR>
  </TABLE>
  <FORM ACTION="%s" method="post"><INPUT TYPE="hidden" NAME="id" VALUE="%s"><INPUT TYPE="hidden" NAME="pos" VALUE="%s">
  <TABLE ALIGN="center" border="0" cellspacing="0" cellpadding="0" summary="overall table">
   <TR>
    <TD align="right" colspan="2"><A HREF="javascript:window.close();void(0);"><IMG SRC="}.HL.q{/images/iconClose.gif" ALT="close" border="0"></A></TD>
   </TR>
   <TR style="background-color:#E1E1F1">
    <TD colspan="2"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="4" alt="space"></TD>
   </TR>
   <TR style="background-color:#E1E1F1" valign="middle">
    <TD align="right"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="5" alt="space">
    <INPUT TYPE="submit" NAME="submit" VALUE="Download multiple alignment data">
    <IMG src="}.HL.q{/images/spacer.gif" width="5" height="3" alt="space">
     Format: 
    <SELECT NAME="format">
     <OPTION VALUE="txt" SELECTED>Plain text (.txt)
     <OPTION VALUE="fa">Multi-FASTA (.fa)
     <OPTION VALUE="tsv">Tab separated values (.tsv)
     <OPTION VALUE="csv">Comma separated values (.csv)
    </SELECT>
    <IMG src="}.HL.q{/images/spacer.gif" width="5" height="3" alt="space"></TD>
    <TD align="right"><A HREF="javascript:window.open('}.HL.q{/help/%s','help','width=650,height=400,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="}.HL.q{/images/help.gif" alt="help" border="0"></A>
    <IMG src="}.HL.q{/images/spacer.gif" width="5" height="3" alt="space"></TD>
   </TR>
   <TR style="background-color:#E1E1F1">
    <TD colspan="2"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="4" alt="space"></TD>
   </TR>
   <TR>
    <TD colspan="2"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="4" alt="space"></TD>
   </TR>
   <TR style="background-color:#F3F3FF">
    <TD colspan="2"><TABLE ALIGN="left" border="0" cellspacing="0" cellpadding="15" summary="alignment">
     <TR>
      <TD><TT>%s</TT></TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD colspan="2" align="right"><A HREF="javascript:window.close();void(0);"><IMG SRC="}.HL.q{/images/iconClose.gif" ALT="close" border="0"></A></TD>
   </TR>
  </TABLE>
  </FORM>
 </BODY>
</HTML>
};

my ($qhead );
my ($lc    );
my ($cgi   );
my ($data  );
my ($help  );
my (@pos   );
my ($file  );
my ($fh    );
my ($line  );
my (@gen   );
my ($ref   );
my (@data  );
my ($proj  );
my ($gseq  );
my ($glen  );
my ($i     );
my (@mali  );
my ($nlen  );
my ($len   );
my ($start );
my ($stop  );
my ($g, $q );
my ($j, $k );
my ($nextb );
my ($prevb );
my ($m     );
my ($gen   );
my ($l     );
my ($spn   );
my ($ret   );
my ($sps   );
my ($pos   );
my ($out   );
my ($seqp  );
my ($tmp   );
my ($name  );
my ($type  );
local ($_  );
local ($1  );

$qhead = QHEAD;
$lc    = LINE;
$nlen  = length NAMEG;
$spn   = ' ' x SPNUM;

$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;
ipCheck ($data);

$data->{cpgcheck} = 0
    unless (exists $data->{cpgcheck} && $data->{cpgcheck} eq 'on');
$help = $data->{cpgcheck} ? 'multiAliHelpC.html' : 'multiAliHelp.html';

$data->{pos}
    or errorAndExit ('No data to show',
		     'No data to show',
		     "No data to show : $data->{pos}");
$data->{pos} =~ /^\d+(,\d+)*$/
    or errorAndExit ('Invalid access',
		     'Invalid access',
		     "Invalid POS value : $data->{pos}");
@pos = split ',', $data->{pos};

$file = DATADIR . $data->{id};
open $fh, $file
    or errorAndExit ("Server Error!",
		     "Server Error!",
		     "open file error : $! : $file");

chomp ($line = <$fh>);
@gen = split /\t/, $line;

while ($line = <$fh>) {
    chomp $line;
    $ref = {};
    @{$ref}{@$qhead} =  split /\t/, $line;
    push @data, $ref;
}
close $fh;

shift @gen;
$proj = shift @gen;
$proj ||= '';
$proj =~ s/"//g;
shift @gen; # group1
shift @gen; # group2
shift @gen; # convdir
$gseq = shift @gen;
$glen = length $gseq;

for ($i = 0; $i < $glen; $i++) {
    $mali[$i]->{g} = substr $gseq, $i, 1;
}

@data = @data[map{$_ - 1} @pos];

for ($i = 0; $i < @data; $i++) {

    $ref = $data[$i];
    $len = length $ref->{gAli};

    for ($start = 0; $start < $len; $start++) {
	$g = substr $ref->{gAli}, $start, 1;
	last unless ($g eq '-');
    }

    for ($stop = $len - 1; $stop >= 0; $stop--) {
	$g = substr $ref->{gAli}, $stop, 1;
	last unless ($g eq '-');
    }

    $prevb = '';

    for ($j = $k = 0; $j < $stop - $start + 1; $j++) {

	$g = substr $ref->{gAli}, $start + $j, 1;
	$q = substr $ref->{qAli}, $start + $j, 1;
	if ($g eq '-') {
	    $mali[$k]->{gap}{$i} .= $q;

	} else {
	    $g eq $mali[$k]->{g} or
		errorAndExit ('Unknown error',
			      'Unknown error',
			      'Genome sequence mismatch');
	    $mali[$k]->{$i} = $q;

	    if ($ref->{gdir} == 1 && $g eq 'C') {
		if (@mali > $k + 1 && $mali[$k+1]->{g} eq 'G') { # Cpg
                    for ($m = $j+1; $m < $stop - $start + 1; $m++) {
                        $nextb = substr $ref->{qAli}, $start + $m, 1;
                        last unless ($nextb eq '-');
                    }

                    if (!$data->{cpgcheck} ||
                        $nextb && $nextb eq 'G') {
		        $mali[$k]->{state}{$i} = $q eq 'C' ? 'MeCpG'   :
			                         $q eq 'T' ? 'unMeCpG' :
				   	                     'miss'    ;
                    } else {
		        $mali[$k]->{state}{$i} = $q eq 'C' ? 'notCpG'  :
			                         $q eq 'T' ? 'notCpG'  :
				   	                     'miss'    ;
                    }
		} else {                                     # Cph
		    $mali[$k]->{state}{$i} = $q eq 'C' ? 'unconv' :
			                     $q eq 'T' ? 'conv'   :
					                 'miss'   ;
		}

	    } elsif ($ref->{gdir} == -1 && $g eq 'G') {
		if ($k > 0 && $mali[$k-1]->{g} eq 'C') {     # cpG
                    if (!$data->{cpgcheck} ||
                        $prevb && $prevb eq 'C') {
		        $mali[$k]->{state}{$i} = $q eq 'G' ? 'MeCpG'   :
			                         $q eq 'A' ? 'unMeCpG' :
					                     'miss'    ;
                    } else {
		        $mali[$k]->{state}{$i} = $q eq 'G' ? 'notCpG'  :
			                         $q eq 'A' ? 'notCpG'  :
					                     'miss'    ;
                    }
		} else {                                     # hpG
		    $mali[$k]->{state}{$i} = $q eq 'G' ? 'unconv'   :
			                     $q eq 'A' ? 'conv' :
					                 'miss'    ;
		}
	    } elsif ($q eq '-') {
		$mali[$k]->{state}{$i} = 'qgap';
	    } elsif ($g ne $q) {
		$mali[$k]->{state}{$i} = 'miss';
	    } else {
		$mali[$k]->{state}{$i} = 'match';
	    }
            $prevb = $q;
	    $k++;
	}
    }

    $ref->{name} =~ s/^(\S+) sequence exported from \1_\w\d{2}_\d{3}\.ab1$/$1/;
    $ref->{name} =~ s/^(\S+)\.ab1 CHROMAT_FILE: \1\.ab1 PHD_FILE: \1\.ab1\.phd\.1 CHEM: \S+ DYE: \S+ TIME: \S+.*20\d\d$/$1/;
    $ref->{name} =~ s/\.txt$//;
    $ref->{name} =~ s/\.fa(sta)?$//;
    $ref->{name} =~ s/\.seq$//i;
    $ref->{name} =~ s/\.ab1$//i;
    $ref->{name} =~ s/^\s+//;
    $ref->{name} =~ s/\s+$//;
    $ref->{name} =~ s/\.ab1 no comment$//i;
    $ref->{name} =~ s/\.ab1 Length=\d+$//;
    $ref->{name} =~ s/^ID\|//;
    $nlen = length $ref->{name} if ($nlen < length ($ref->{name}))
}

for ($i = $j = 0; $i < @mali; $i++, $j++) {

    $len = 0;

    if (exists $mali[$i]->{gap}) {
	foreach $k (keys %{$mali[$i]->{gap}}) {
	    $len = length $mali[$i]->{gap}{$k}
	        if ($len < length $mali[$i]->{gap}{$k});
	}
    }
    
    $gen .= '-' x $len . $mali[$i]->{g};

    for ($k = 0; $k < @data; $k++) {

	$ref = $data[$k];

	if ($len) {
	    $mali[$i]->{gap}{$k} ||= '';
	    $mali[$i]->{gap}{$k} .=
		'-' x ($len - length ($mali[$i]->{gap}{$k}));
	    $ref->{multi} .= $mali[$i]->{gap}{$k}
	}

	for ($l = 0; $l < $len; $l++) {
	    $ref->{mstate}{$j+$l} = 'ggap';
	}

	$ref->{multi} .= $mali[$i]->{$k};
	$ref->{mstate}{$j+$len} = $mali[$i]->{state}{$k};
    }
    $j += $len;
}

$len = length $gen;
($sps, $ret) = $data->{submit} ? (' ', "\r\n") : ('&nbsp;', "<BR>\n");

for ($i = 0, $out = ''; $i < 1 + int (($len - 1) / $lc); $i++) {

    last if ($data->{submit} && 
             ($data->{format} eq 'fa'  ||
              $data->{format} eq 'csv' ||
              $data->{format} eq 'tsv'));

    $pos = $lc * $i + 1;
    $out .= ($sps x ($nlen + SPNUM + 1 - length $pos) . $pos);

    for ($j = 1; $j <= int ($lc / POSDIS); $j++) {
	$pos = $lc * $i + POSDIS * $j;
	$out .= $sps unless ($j == 1);
	$out .= ($sps x (POSDIS - 1 - length $pos) . $pos);
	last if ($pos + POSDIS > $len);
    }

    $out .= $ret;

    $seqp = substr $gen, $lc * $i, $lc;
    $seqp =~ s/(\-+)/<A STYLE="COLOR:#00FF00">$1<\/A>/g unless ($data->{submit});

    $tmp = sprintf "%-${nlen}s$spn", NAMEG;
    $tmp =~ s/ /$sps/g;
    $out .= $tmp;
    $out .= $seqp . $ret;

    foreach $ref (@data) {

	$seqp = '';

	for ($j = $lc*$i; $j < $lc*($i+1) && $j < length $gen; $j++) {
	    $seqp .=
		$ref->{mstate}{$j} eq 'ggap'    ? '<A STYLE="COLOR:#00FF00">' :
		$ref->{mstate}{$j} eq 'qgap'    ? '<A STYLE="COLOR:#00FF00">' :
		$ref->{mstate}{$j} eq 'miss'    ? '<A STYLE="COLOR:#00FF00">' :
		$ref->{mstate}{$j} eq 'MeCpG'   ? '<A STYLE="COLOR:#FF00FF">' :
		$ref->{mstate}{$j} eq 'unMeCpG' ? '<A STYLE="COLOR:#0000FF">' :
		$ref->{mstate}{$j} eq 'unconv'  ? '<A STYLE="COLOR:#FF9955">' :
                $ref->{mstate}{$j} eq 'notCpG'  ? '<A STYLE="COLOR:#00AA00">' :
             	                                  '' unless ($data->{submit});

	    $seqp .= substr $ref->{multi}, $j, 1;
            $seqp .= '</A>' unless ($ref->{mstate}{$j} eq 'match' ||
                                    $ref->{mstate}{$j} eq 'conv'  ||
                                    $data->{submit});
	}
	$tmp = sprintf "%-${nlen}s$spn", $ref->{name};
	$tmp =~ s/ /$sps/g;
	$out .= $tmp;
	$out .= $seqp . $ret;
    }
    $out .= $ret if ($i + 1 < 1 + int (($len - 1) / $lc));
}

unless ($data->{submit}) {
    printf HTML, MALIGN, $data->{id}, $data->{pos}, $help, $out;
    exit;
}

$name  = substr $data->{id}, 0, 12;
$name .= "_$proj" if ($proj);
$name .= '_multiple_alignment_data.';

if ($data->{format} eq 'txt') {
    $name .= 'txt';
    $type  = 'text/plain';

} elsif ($data->{format} eq 'fa') {
    $out = ">" . NAMEG . "\r\n";
    $gen =~ s/(.{1,$lc})/$1\r\n/g;
    $out .= $gen;
    foreach $ref (@data) {
	$out .= ">$ref->{name}\r\n";
	$ref->{multi} =~ s/(.{1,$lc})/$1\r\n/g;
	$out .= $ref->{multi};
    }
    $name .= 'fa';
    $type  = 'text/fasta';

} elsif ($data->{format} eq 'tsv') {
    $out = NAMEG . "\t$gen\r\n";
    foreach $ref (@data) {
	$out .= "$ref->{name}\t$ref->{multi}\r\n";
    }
    $name .= 'tsv';
    $type  = 'text/tsv';

} else {  # CSV
    $out = qq{"} . NAMEG . qq{","$gen"\r\n};
    foreach $ref (@data) {
	$out .= qq{"$ref->{name}","$ref->{multi}"\r\n};
    }
    $name .= 'csv';
    $type  = 'text/csv';
}

$len = length $out;

print qq{Content-Disposition: attachment; filename="$name"
Content-Length: $len
Content-Type: $type
Status: 200 OK

$out};

###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
