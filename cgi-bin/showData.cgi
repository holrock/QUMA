#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: showData.cgi                                                   *
#_* cgi for creating alignment view                                           *
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

use constant HTML => q{Content-type:text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="en">
 <HEAD>
  <META HTTP-EQUIV="Content-Type" content="text/html; charset=ISO-8859-1">
  <META HTTP-EQUIV="Content-Script-Type" content="text/javascript">
  <META HTTP-EQUIV="Content-Style-Type" content="text/css">
  <LINK REV="MADE" HREF="mailto:yuichi@kumaki.jp">
  <LINK REL="INDEX" HREF="}.HL.qq{/top/index.html">
  <TITLE>Alignment result</TITLE>
 </HEAD>
 <BODY style="background-color:#FFFFFF">
  <TABLE ALIGN="center" border="0" cellspacing="0" cellpadding="0" summary="title table">
   <TR style="background-color:#3333CC">
    <TD><IMG src="}.HL.q{/images/spacer.gif" width="500" height="3" alt="space"></TD>
   </TR>
   <TR>
    <TD align="center" style="color:#333399;font-size:x-large;font-weight:bold;font-style:italic">
    Alignment result
    </TD>
   </TR>
   <TR style="background-color:#3333CC">
    <TD><IMG src="}.HL.q{/images/spacer.gif" width="500" height="3" alt="space"></TD>
   </TR>
  </TABLE>
  <FORM ACTION="%s" method="post"><INPUT TYPE="hidden" NAME="id" VALUE="%s"><INPUT TYPE="hidden" NAME="pos" VALUE="%d"><INPUT TYPE="hidden" NAME="cpgcheck" VALUE="%s">
  <TABLE ALIGN="center" border="0" cellspacing="0" cellpadding="0" summary="overall table">
   <TR>
    <TD align="right" colspan="3"><A HREF="javascript:window.close();void(0);"><IMG SRC="}.HL.q{/images/iconClose.gif" ALT="close" border="0"></A></TD>
   </TR>
   <TR style="background-color:#F3F3FF">
    <TD><DIV style="font-size:large;font-weight:bold">&nbsp;<IMG width="13" height="13" src="}.HL.q{/images/icon034.gif" alt="list">
        Summary of information</DIV></TD>
    <TD valign="bottom"><INPUT TYPE="submit" NAME="submit" VALUE="Download alignment data"></TD>
    <TD align="right" valign="bottom"><A HREF="javascript:window.open('}.HL.q{/help/aliSummaryHelp.html','help','width=300,height=420,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="}.HL.q{/images/help.gif" alt="help" border="0"></A>&nbsp;&nbsp;</TD>
   </TR>
   <TR>
    <TD colspan="3"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="2" alt="space"></TD>
   </TR>
   <TR>
    <TD colspan="3"><TABLE style="font-size:small" width="100%%" ALIGN="left" border="0" cellspacing="2" cellpadding="2" summary="summary information">
%s     <TR style="background-color:#D1D1F1">
      <TH colspan="3" align="left">Bisulfite sequence name</TH>
      <TD colspan="%s">%s</TD>
     </TR>
     <TR style="background-color:#EAEAFB">
      <TD colspan="5" align="left"><A style="font-weight:bold">%s =&gt; %s conversion</A> <A style="font-size:small">(conversion and detection of %s strand of the genomic sequence)</A></TD>
     </TR>
     <TR style="background-color:#D1D1F1">
      <TH align="left">Length of bisulfite sequence</TH>
      <TD align="right">%d</TD>
      <TD style="background-color:#FFFFFF" ></TD>
      <TH align="left">Length of target genome sequence</TH>
      <TD align="right">%d</TD>
     </TR>
     <TR style="background-color:#EAEAFB">
      <TH align="left">Aligned region of bisulfite sequence</TH>
      <TD align="center">%d - %d</TD>
      <TD style="background-color:#FFFFFF" ></TD>
      <TH align="left">Alignment direction</TH>
      <TD align="center">%s</TD>
     </TR>
     <TR style="background-color:#D1D1F1">
      <TH align="left">Me-CpG</TH>
      <TD align="center">%d/%d (%.1f %%)</TD>
      <TD style="background-color:#FFFFFF" ></TD>
      <TH align="left">Unconverted CpHs (%% converted)</TH>
      <TD align="center">%d/%d (%.1f %%)</TD>
     </TR>
     <TR style="background-color:#EAEAFB">
      <TH colspan="3" align="left">mismatch (gap) / alignment length (%% identity)</TH>
      <TD colspan="2" align="center">%d (%d) / %d (%.1f %%)</TD>
     </TR>
     <TR style="background-color:#D1D1F1">
      <TH colspan="1" align="left">Methylation pattern</TH>
      <TD colspan="4"><IMG SRC="%s" alt="methfig"></TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD colspan="3"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="4" alt="space"></TD>
   </TR>
   <TR style="background-color:#E1E1F1">
    <TD colspan="2"><DIV style="font-size:large;font-weight:bold">&nbsp;<IMG width="13" height="13" src="}.HL.q{/images/icon034.gif" alt="list">
        Target genome sequence</DIV></TD>
    <TD align="right"></TD>
   </TR>
   <TR>
    <TD colspan="3"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="2" alt="space"></TD>
   </TR>
   <TR style="background-color:#F9F9FF">
    <TD colspan="3"><TABLE ALIGN="left" border="0" cellspacing="0" cellpadding="5" summary="target genome sequence">
     <TR>
      <TD><TT>%s</TT></TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD colspan="3"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="4" alt="space"></TD>
   </TR>
   <TR style="background-color:#E1E1F1">
    <TD colspan="2"><DIV style="font-size:large;font-weight:bold">&nbsp;<IMG width="13" height="13" src="}.HL.q{/images/icon034.gif" alt="list">
        Bisulfite sequence</DIV></TD>
    <TD align="right" valign="bottom"><A HREF="javascript:window.open('}.HL.q{/help/biseqHelp.html','help','width=300,height=180,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="}.HL.q{/images/help.gif" alt="help" border="0"></A>&nbsp;&nbsp;</TD>
   </TR>
   <TR>
    <TD colspan="3"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="2" alt="space"></TD>
   </TR>
   <TR style="background-color:#F9F9FF">
    <TD colspan="3"><TABLE ALIGN="left" border="0" cellspacing="0" cellpadding="5" summary="bisulfite sequence">
     <TR>
      <TD><TT>%s</TT></TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD colspan="3"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="4" alt="space"></TD>
   </TR>
   <TR style="background-color:#E1E1F1">
    <TD colspan="2"><DIV align="left" style="font-size:large;font-weight:bold">
        <IMG width="13" height="13" src="}.HL.q{/images/icon034.gif" alt="list">
         Alignment</DIV>
    <TD align="right" valign="bottom"><A HREF="javascript:window.open('}.HL.q{/help/%s','help','width=300,height=600,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="}.HL.q{/images/help.gif" alt="help" border="0"></A>&nbsp;&nbsp;</TD>
   </TR>
   <TR>
    <TD colspan="3"><IMG src="}.HL.q{/images/spacer.gif" width="5" height="2" alt="space"></TD>
   </TR>
   <TR style="background-color:#F9F9FF">
    <TD colspan="3"><TABLE ALIGN="left" border="0" cellspacing="0" cellpadding="15" summary="alignment">
     <TR>
      <TD><TT>%s</TT></TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD colspan="2" valign="bottom"><INPUT TYPE="submit" NAME="submit" VALUE="Download alignment data"></TD>
    <TD align="right"><A HREF="javascript:window.close();void(0);"><IMG SRC="}.HL.q{/images/iconClose.gif" ALT="close" border="0"></A></TD>
   </TR>
  </TABLE>
  </FORM>
 </BODY>
</HTML>
};

my ($lc     );
my ($cgi    );
my ($data   );
my ($file   );
my ($fh     );
my ($line   );
my (@gen    );
my ($proj   );
my ($grp1   );
my ($grp2   );
my (@que    );
my ($cpgn   );
my (%cpg    );
my ($i      );
my ($gseq   );
my ($glen   );
my ($qseq   );
my ($qlen   );
my ($gAli   );
my ($qAli   );
my ($dir    );
my ($gdir   );
my ($start  );
my ($stop   );
my ($qstart );
my ($qstop  );
my ($q      );
my ($g      );
my ($j      );
my ($k      );
my ($l      );
my ($cpg    );
my ($qseqout);
my ($bbase  );
my ($abase  );
my ($len    );
my ($gout   );
my ($ali    );
my ($qout   );
my ($nextb  );
my ($prevb  );
my ($m      );
my ($output );
my ($cph    );
my ($url    );
my ($col    );
my ($name   );
my ($grp    );
my ($cpgp   );
my ($help   );
local ($!   );
local ($_   );
local ($1   );

$lc = LINE;
$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;
ipCheck ($data);
$data->{pos} =~ /^\d+$/
    or errorAndExit ('Invalid access', 'Invalid access', "Invalid POS value : $data->{pos}");
$data->{cpgcheck} = 0
    unless (exists $data->{cpgcheck} && $data->{cpgcheck} eq 'on');

$file = DATADIR . $data->{id};
open $fh, $file or errorAndExit ("Server Error!", "Server Error!", "open file error : $! : $file");
chomp ($line = <$fh>);
@gen = split /\t/, $line;

while ($line = <$fh>) {
    last if (++$i == $data->{pos});
}
close $fh;
chomp $line;
@que = split /\t/, $line;

shift @gen;
$proj = shift @gen;
$proj ||= '';
$grp1 = shift @gen;
$grp1 ||= '';
$grp2 = shift @gen;
$grp2 ||= '';
shift @gen; # convdir
$gseq = shift @gen;
$glen = length $gseq;
$gseq =~ s/(\w{1,$lc})/$1<BR>\n/g;
$qseq = $que[2];
$qlen = length $qseq;
$qseq =~ s/(\w{1,$lc})/$1<BR>\n/g;
$cpgn = shift @gen;
%cpg = map {$_ => 1} @gen;

$qAli = $que[3];
$gAli = $que[4];
$dir  = $que[14];
$gdir = $que[15];

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

$qseqout = q{<A STYLE="COLOR:#777777">} if ($qstart);

for ($i = $j = 0; $i < length $qseq; $i++) {
    $q = substr $qseq, $i, 1;
    if ($q eq '<' ... $q eq '>') {
	$qseqout .= $q;
    } elsif ($q eq "\n") {
	$qseqout .= $q;
    } else {
	$qseqout .= $q;
	$qseqout .= q{<A STYLE="COLOR:#777777">} if ($j == $qstop);
	$j++;
	$qseqout .= q{</A>} if ($j == $qstart);
    }
}

$qseqout .= q{</A>};

if ($gdir == 1) {
    ($bbase, $abase) = ('C', 'T');
} else {
    ($bbase, $abase) = ('G', 'A');
}

for ($j = $k = $l = 0, $i = $start; $i <= $stop; $i++) {

    $nextb = '';
    $j = $i - $start + 1;
    $g = substr $gAli, $i, 1;
    $q = substr $qAli, $i, 1;
    $k++ unless ($g eq '-');
    $l++ unless ($q eq '-');

    if ($j % LINE == 1) {
	$k++ if ($g eq '-');
	$l++ if ($q eq '-');
	$gout = 'Genome'   .'&nbsp;'x(3 + 6 - length($k)).$k.'&nbsp;'x2;
	$ali  =             '&nbsp;'x(9 + 6 + 2);
	$qout = 'Bisulfite'.'&nbsp;'x(0 + 6 - length($l)).$l.'&nbsp;'x2;
	$k-- if ($g eq '-');
	$l-- if ($q eq '-');
    }

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
		    $gout .= qq{<A STYLE="COLOR:#FF00FF">$bbase</A>};
		    $ali  .=  q{<A STYLE="COLOR:#FF00FF">*</A>};
		    $qout .= qq{<A STYLE="COLOR:#FF00FF">$bbase</A>};
		} else {
		    $gout .= qq{<A STYLE="COLOR:#00AA00">$bbase</A>};
		    $ali  .=  q{<A STYLE="COLOR:#00AA00">+</A>};
		    $qout .= qq{<A STYLE="COLOR:#00AA00">$bbase</A>};
		}
	    } else {
		$gout .= qq{<A STYLE="COLOR:#FF9955">$bbase</A>};
		$ali  .=  q{<A STYLE="COLOR:#FF9955">!</A>};
		$qout .= qq{<A STYLE="COLOR:#FF9955">$bbase</A>};
	    }
	} elsif ($q eq $abase) {
	    if ($cpg) {
		if (!$data->{cpgcheck} ||
		    $gdir == 1 && $nextb && $nextb eq 'G' ||
		    $gdir != 1 && $prevb && $prevb eq 'C') {
		    $gout .= qq{<A STYLE="COLOR:#0000FF">$bbase</A>};
		    $ali  .=  q{<A STYLE="COLOR:#0000FF">#</A>};
		    $qout .= qq{<A STYLE="COLOR:#0000FF">$abase</A>};
	        } else {
		    $gout .= qq{<A STYLE="COLOR:#00AA00">$bbase</A>};
		    $ali  .=  q{<A STYLE="COLOR:#00AA00">+</A>};
		    $qout .= qq{<A STYLE="COLOR:#00AA00">$abase</A>};
		}
	    } else {
		$gout .= qq{<A STYLE="COLOR:#555555">$bbase</A>};
		$ali  .=  q{<A STYLE="COLOR:#555555">:</A>};
		$qout .= qq{<A STYLE="COLOR:#555555">$abase</A>};
	    }
	} else {
	    $gout .= qq{<A STYLE="COLOR:#888888">$g</A>};
	    $ali  .= qq{&nbsp;};
	    $qout .= qq{<A STYLE="COLOR:#888888">$q</A>};
	}

    } elsif ($g eq $q) {
	$gout .= $g;
	$ali  .= '|';
	$qout .= $q;
    } else {
	$gout .= qq{<A STYLE="COLOR:#888888">$g</A>};
	$ali  .= qq{&nbsp;};
	$qout .= qq{<A STYLE="COLOR:#888888">$q</A>};
    }

    if ($j % LINE == 0) {
	$gout .= "<BR>\n";
	$ali  .= "<BR>\n";
	$qout .= "<BR>\n";

	$output .= $gout . $ali . $qout . "<BR>\n";
	$gout = $ali = $qout = '';
    }

    $prevb = $q unless ($q eq '-');
}

if ($j % LINE > 1) {
	$gout .= "<BR>\n";
	$ali  .= "<BR>\n";
	$qout .= "<BR>\n";
	$output .= $gout . $ali . $qout;
}

$dir = $dir * $gdir == 1 ? 'forward' : 'reverse';
$cph = $que[10] + $que[11];
$cpg = $que[13] =~ y/01//;
$url = sprintf SGLURL2, $data->{id}, $data->{pos};
$name = htmlSunitize ($que[1]);
if ($que[16]) {
    $col = 1;
    $name .= qq{</TD><TD>group$que[17]};
} else {
    $col = 2;
}

$gdir = $gdir == 1 ? 'forward' : 'reverse';

$proj = htmlSunitize ($proj) if ($proj);
$grp1 = htmlSunitize ($grp1) if ($grp1);
$grp2 = htmlSunitize ($grp2) if ($grp2);

$proj = qq{     <TR style="background-color:#EAEAFB">
      <TH align="left">Project name</TH>
      <TD colspan="4">$proj</TD>
     </TR>
} if ($proj);

$grp = '';

if ($que[16]) {
    if ($que[17] == 1) {
	$grp = $grp1 if ($grp1);
    } else {
	$grp = $grp2 if ($grp2);
    }
} elsif ($grp1) {
    $grp = $grp1;
}

$proj =~ s/EAEAFB/D1D1F1/ if ($grp && $proj);
$proj .= qq{     <TR style="background-color:#EAEAFB">
      <TH align="left">Sequence group name</TH>
      <TD colspan="4">$grp</TD>
     </TR>
} if ($grp);

    $cpgp = $cpg ? 100 * $que[9]/$cpg : 0;
    $help = $data->{cpgcheck} ? 'aliHelpC.html' : 'aliHelp.html';
    printf HTML, ALIDATA, $data->{id}, $data->{pos}, $data->{cpgcheck},
             $proj, $col, $name, $bbase, $abase, $gdir,
             $qlen, $glen, $qstart + 1, $qstop + 1, $dir,
             $que[9], $cpg, $cpgp, $que[10], $cph, $que[12], $que[6], $que[8],
             $que[5], $que[7], $url, $gseq, $qseqout, $help, $output;

###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
