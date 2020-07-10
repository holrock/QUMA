#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeStatData.cgi                                               *
#_* cgi for creating statistical analysis result page                         *
#_* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
#_* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
#_*                                                                           *
#_* 2008/02/20 First open source version                                      *
#_* 2008/03/31 "unselect all" link is added                                   *
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
use Statistics::Lite qw(:funcs);

use BFSetting;
use BFUtils;

use constant HEAD => q[Content-type:text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="en">
 <HEAD>
  <META HTTP-EQUIV="Content-Type" content="text/html; charset=ISO-8859-1">
  <META HTTP-EQUIV="Content-Script-Type" content="text/javascript">
  <META HTTP-EQUIV="Content-Style-Type" content="text/css">
  <LINK REV="MADE" HREF="mailto:yuichi@kumaki.jp">
  <LINK REL="INDEX" HREF="].HL.q[/top/index.html">
  <TITLE>Results of statistical analysis</TITLE>
  <SCRIPT type="text/javascript" language="JavaScript">
  <!--

    var browser;

    if (document.getElementById) {
      browser = "IE56NN6";
    } else if (document.all) {
      browser = "IE46";
    } else if (document.layers) {
      browser = "NN4";
    }

    function checkValue() {
	if (document.allform.optionShow.value == 0) {
	    document.allform.optionShow.value = 1;
	} else {
	    document.allform.optionShow.value = 0;
	}
	foption();

	document.allform.graphShow.value--;
	if (document.allform.graphShow.value < 0) {
	    document.allform.graphShow.value = 7;
	}
	fgraph();
    }

    function foption() {
       if (browser == "IE56NN6") {

         optionAnc  = document.getElementById("options");
	 optionText = document.getElementById("options").childNodes.item(0);
	 optionAnc.removeChild(optionText);

         if (document.allform.optionShow.value == 0) {
	   document.getElementById("optionList").style.display = "block";
	   document.getElementById("optionOrder").style.display = "block";
	   document.getElementById("optImage1").src = "].HL.q[/images/icon033.gif";
	   newText = document.createTextNode(" Hide options");
           document.allform.optionShow.value = "1";

         } else {
           document.getElementById("optionList").style.display = "none";
           document.getElementById("optionOrder").style.display = "none";
	   document.getElementById("optImage1").src = "].HL.q[/images/icon030.gif";
	   newText = document.createTextNode(" Show options");
           document.allform.optionShow.value = "0";
	 }

         optionAnc.appendChild(newText);

       } else if (browser == "IE46") {
         if (document.allform.optionShow.value == 0) {
           optionList.style.display = "block";
           optionOrder.style.display = "block";
           document.images[21].src = "].HL.q[/images/icon033.gif";
	   options.innerText = " Hide options";
           document.allform.optionShow.value = "1";

         } else {
           optionList.style.display= "none";
           optionOrder.style.display = "none";
           document.images[21].src = "].HL.q[/images/icon030.gif";
	   options.innerText = " Show options";
           document.allform.optionShow.value = "0";
         }
       }
    }

    function fgraph() {
       if (browser == "IE56NN6") {

         if (document.allform.graphShow.value == 0) {
	   document.getElementById("compGraph1").style.display = "none";
	   document.getElementById("compGraph2").style.display = "block";
	   document.getElementById("compGraph3").style.display = "none";
	   document.getElementById("compGraph4").style.display = "none";
	   document.getElementById("compGraph5").style.display = "none";
	   document.getElementById("compGraph6").style.display = "none";
	   document.getElementById("compGraph7").style.display = "none";
	   document.getElementById("compGraph8").style.display = "none";
           document.allform.graphShow.value = 1;

         } else if (document.allform.graphShow.value == 1) {
	   document.getElementById("compGraph1").style.display = "none";
	   document.getElementById("compGraph2").style.display = "none";
	   document.getElementById("compGraph3").style.display = "block";
	   document.getElementById("compGraph4").style.display = "none";
	   document.getElementById("compGraph5").style.display = "none";
	   document.getElementById("compGraph6").style.display = "none";
	   document.getElementById("compGraph7").style.display = "none";
	   document.getElementById("compGraph8").style.display = "none";
           document.allform.graphShow.value = 2;

         } else if (document.allform.graphShow.value == 2) {
	   document.getElementById("compGraph1").style.display = "none";
	   document.getElementById("compGraph2").style.display = "none";
	   document.getElementById("compGraph3").style.display = "none";
	   document.getElementById("compGraph4").style.display = "block";
	   document.getElementById("compGraph5").style.display = "none";
	   document.getElementById("compGraph6").style.display = "none";
	   document.getElementById("compGraph7").style.display = "none";
	   document.getElementById("compGraph8").style.display = "none";
           document.allform.graphShow.value = 3;

         } else if (document.allform.graphShow.value == 3) {
	   document.getElementById("compGraph1").style.display = "none";
	   document.getElementById("compGraph2").style.display = "none";
	   document.getElementById("compGraph3").style.display = "none";
	   document.getElementById("compGraph4").style.display = "none";
	   document.getElementById("compGraph5").style.display = "block";
	   document.getElementById("compGraph6").style.display = "none";
	   document.getElementById("compGraph7").style.display = "none";
	   document.getElementById("compGraph8").style.display = "none";
           document.allform.graphShow.value = 4;

         } else if (document.allform.graphShow.value == 4) {
	   document.getElementById("compGraph1").style.display = "none";
	   document.getElementById("compGraph2").style.display = "none";
	   document.getElementById("compGraph3").style.display = "none";
	   document.getElementById("compGraph4").style.display = "none";
	   document.getElementById("compGraph5").style.display = "none";
	   document.getElementById("compGraph6").style.display = "block";
	   document.getElementById("compGraph7").style.display = "none";
	   document.getElementById("compGraph8").style.display = "none";
           document.allform.graphShow.value = 5;

         } else if (document.allform.graphShow.value == 5) {
	   document.getElementById("compGraph1").style.display = "none";
	   document.getElementById("compGraph2").style.display = "none";
	   document.getElementById("compGraph3").style.display = "none";
	   document.getElementById("compGraph4").style.display = "none";
	   document.getElementById("compGraph5").style.display = "none";
	   document.getElementById("compGraph6").style.display = "none";
	   document.getElementById("compGraph7").style.display = "block";
	   document.getElementById("compGraph8").style.display = "none";
           document.allform.graphShow.value = 6;

         } else if (document.allform.graphShow.value == 6) {
	   document.getElementById("compGraph1").style.display = "none";
	   document.getElementById("compGraph2").style.display = "none";
	   document.getElementById("compGraph3").style.display = "none";
	   document.getElementById("compGraph4").style.display = "none";
	   document.getElementById("compGraph5").style.display = "none";
	   document.getElementById("compGraph6").style.display = "none";
	   document.getElementById("compGraph7").style.display = "none";
	   document.getElementById("compGraph8").style.display = "block";
           document.allform.graphShow.value = 7;

         } else {
	   document.getElementById("compGraph1").style.display = "block";
	   document.getElementById("compGraph2").style.display = "none";
	   document.getElementById("compGraph3").style.display = "none";
	   document.getElementById("compGraph4").style.display = "none";
	   document.getElementById("compGraph5").style.display = "none";
	   document.getElementById("compGraph6").style.display = "none";
	   document.getElementById("compGraph7").style.display = "none";
	   document.getElementById("compGraph8").style.display = "none";
           document.allform.graphShow.value = 0;
	 }

       } else if (browser == "IE46") {
         if (document.allform.graphShow.value == 0) {
           compGraph1.style.display = "none";
           compGraph2.style.display = "block";
           compGraph3.style.display = "none";
           compGraph4.style.display = "none";
           compGraph5.style.display = "none";
           compGraph6.style.display = "none";
           compGraph7.style.display = "none";
           compGraph8.style.display = "none";
           document.allform.graphShow.value = 1;

         } else if (document.allform.graphShow.value == 1) {
           compGraph1.style.display = "none";
           compGraph2.style.display = "none";
           compGraph3.style.display = "block";
           compGraph4.style.display = "none";
           compGraph5.style.display = "none";
           compGraph6.style.display = "none";
           compGraph7.style.display = "none";
           compGraph8.style.display = "none";
           document.allform.graphShow.value = 2;

         } else if (document.allform.graphShow.value == 2) {
           compGraph1.style.display = "none";
           compGraph2.style.display = "none";
           compGraph3.style.display = "none";
           compGraph4.style.display = "block";
           compGraph5.style.display = "none";
           compGraph6.style.display = "none";
           compGraph7.style.display = "none";
           compGraph8.style.display = "none";
           document.allform.graphShow.value = 3;

         } else if (document.allform.graphShow.value == 3) {
           compGraph1.style.display = "none";
           compGraph2.style.display = "none";
           compGraph3.style.display = "none";
           compGraph4.style.display = "none";
           compGraph5.style.display = "block";
           compGraph6.style.display = "none";
           compGraph7.style.display = "none";
           compGraph8.style.display = "none";
           document.allform.graphShow.value = 4;

         } else if (document.allform.graphShow.value == 4) {
           compGraph1.style.display = "none";
           compGraph2.style.display = "none";
           compGraph3.style.display = "none";
           compGraph4.style.display = "none";
           compGraph5.style.display = "none";
           compGraph6.style.display = "block";
           compGraph7.style.display = "none";
           compGraph8.style.display = "none";
           document.allform.graphShow.value = 5;

         } else if (document.allform.graphShow.value == 5) {
           compGraph1.style.display = "none";
           compGraph2.style.display = "none";
           compGraph3.style.display = "none";
           compGraph4.style.display = "none";
           compGraph5.style.display = "none";
           compGraph6.style.display = "none";
           compGraph7.style.display = "block";
           compGraph8.style.display = "none";
           document.allform.graphShow.value = 6;

         } else if (document.allform.graphShow.value == 6) {
           compGraph1.style.display = "none";
           compGraph2.style.display = "none";
           compGraph3.style.display = "none";
           compGraph4.style.display = "none";
           compGraph5.style.display = "none";
           compGraph6.style.display = "none";
           compGraph7.style.display = "none";
           compGraph8.style.display = "block";
           document.allform.graphShow.value = 7;

         } else {
           compGraph1.style.display = "block";
           compGraph2.style.display = "none";
           compGraph3.style.display = "none";
           compGraph4.style.display = "none";
           compGraph5.style.display = "none";
           compGraph6.style.display = "none";
           compGraph7.style.display = "none";
           compGraph8.style.display = "none";
           document.allform.graphShow.value = 0;
         }
       }
    }

    function selectAll() {%s
    }

    function unselectAll() {%s
    }
  //-->
  </SCRIPT>
 </HEAD>
 <BODY style="background-color:#FFFFFF">
  <TABLE ALIGN="center" border="0" cellspacing="0" cellpadding="0" summary="title table">
   <TR style="background-color:#3333CC">
    <TD><IMG src="].HL.q[/images/spacer.gif" width="800" height="5" alt="space"></TD>
   </TR>
   <TR>
    <TD align="center" style="color:#333399;font-size:xx-large;font-weight:bold;font-style:italic">
	Results of statistical analysis
    </TD>
   </TR>
   <TR style="background-color:#3333CC">
    <TD><IMG src="].HL.q[/images/spacer.gif" width="800" height="5" alt="space"></TD>
   </TR>
  </TABLE>
  <BR>
  <FORM ACTION="%s" method="post" target="downner" name="allform">
  <INPUT TYPE="hidden" NAME="id" VALUE="%s">
  <INPUT TYPE="hidden" NAME="optionShow" VALUE="%d">
  <INPUT TYPE="hidden" NAME="graphShow" VALUE="%d">
  <INPUT TYPE="hidden" NAME="cpgcheck" VALUE="%s">
  <INPUT TYPE="hidden" NAME="uniq" VALUE="%s">
  <TABLE ALIGN="left" border="0" cellspacing="0" cellpadding="0" summary="overall table">
   <TR>
    <TD><TABLE border="0" cellspacing="2" cellpadding="3" summary="summary information table">
     <TR style="background-color:#F3F3FF">
      <TD colspan="%d"><DIV style="font-size:large;font-weight:bold">&nbsp;<IMG width="13" height="13" src="].HL.q[/images/icon034.gif" alt="list">&nbsp;
	Summary of information</DIV></TD>
     </TR>
     <TR style="background-color:#E7E7F8">
%s      <TH rowspan="2">Length of target<BR>genome sequence</TH>
      <TH rowspan="2">Number of<BR>CpGs</TH>
      <TH colspan="2">Number of bisulfite sequences<BR>(used / excluded / total)</TH>
     </TR>
     <TR style="background-color:#E7E7F8">
%s      <TH>group1</TH>
      <TH>group2</TH>
     </TR>
     <TR style="background-color:#EEEEFF">
%s      <TD align="right">%d</TD>
      <TD align="right">%d</TD>
      <TD align="right">%d / %d / %d</TD>
      <TD align="right">%d / %d / %d</TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD><IMG src="].HL.q[/images/spacer.gif" width="800" height="2" alt="space"></TD>
   </TR>
   <TR>
    <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="methylation status table">
     <TR>
      <TD style="background-color:#E3E3F1"><DIV style="font-size:large;font-weight:bold">&nbsp;<IMG width="13" height="13" src="].HL.q[/images/icon034.gif" alt="list">
      Statistical data</DIV></TD>
     </TR>
     <TR>
      <TD style="background-color:#F1F7FE"><TABLE border="0" cellspacing="2" cellpadding="3" summary="methylation status each table" style="font-size:small">
];
use constant SUMTAB1 =>  q[       <TR style="background-color:#D1D1E1">
        <TH colspan="2">CpG position</TH>
];
use constant SUMTAB2 =>  q[        <TH ALIGN="right">%s</TH>
];
use constant SUMTAB3 =>  q[       </TR>
       <TR style="background-color:#DDDDEE">
        <TH rowspan="3" style="background-color:#E7E7F8">Me-CpG</TH>
];
use constant SUMTAB4 =>  q[        <TH>%s</TH>
];
use constant SUMTAB5 =>  q[        <TD ALIGN="right">%d/%d<BR>%.1f%%</TD>
];

use constant SUMTAB6 =>  q[       </TR>
       <TR style="background-color:%s">
];

use constant SUMTAB7 =>  q[       </TR>
       <TR>
        <TD></TD>
       </TR>
       <TR style="background-color:#D1D1E1">
        <TH colspan="2">CpG position</TH>
];

use constant SUMTAB8 =>  q[        <TD></TD>
];

use constant SUMTAB9 =>  q[       </TR>
       <TR style="background-color:#D9D9F9">
        <TD colspan="2" nowrap><TABLE ALIGN="center" border="0" cellspacing="0" cellpadding="0" summary="fisher" width="100%">
         <TR>
          <TH nowrap>P-value of Fisher's exact test</TH>
          <TD align="right">&nbsp;<A HREF="javascript:window.open('].HL.q[/help/fisherHelp.html','help','width=600,height=500,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
         </TR>
        </TABLE></TD>
];

use constant SUMTAB10 =>  q[        <TD align="right">%.4f</TD>
];

use constant SUMTAB11 =>  q[       </TR>
       <TR style="background-color:#D7DDF1">
        <TD colspan="2" nowrap><TABLE ALIGN="center" border="0" cellspacing="0" cellpadding="0" summary="utest" width="100%%">
         <TR>
          <TH nowrap>P-value of Mann-Whitney U-test</TH>
          <TD align="right">&nbsp;<A HREF="javascript:window.open('].HL.q[/help/utestHelp.html','help','width=650,height=420,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
         </TR>
        </TABLE></TD>
        <TD colspan="%d" ALIGN="center">%.4f</TD>
       </TR>
      </TABLE></TD>
     </TR>
     <TR>
      <TD style="background-color:#EEEEF8"><TABLE border="0" cellspacing="2" cellpadding="3" summary="SD table" style="font-size:small">

       <TR style="background-color:#D1D1E1">
        <TH><A HREF="http://en.wikipedia.org/wiki/Standard_deviation" target="_blank">S.D.</A> and
            <A HREF="http://en.wikipedia.org/wiki/Standard_error_(statistics)" target="_blank">S.E.</A>
            of<BR>percent methylated CpGs</TH>
        <TH>S.D. between CpGs</TH>
        <TH>S.E. between CpGs</TH>
        <TH>S.D. between sequences</TH>
        <TH>S.E. between sequences</TH>
       </TR>
       <TR style="background-color:#DDDDEE">
        <TD>group1</TD>
        <TD align="right">%.1f%%</TD>
        <TD align="right">%.2f%%</TD>
        <TD align="right">%.1f%%</TD>
        <TD align="right">%.2f%%</TD>
       </TR>
       <TR style="background-color:#DDDDEE">
        <TD>group2</TD>
        <TD align="right">%.1f%%</TD>
        <TD align="right">%.2f%%</TD>
        <TD align="right">%.1f%%</TD>
        <TD align="right">%.2f%%</TD>
       </TR>
       <TR style="background-color:#DDDDEE">
        <TD>total</TD>
        <TD align="right">%.1f%%</TD>
        <TD align="right">%.2f%%</TD>
        <TD align="right">%.1f%%</TD>
        <TD align="right">%.2f%%</TD>
       </TR>
       </TABLE></TD>
     </TR>
     <TR style="background-color:#D1D1E1">
      <TD><TABLE border="0" cellspacing="3" cellpadding="2" summary="graph show table">
       <TR>
        <TD><TABLE id="compGraph1" style="display:block" border="0" cellspacing="0" cellpadding="0" summary="graph1 table">
         <TR>
          <TD><IMG SRC="%s" alt="graph1"></TD>
         </TR>
        </TABLE><TABLE id="compGraph2" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph2 table">
         <TR>
          <TD><IMG SRC="%s" alt="graph2"></TD>
         </TR>
        </TABLE><TABLE id="compGraph3" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph3 table">
         <TR>
          <TD><IMG SRC="%s" alt="graph3"></TD>
         </TR>
        </TABLE><TABLE id="compGraph4" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph4 table">
         <TR>
          <TD><IMG SRC="%s" alt="graph4"></TD>
         </TR>
        </TABLE><TABLE id="compGraph5" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph5 table">
         <TR>
          <TD><IMG SRC="%s" alt="graph5"></TD>
         </TR>
        </TABLE><TABLE id="compGraph6" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph6 table">
         <TR>
          <TD><IMG SRC="%s" alt="graph6"></TD>
         </TR>
        </TABLE><TABLE id="compGraph7" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph7 table">
         <TR>
          <TD><IMG SRC="%s" alt="graph7"></TD>
         </TR>
        </TABLE><TABLE id="compGraph8" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph8 table">
         <TR>
          <TD><IMG SRC="%s" alt="graph8"></TD>
         </TR>
        </TABLE></TD>
       </TR>
       <TR>
        <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="graph option table">
         <TR>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="15" height="30" alt="space"></TD>
          <TD><DIV onmousedown="fgraph()" onkeydown="fgraph()" style="cursor: pointer;">
              <IMG id="optImage2" src="].HL.q[/images/icon034.gif" alt="list"><A id="graphes" style="color: blue;text-decoration: underline">&nbsp;Change graph</A></DIV></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="30" height="2" alt="space"></TD>
          <TD valign="bottom"><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD valign="bottom">&nbsp;&nbsp;(file format
           <SELECT NAME="format">
            <OPTION VALUE="PNG" %s>PNG
            <OPTION VALUE="SVG" %s>SVG
            <OPTION VALUE="SVGZ" %s>SVGZ
            </SELECT>&nbsp;<A HREF="javascript:window.open('].HL.q[/help/formatHelp.html','help','width=600,height=420,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A>&nbsp;)</TD>
         </TR>
        </TABLE></TD>
       </TR>
      </TABLE></TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD><IMG src="].HL.q[/images/spacer.gif" width="800" height="2" alt="space"></TD>
   </TR>
   <TR>
    <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="bisulfite information table">
     <TR style="background-color:#F1F1FF">
      <TD colspan="2"><TABLE border="0" cellspacing="0" cellpadding="0" summary="bisulfite information title table">
       <TR>
        <TD><DIV style="font-size:large;font-weight:bold">&nbsp;<IMG width="13" height="13" src="].HL.q[/images/icon034.gif" alt="list">
            Bisulfite sequence information</DIV></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD>&nbsp;<A HREF="javascript:window.open('].HL.q[/help/restoreHelp.html','help','width=650,height=600,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="50" height="2" alt="space"></TD>
        <TD><DIV onmousedown="foption()" onkeydown="foption()" style="cursor: pointer;">
            <IMG id="optImage1" src="].HL.q[/images/icon030.gif" alt="option"><A id="options" style="color: blue;text-decoration: underline">&nbsp;Show options</A></DIV></TD>
       </TR>
      </TABLE></TD>
     </TR>
     <TR style="background-color:#F4F4FF">
      <TD><TABLE border="0" cellspacing="2" cellpadding="0" summary="bisulfite information option table">
       <TR>
        <TD><TABLE id="optionOrder" style="display:none" border="0" cellspacing="2" cellpadding="0" summary="bisulfite information option order table">
         <TR style="background-color:#E7E7F8">
          <TD colspan="2" width="400"><TABLE border="0" cellspacing="0" cellpadding="0" summary="sort top" width="100%%">
           <TR>
            <TD>&nbsp;<IMG src="].HL.q[/images/icon034.gif" alt="list">&nbsp;Sorting conditions
            &nbsp;&nbsp;<A style="font-size:small">(CpH: CpA, CpC, CpT)</A></TD>
            <TD align="right"><A HREF="javascript:window.open('].HL.q[/help/sortHelp.html','help','width=600,height=420,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A>&nbsp;</TD>
           </TR>
          </TABLE></TD>
         </TR>
         <TR>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="1" height="1" alt="space"></TD>
         </TR>
         <TR style="background-color:#D7D7E8">
          <TD><INPUT TYPE="radio" NAME="order" VALUE="1" %s>user specified order</TD>
          <TD><INPUT TYPE="radio" NAME="order" VALUE="2" %s>number of methylated CpGs</TD>
         </TR>
         <TR style="background-color:#D7D7E8">
          <TD><INPUT TYPE="radio" NAME="order" VALUE="3" %s>number of unconverted CpHs</TD>
          <TD><INPUT TYPE="radio" NAME="order" VALUE="4" %s>percent converted CpHs</TD>
         </TR>
         <TR style="background-color:#D7D7E8">
          <TD><INPUT TYPE="radio" NAME="order" VALUE="5" %s>number of mismatches</TD>
          <TD><INPUT TYPE="radio" NAME="order" VALUE="6" %s>percent identity</TD>
         </TR>
         <TR style="background-color:#D7D7E8">
          <TD><INPUT TYPE="radio" NAME="order" VALUE="7" %s>sequence name</TD>
          <TD></TD>
         </TR>
         <TR>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="1" height="1" alt="space"></TD>
         </TR>
         <TR style="background-color:#E7E7F8">
          <TD><INPUT TYPE="radio" NAME="direct" VALUE="1" %s>ascending order</TD>
          <TD><INPUT TYPE="radio" NAME="direct" VALUE="2" %s>descending order</TD>
         </TR>
        </TABLE></TD>
        <TD><TABLE id="optionList" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="bisulfite information options table">
         <TR style="background-color:#D7D7E8">
          <TD width="350">&nbsp;<IMG src="].HL.q[/images/icon034.gif" alt="option">&nbsp;Conditions to exclude low quality sequences</TD>
          <TD align="right"> <A HREF="javascript:window.open('].HL.q[/help/cutoffHelp2.html','help','width=600,height=420,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A>&nbsp;</TD>
         </TR>
         <TR>
          <TD colspan="2"><IMG src="].HL.q[/images/spacer.gif" width="1" height="4" alt="space"></TD>
         </TR>
         <TR style="background-color:#E7E7F8">
          <TD>&nbsp;Upper limit of unconverted CpHs</TD>
          <TD>&nbsp;:&nbsp;<input type="text" NAME="unconv" MAXLENGTH="3" SIZE="3" VALUE="%d"></TD>
         </TR>
         <TR style="background-color:#E7E7F8">
          <TD>&nbsp;Lower limit of percent converted CpHs</TD>
          <TD nowrap>&nbsp;:&nbsp;<input type="text" NAME="pconv" MAXLENGTH="5" SIZE="5" VALUE="%.1f"></TD>
         </TR>
         <TR style="background-color:#E7E7F8">
          <TD>&nbsp;Upper limit of alignment mismatches</TD>
          <TD>&nbsp;:&nbsp;<input type="text" NAME="mis" MAXLENGTH="3" SIZE="3" VALUE="%d"></TD>
         </TR>
         <TR style="background-color:#E7E7F8">
          <TD>&nbsp;Lower limit of percent identity</TD>
          <TD nowrap>&nbsp;:&nbsp;<input type="text" NAME="perc" MAXLENGTH="5" SIZE="5" VALUE="%.1f"></TD>
         </TR>
         <TR>
          <TD colspan="2"><IMG src="].HL.q[/images/spacer.gif" width="1" height="4" alt="space"></TD>
         </TR>
         <TR style="background-color:#E3E3F3">
          <TD colspan="2" align="center" valign="middle" height="30">
           <INPUT TYPE="submit"  onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" NAME="submit" VALUE="%s"></TD>
         </TR>
        </TABLE></TD>
       </TR>
      </TABLE></TD>
     </TR>
     <TR style="background-color:#E9E9F9">
      <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="bisulfite information submit table">
       <TR>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="15" height="30" alt="space"></TD>
        <TD><INPUT TYPE="reset" value="Reset"></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='mali';"    onkeydown="document.allform.target='mali';"    TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD>&nbsp;<A HREF="javascript:window.open('].HL.q[/help/buttonsHelpS.html','help','width=600,height=400,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
       </TR>
      </TABLE></TD>
     </TR>
     <TR>
      <TD><TABLE border="0" cellspacing="2" cellpadding="2" width="100%%" summary="bisulfite information result table">
       <TR style="background-color:#D9D9F9">
        <TH style="font-size:small">group</TH>
        <TH style="font-size:small">No.</TH>

        <TH style="font-size:small" >order<BR>
           <A HREF="javascript:window.open('].HL.q[/help/orderHelp.html','help','width=600,height=200,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TH>
        <TH><A style="font-size:small"> exclude</A><BR>
            <A style="font-size:x-small" HREF="javascript:selectAll()">select all</A><BR>
            <A style="font-size:x-small" HREF="javascript:unselectAll()">unselect all</A><BR>
            <A HREF="javascript:window.open('].HL.q[/help/excludeHelp.html','help','width=600,height=200,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TH>
        <TH style="font-size:small" >Sequence<BR>name</TH>
        <TH style="font-size:small" >mismatch (gap) /<BR>alignment length<BR>(%% identity)</TH>
        <TH style="font-size:small" >Me-CpG<BR>(%%)</TH>
        <TH style="font-size:small" >unconverted<BR>(%% converted)</TH>
        <TH style="font-size:small" >Methylation pattern<BR>(or reason for the exclusion <A HREF="javascript:window.open('].HL.q[/help/reasonHelp.html','help','width=600,height=520,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A>)</TH>
       </TR>
];

use constant TABF1  => q[       <TR style="background-color:%s">
        <TD rowspan="%d" align="right" style="background-color:%s">%d</TD>
];
use constant TABF2  => q[       <TR style="background-color:%s">
];

use constant COLS   => ['#EEEEFF', '#E1E1F1', '#DDD7F1', '#D7DDF1'];

use constant TAB    => q[        <TD align="right"><A HREF="javascript:window.open('%s','alignment','width=700,height=500,resizable,scrollbars').focus();void(0);">%d</A></TD>
        <TD align="right"><INPUT TYPE="text" NAME="ord%d" SIZE="3" VALUE="%d"></TD>
        <TD ALIGN="center"><INPUT TYPE="checkbox" NAME="exc%d" value="%s" %s></TD>
        <TD %s style="font-size:%s">%s</TD>
        <TD align="right" nowrap>%s (%d) / %d (<TT>%s</TT>)</TD>
        <TD align="right">%d (<TT>%s</TT>)</TD>
        <TD align="right">%s (<TT>%s</TT>)</TD>
        <TD style="font-size:small">%s</TD>
       </TR>
];

use constant FOOT   => q[
      </TABLE></TD>
     </TR>
     <TR style="background-color:#E9E9F9">
      <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="bisulfite information submit table2">
       <TR>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="15" height="30" alt="space"></TD>
        <TD><INPUT TYPE="reset" value="Reset"></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
        <TD><INPUT onmousedown="document.allform.target='mali';"    onkeydown="document.allform.target='mali';"    TYPE="submit" NAME="submit" VALUE="%s"></TD>
        <TD>&nbsp;<A HREF="javascript:window.open('].HL.q[/help/buttonsHelpS.html','help','width=600,height=400,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
       </TR>
      </TABLE></TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD><HR></TD>
   </TR>
   <TR>
    <TD align="center" colspan="3">
     <IMG src="].HL.q[/images/spacer.gif" alt="spacer" width="1" height="10">
    </TD>
   </TR>
  </TABLE>
  </FORM>
  <SCRIPT type="text/javascript" language="JavaScript">
  <!--
  checkValue();
%s
  //-->
  </SCRIPT>
 </BODY>
</HTML>
];

use constant SELECTJS => qq[
	document.allform.exc%d.checked = true;];

use constant UNSELECTJS => qq[
	document.allform.exc%d.checked = false;];

use constant OUTFORM  => q["Summary of information"
%s"Length of target genome sequence",%d
"Number of CpGs",%d
"Number of bisulfite sequences (used) (group1)",%d
"Number of bisulfite sequences (excluded) (group1)",%d
"Number of bisulfite sequences (total) (group1)",%d
"Number of bisulfite sequences (used) (group2)",%d
"Number of bisulfite sequences (excluded) (group2)",%d
"Number of bisulfite sequences (total) (group2)",%d

"Condition to exclude low quality sequences"
"Upper limit of unconverted CpHs",%d
"Lower limit of percent converted CpHs","%f%%"
"Upper limit of alignment mismatches",%d
"Lower limit of percent identity","%f%%"

"Methylation status of each CpG site"
"CpG position",%s
"Number of methylated CpGs (group1)",%s
"Number of CpGs (group1)",%s
"ratio of methylation (%%) (group1)",%s
"Number of methylated CpGs (group2)",%s
"Number of CpGs (group2)",%s
"ratio of methylation (%%) (group2)",%s
"Number of methylated CpGs (total)",%s
"Number of CpGs (total)",%s
"ratio of methylation (%%) (total)",%s
"P-value of Fisher's exact test",%s
"P-value of Mann-Whitney U-test",%f
"S.D. of %% methylatied (between CpGs, group1)","%.1f"
"S.E. of %% methylatied (between CpGs, group1)","%.2f"
"S.D. of %% methylatied (between sequences, group1)","%.1f"
"S.E. of %% methylatied (between sequences, group1)","%.2f"
"S.D. of %% methylatied (between CpGs, group2)","%.1f"
"S.E. of %% methylatied (between CpGs, group2)","%.2f"
"S.D. of %% methylatied (between sequences, group2)","%.1f"
"S.E. of %% methylatied (between sequences, group2)","%.2f"
"S.D. of %% methylatied (between CpGs, total)","%.1f"
"S.E. of %% methylatied (between CpGs, total)","%.2f"
"S.D. of %% methylatied (between sequences, total)","%.1f"
"S.E. of %% methylatied (between sequences, total)","%.2f"

"Bisulfite sequence information"
"No.","sequence group","sequence name","mismatches(include gaps)","gaps","alignment length","percent identity","methylated CpGs","percent methylated CpGs","unconverted CpHs","number of CpHs","percent converted CpHs","methylation pattern (U: unmethylated, M: methylated, A,C,G,T,N: mismatch,%s -: gap)"
%s
];

my ($cols);
my ($cgi );
my ($data);
my ($id  );
my ($cchk);
my ($fh  );
my ($gen );
my (@gen );
my ($proj);
my ($grp1);
my ($grp2);
my ($seq );
my ($len );
my ($cpgn);
my (@cpg );
my (@que );
my ($i   );
my ($js1 );
my ($js2 );
my ($num1);
my ($num2);
my ($num3);
my ($num4);
my ($que );
my ($glen);
my ($stt );
my ($stp );
my ($g   );
my (%useq);
my ($ref );
my ($ord );
my (@refs);
my ($pos );
my (@sds1);
my ($sds1);
my ($ses1);
my (@sds2);
my ($sds2);
my ($ses2);
my (@sdst);
my ($sdst);
my ($sest);
my (@sdc1);
my ($sdc1);
my ($sec1);
my (@sdc2);
my ($sdc2);
my ($sec2);
my (@sdct);
my ($sdct);
my ($sect);
my ($j   );
my (%meth);
my (%udat);
my (%tdat);
my ($meth);
my ($chk );
my ($pat );
my ($me  );
my ($num );
my ($max );
my ($wrap);
my ($m   );
my ($mis );
my ($unc );
my ($cpg );
my ($cpgp);
my ($pcon);
my ($out );
my ($perc);
my ($url1);
my ($url2);
my ($tab );
my ($k   );
my (@meth);
my ($opt1);
my ($opt2);
my ($opt3);
my ($val1);
my ($val2);
my ($val3);
my ($val4);
my ($val5);
my ($val6);
my ($val7);
my ($val8);
my ($val9);
my ($valF);
my ($head);
my ($size);
my ($name);
my ($rows);
my ($tab1);
my ($tab2);
my ($tab3);
my ($tab4);
my ($tab5);
my ($fmt1);
my ($fmt2);
my ($fmt3);
my ($conv);
local ($_);
local ($!);
local ($a);
local ($b);

$cols = COLS;
$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;
ipCheck ($data);
$id = $data->{id};

$data->{cpgcheck} = 0
    unless (exists $data->{cpgcheck} && $data->{cpgcheck} eq 'on');

$data->{uniq} = 0
    unless (exists $data->{uniq} && $data->{uniq} eq 'on');

if (exists $data->{submit} && $data->{submit} eq DOWNALID) {
    printf REPALI, $id, $data->{cpgcheck};
    exit;
}

$data->{unconv} = UNCONVL
    unless (exists $data->{unconv} && $data->{unconv} =~ /^\d{1,3}$/);
$data->{pconv}  = PCONVL
    unless (exists $data->{pconv}  && $data->{pconv}   =~ /^\d{1,3}(\.\d+)?$/);
$data->{mis}    = MISL
    unless (exists $data->{mis}    && $data->{mis}    =~ /^\d{1,3}$/);
$data->{perc}   = PERCL
    unless (exists $data->{perc}   && $data->{perc}   =~ /^\d{1,3}(\.\d+)?$/);
$data->{format} ||= 'PNG';
$cchk = $data->{cpgcheck} ?  ' +: not CpG site,' : '';

open $fh, DATADIR . $id
    or errorAndExit ('File access error!', 'File access error!', "File access error : $! : " . DATADIR . $id);

if ($data->{submit} && $data->{submit} eq SAVE) {

    use Compress::Zlib;

    $data->{submit} = RENEW;
    $out  = "QUMA_data_file\n";
    $out .= join '', <$fh>;
    $out .= "=====\t2\n";
    $out .= join '', map {"$_\t$data->{$_}\n"} keys %$data;
    $out = Compress::Zlib::memGzip ($out);
    $size = length $out;
    $name = substr $data->{id}, 0, 12;
    $name .= "_$proj" if ($proj);
    $name .= "_quma_restore_analysis_S.qma";
    print qq{Content-Disposition: attachment; filename="$name"\n};
    print qq{Content-Length: $size\n};
    print qq{Content-Type: application/x-quma\n};
    print qq{Status: 200 OK\n\n};
    print $out;
    exit;
}

chomp ($gen = <$fh>);
@gen = split /\t/, $gen;
shift @gen;
$proj = shift @gen;
$proj ||= '';
$proj =~ y/&;`'"|*?~<>^()[]{}$\\\n\r//d;
$proj =~ s/[^\w-]//g;
$grp1 = shift @gen;
$grp1 ||= '';
$grp2 = shift @gen;
$grp2 ||= '';
shift @gen; # convdir
$seq  = shift @gen;
$len  = length $seq;
$cpgn = shift @gen;
@cpg  = map {++$_} @gen;
chomp (@que = <$fh>);
close $fh;

$i = 0;
$num1 = $num2 = $num3 = $num4 = 0;
$js1 = '';
$js2 = '';

foreach $que (@que) {
    $ref = {};
    @{$ref}{'pos', 'com', 'seq', 'qAli', 'gAli', 'aliLen', 'aliMis', 'perc',
	    'gap', 'menum', 'unc', 'conv', 'pconv', 'val', 'dir', 'gdir', 'stat', 'group'} = split /\t/, $que;

    $ref->{exc} = 0;
    $ref->{exc} = 1 if (exists $data->{'exc' . $ref->{pos}} &&
			$data->{'exc' . $ref->{pos}} eq 'on');

    $ref->{exc} = 0 if (exists $data->{submit} && $data->{submit} eq RSTPARA);

    if (! exists $data->{submit} || $data->{submit} eq RSTPARA) {
	$ref->{exc} = 1 if ($ref->{pconv}  < $data->{pconv});
	$ref->{exc} = 1 if ($ref->{unc}    > $data->{unconv});
	$ref->{exc} = 1 if ($ref->{aliMis} > $data->{mis});
	$ref->{exc} = 1 if ($ref->{perc}   < $data->{perc});
    }

    if ($data->{uniq}) {
	$glen = length $ref->{gAli};

	for ($stt = 0; $stt < $glen; $stt++) {
	    $g = substr $ref->{gAli}, $stt, 1;
	    last unless ($g eq '-');
	}

	for ($stp = $glen - 1; $stp >= 0; $stp--) {
	    $g = substr $ref->{gAli}, $stp, 1;
	    last unless ($g eq '-');
	}

	$ref->{aseq} = substr $ref->{qAli}, $stt, $stp - $stt + 1;
	if (exists $useq{$ref->{group}}->{$ref->{aseq}}) {
	    $ref->{exc} = 1;
	    $ref->{nuniq} = 1;
	}
	$useq{$ref->{group}}->{$ref->{aseq}}++;
    }

    $ord = 'ord' . $ref->{pos};
    if (defined $data->{$ord}) {
        $data->{$ord} =~ s/\D//g;
        $data->{$ord} = 1000000 unless ($data->{$ord} =~ /\d/);
    } else {
        $data->{$ord} = 1000000;
    }

    push @refs, $ref;

    if ($ref->{group} == 1) {
	$num1++;
        $num3++ unless ($ref->{exc});
    } else {
	$num2++;
        $num4++ unless ($ref->{exc});
    }

    $js1 .= sprintf SELECTJS,   $ref->{pos};
    $js2 .= sprintf UNSELECTJS, $ref->{pos};
}

if (exists $data->{submit} && $data->{submit} eq RSTPARA) {
    $data->{order} = 0;
    $data->{direct} = 1;
}

if (!$data->{order} || $data->{order} == 2) {

    @refs = sort {$a->{menum} <=> $b->{menum} || $a->{val} cmp $b->{val}} @refs;
    $data->{order} = 1 unless ($data->{order});

} elsif ($data->{order} == 1) {

    @refs = sort {$data->{'ord'. $a->{pos}} <=> $data->{'ord'.$b->{pos}}} @refs;

} elsif ($data->{order} == 3) {

    @refs = sort {$a->{unc} <=> $b->{unc}} @refs;

} elsif ($data->{order} == 4) {

    @refs = sort {$a->{pconv} <=> $b->{pconv}} @refs;

} elsif ($data->{order} == 5) {

    @refs = sort {$a->{aliMis} <=> $b->{aliMis}} @refs;

} elsif ($data->{order} == 6) {

    @refs = sort {$a->{perc} <=> $b->{perc}} @refs;

} elsif ($data->{order} == 7) {

     @refs = sort {htmlSunitize($a->{com}) cmp htmlSunitize($b->{com})} @refs;

} else {

    @refs = sort {$a->{menum} <=> $b->{menum} || $a->{val} cmp $b->{val}} @refs;
    $data->{order} = 1;
}

if (exists $data->{direct} && $data->{direct} == 2) {
    @refs = reverse @refs;
    $data->{direct} = 1 if ($data->{order} == 1);

} else {
    $data->{direct} = 1;
}

@refs = sort {$a->{group} <=> $b->{group} || $a->{exc} <=> $b->{exc}} @refs;

$pos = join ',', map {$_->{pos}} grep {$_->{'exc'} == 0} @refs;

if (exists $data->{submit} && $data->{submit} eq MALI) {
    printf SHOWMALI, $id, $pos, $data->{cpgcheck};
    exit;
}

for ($j = 1; $j <= $cpgn; $j++) {

    $meth{$j}->{total}   = 0;
    $meth{$j}->{unmeth}  = 0;
    $meth{$j}->{meth}    = 0;
    $meth{$j}->{ng}      = 0;

    $meth{$j}->{total1}  = 0;
    $meth{$j}->{unmeth1} = 0;
    $meth{$j}->{meth1}   = 0;
    $meth{$j}->{ng1}     = 0;

    $meth{$j}->{total2}  = 0;
    $meth{$j}->{unmeth2} = 0;
    $meth{$j}->{meth2}   = 0;
    $meth{$j}->{ng2}     = 0;
}

$udat{1} = [];
$udat{2} = [];
$tdat{1} = {};
$tdat{2} = {};
$tdat{1}->{total} = 0;
$tdat{1}->{me}    = 0;
$tdat{2}->{total} = 0;
$tdat{2}->{me}    = 0;
$tdat{total} = 0;
$tdat{me}    = 0;
$max  = length htmlSunitize ((sort {length htmlSunitize $b->{com} <=> length htmlSunitize $a->{com}} @refs)[0]->{com});
$wrap = $max > FONTWRP ? '' : 'nowrap';
$max  = $max > FONTXXS ? 'xx-small' :
        $max > FONTXS  ? 'x-small'  : 
        $max > FONTS   ? 'small'    :
                         'medium'   ;
foreach $ref (@refs) {

    $meth = $ref->{gdir} == 1 ? reverse $ref->{val} : $ref->{val};

    $chk = '';
    $pat = '';
    
    if ($ref->{exc}) {
	$chk = 'checked';

    } else {

	for ($me = $num = 0, $j = 1; $j <= $cpgn; $j++) {

            $m = chop $meth;

	    if ($m eq '0') {
		$meth{$j}->{total}++;
		$meth{$j}->{unmeth}++;
		$meth{$j}->{'total' . $ref->{group}}++;
		$meth{$j}->{'unmeth' . $ref->{group}}++;
		$num++;
		$pat .= 'U';

	    } elsif ($m eq '1') {

		$meth{$j}->{total}++;
		$meth{$j}->{meth}++;
		$meth{$j}->{'total' . $ref->{group}}++;
		$meth{$j}->{'meth' . $ref->{group}}++;
		$num++;
		$me++;
		$pat .= 'M';

	    } else {
		$meth{$j}->{ng}++;
		$meth{$j}->{'ng' . $ref->{group}}++;
	        $m =~ y/MRWSYKVHDB/mrwsykvhdb/;
		$pat .= $m;
	    }
	}
        $tdat{$ref->{group}}->{total} += $num;
        $tdat{$ref->{group}}->{me}    += $me;
        $tdat{total} += $num;
        $tdat{me}    += $me;
	push @{$udat{$ref->{group}}}, $num ? $me/$num : 0;
    }

    $mis = $ref->{aliMis};
    $unc = "$ref->{unc}/" . ($ref->{unc} + $ref->{conv});

    $pat ||= 'excluded';
    $cpg  = $ref->{val} =~ y/01//;
    $cpgp = $cpg ? 100 * $ref->{menum} / $cpg : 0;

    if ($ref->{group} == 1) {
        push @sds1, $cpgp unless ($ref->{exc});
    } else {
        push @sds2, $cpgp unless ($ref->{exc});
    }
    push @sdst, $cpgp unless ($ref->{exc});

    $cpgp = sprintf "%5.1f", $cpgp;

    $out .= join ',', ($i+1, $ref->{group}, qq{"$ref->{com}"}, $mis, $ref->{gap},
		       $ref->{aliLen}, $ref->{perc}, $ref->{menum}, $cpgp,
		       $ref->{unc}, $ref->{unc} + $ref->{conv}, $ref->{pconv}, qq{="$pat"});
    $out .= "\n";

    $mis = qq{<A STYLE="COLOR:#FF00FF">$mis</A>}   if ($ref->{aliMis} > $data->{mis});
    $cpgp =~ s/ /&nbsp;/g;
    $perc = sprintf "%5.1f", $ref->{perc};
    $perc =~ s/ /&nbsp;/g;
    $perc = qq{<A STYLE="COLOR:#FF00FF">$perc</A>} if ($ref->{perc}   < $data->{perc});
    $unc = qq{<A STYLE="COLOR:#FF00FF">$unc</A>}   if ($ref->{unc}    > $data->{unconv});
    $pcon = sprintf "%5.1f", $ref->{pconv};
    $pcon =~ s/ /&nbsp;/g;
    $pcon = qq{<A STYLE="COLOR:#FF00FF">$pcon</A>} if ($ref->{pconv}  < $data->{pconv});

    $url1 = sprintf DATAURL, $id, $ref->{pos}, $data->{cpgcheck};

    if ($ref->{exc}) {

        $url2 = '';
        $url2 .= 'mismatch, ' if ($ref->{aliMis} > $data->{mis});
        $url2 .= '% ident, '  if ($ref->{perc}   < $data->{perc});
        $url2 .= 'unconv, '   if ($ref->{unc}    > $data->{unconv});
        $url2 .= '% conv, '   if ($ref->{pconv}  < $data->{pconv});
	$url2 .= 'multiple, ' if (exists $ref->{nuniq});

        if ($url2) {
            chop $url2;
            chop $url2;
        } else {
            $url2 = 'user desired';
        }

    } else {
	$url2 = qq{<IMG SRC="} . (sprintf SGLURL,  $id, $ref->{pos}) . qq{" alt="methfig">};
    }

    $i++;

    if ($i == 1) {
	$tab .= sprintf TABF1, $cols->[$i%2], $num1, $cols->[2], 1;
    } elsif ($i == $num1 + 1) {
	$tab .= sprintf TABF1, $cols->[$i%2], $num2, $cols->[3], 2;
    } else {
        $tab .= sprintf TABF2, $cols->[$i%2];
    }

    $k = $i;
    $k = $i - $num1 if ($i > $num1);

    $tab .= sprintf TAB, $url1, $i, $ref->{pos}, $k, $ref->{pos}, 'on', $chk,
			 $wrap, $max, htmlSunitize($ref->{com}), 
                         $mis, $ref->{gap}, $ref->{aliLen},
			 $perc, $ref->{menum}, $cpgp, $unc, $pcon, $url2;

}

@meth = @meth{1..$cpgn};
$opt1 = join (',', @cpg);
$opt2 = join (',', map {"$_->{meth1}%7c$_->{total1}"} @meth);
$opt3 = join (',', map {"$_->{meth2}%7c$_->{total2}"} @meth);

$url1 = sprintf COMPOPT, ($id, $len, $opt1, $opt2, $opt3);

if (exists $data->{submit} && $data->{submit} eq DOWNCPGG) {
    $url2 = $data->{graphShow} == 0 ? REPCOMP1 :
	    $data->{graphShow} == 1 ? REPCOMP2 :
	    $data->{graphShow} == 2 ? REPCOMP3 :
	    $data->{graphShow} == 3 ? REPCOMP4 :
	    $data->{graphShow} == 4 ? REPCOMP5 :
	    $data->{graphShow} == 5 ? REPCOMP6 :
	    $data->{graphShow} == 6 ? REPCOMP7 :
	                              REPCOMP8 ;
    printf $url2, $id, $len, $opt1, $opt2, $opt3, $proj, $data->{format};
    exit;
}

@sdc1 = map {$_->{total1} ? 100 * $_->{meth1}/$_->{total1} : 0} @meth;
@sdc2 = map {$_->{total2} ? 100 * $_->{meth2}/$_->{total2} : 0} @meth;
@sdct = map {$_->{total}  ? 100 * $_->{meth} /$_->{total}  : 0} @meth;

$sds1 = @sds1 ? stddev @sds1 : 0;
$sds2 = @sds2 ? stddev @sds2 : 0;
$sdst = @sdst ? stddev @sdst : 0;
$sdc1 = @sdc1 ? stddev @sdc1 : 0;
$sdc2 = @sdc2 ? stddev @sdc2 : 0;
$sdct = @sdct ? stddev @sdct : 0;

$ses1 = $sds1 / sqrt(@sds1 || 1);
$ses2 = $sds2 / sqrt(@sds2 || 1);
$sest = $sdst / sqrt(@sdst || 1);
$sec1 = $sdc1 / sqrt($cpgn || 1);
$sec2 = $sdc2 / sqrt($cpgn || 1);
$sect = $sdct / sqrt($cpgn || 1);

$ref = {};

if (exists $data->{submit} && $data->{submit} eq DOWNSTATD) {

    $val1 = join (',', map {$_->{meth1} } @meth);
    $val2 = join (',', map {$_->{total1}} @meth);
    $val3 = join (',', map {sprintf "%.1f", $_} @sdc1);
    $val4 = join (',', map {$_->{meth2} } @meth);
    $val5 = join (',', map {$_->{total2}} @meth);
    $val6 = join (',', map {sprintf "%.1f", $_} @sdc2);
    $val7 = join (',', map {$_->{meth}  } @meth);
    $val8 = join (',', map {$_->{total} } @meth);
    $val9 = join (',', map {sprintf "%.1f", $_} @sdct);

    $valF = join (',', map {fisherExactTest($ref, $_->{meth1},$_->{unmeth1},$_->{meth2},$_->{unmeth2})} @meth);

    $opt1 .=  q{,"Total"};
    $val1 .= qq{,$tdat{1}->{me}};
    $val2 .= qq{,$tdat{1}->{total}};
    $val3 .=  q{,}.($tdat{1}->{total} ? 100 * $tdat{1}->{me} / $tdat{1}->{total} : 0);
    $val4 .= qq{,$tdat{2}->{me}};
    $val5 .= qq{,$tdat{2}->{total}};
    $val6 .=  q{,}.($tdat{2}->{total} ? 100 * $tdat{2}->{me} / $tdat{2}->{total} : 0);
    $val7 .= qq{,$tdat{me}};
    $val8 .= qq{,$tdat{total}};
    $val9 .=  q{,}.($tdat{total} ? 100 * $tdat{me} / $tdat{total} : 0);
    $valF .=  q{,}.fisherExactTest($ref,
                                   $tdat{1}->{me}, $tdat{1}->{total} - $tdat{1}->{me},
				   $tdat{2}->{me}, $tdat{2}->{total} - $tdat{2}->{me});
    $head  = '';
    $proj =~ s/"//g;
    $head .= qq{"Project name","$proj"\n} if ($proj);
    $grp1 =~ s/"//g;
    $grp2 =~ s/"//g;
    $head .= qq{"Sequence group name 1","$grp1"\n"Sequence group name 2","$grp2"\n} if ($grp1 && $grp2);
    $out = sprintf OUTFORM, $head, $len, $cpgn,
                            $num3, $num1 - $num3 ,$num1,
                            $num4, $num2 - $num4, $num2,
                            $data->{unconv}, $data->{pconv}, $data->{mis}, $data->{perc},
                            $opt1,
		            $val1, $val2, $val3,
		            $val4, $val5, $val6,
		            $val7, $val8, $val9,
                            $valF,
                            (@{$udat{1}} && @{$udat{2}} ? uTest($udat{1}, $udat{2}) : 1),
                            $sdc1, $sec1, $sds1, $ses1,
                            $sdc2, $sec2, $sds2, $ses2,
                            $sdct, $sect, $sdst, $sest,
		            $cchk, $out;
    $size  = length $out;
    $name  = substr $data->{id}, 0, 12;
    $name .= "_$proj" if ($proj);
    $name .= "_quma_stat_data.csv";

    print qq{Content-Disposition: attachment; filename="$name"\n};
    print qq{Content-Length: $size\n};
    print qq{Content-Type: text/csv\n};
    print qq{Status: 200 OK\n\n};
    print $out;
    exit;
}

$proj = htmlSunitize ($proj) if ($proj);
$grp1 = htmlSunitize ($grp1) if ($grp1);
$grp2 = htmlSunitize ($grp2) if ($grp2);
$val1  = 5;
$val2  = '';
$val3  = '';
$val4  = '';
$val1++ if ($proj);
$val2 .= qq{      <TH rowspan="2">Project<BR>name</TH>\n} if ($proj);
$val4 .= qq{      <TD align="center">$proj</TD>\n} if ($proj);
$val1++ if ($grp1 && $grp2);

$val2 .= qq{      <TH colspan="2">sequence<BR>group name</TH>\n} if ($grp1 && $grp2);
$val3 .= qq{      <TH>group1</TH>\n      <TH>group2</TH>\n} if ($grp1 && $grp2);
$val4 .= qq{      <TD align="center">$grp1</TD>\n      <TD align="center">$grp2</TD>\n} if ($grp1 && $grp2);

$data->{graphShow}  ||= 0;
$data->{optionShow} ||= 0;
printf HEAD, $js1, $js2, STAT, $id, $data->{optionShow}, $data->{graphShow}, $data->{cpgcheck}, $data->{uniq},
	     $val1, $val2, $val3, $val4, $len, $cpgn, $num3, $num1 - $num3,
	     $num1, $num4, $num2 - $num4, $num2;

$num = int (($cpgn + 1)/ CPGROWL2) + 1;
$rows = int (($cpgn + 1)/$num);
$rows++ if ($cpgn + 1 - $rows * $num);

print  SUMTAB1;

for ($i = 0; $i < $rows * $num - 1; $i++) {
    if ($i && ! ($i % $rows)) {
         print $tab1.SUMTAB3.
               sprintf(SUMTAB4,'group1').$tab2.
               sprintf(SUMTAB6,'#D8D8E7').
               sprintf(SUMTAB4,'group2').$tab3.
               sprintf(SUMTAB6,'#E3E3F1').
               sprintf(SUMTAB4,'total' ).
               $tab4.SUMTAB9.$tab5.SUMTAB7;
         $tab1 = $tab2 = $tab3 = $tab4 = $tab5 = '';
    }

    if ($i > @cpg - 1) {
         $tab1 .= SUMTAB8;
         $tab2 .= SUMTAB8;
         $tab3 .= SUMTAB8; 
         $tab4 .= SUMTAB8;
         $tab5 .= SUMTAB8;
         next;
    }

    $tab1 .= sprintf SUMTAB2, $cpg[$i];
    $tab2 .= sprintf SUMTAB5, ($meth{$i+1}->{meth1}, $meth{$i+1}->{total1},
                               ($meth{$i+1}->{total1} ? 100 * $meth{$i+1}->{meth1}/$meth{$i+1}->{total1} : 0));
    $tab3 .= sprintf SUMTAB5, ($meth{$i+1}->{meth2}, $meth{$i+1}->{total2},
                               ($meth{$i+1}->{total2} ? 100 * $meth{$i+1}->{meth2}/$meth{$i+1}->{total2} : 0));
    $tab4 .= sprintf SUMTAB5, ($meth{$i+1}->{meth}, $meth{$i+1}->{total},
                               ($meth{$i+1}->{total} ? 100 * $meth{$i+1}->{meth}/$meth{$i+1}->{total} : 0));
    $tab5 .= sprintf SUMTAB10, fisherExactTest ($ref,
                                                $meth{$i+1}->{meth1}, $meth{$i+1}->{unmeth1},
                                                $meth{$i+1}->{meth2}, $meth{$i+1}->{unmeth2});
}

$tab1 .= sprintf SUMTAB2, 'Total';
$tab2 .= sprintf SUMTAB5, ($tdat{1}->{me}, $tdat{1}->{total}, $tdat{1}->{total} ? 100 * $tdat{1}->{me} / $tdat{1}->{total} : 0);
$tab3 .= sprintf SUMTAB5, ($tdat{2}->{me}, $tdat{2}->{total}, $tdat{2}->{total} ? 100 * $tdat{2}->{me} / $tdat{2}->{total} : 0);
$tab4 .= sprintf SUMTAB5, ($tdat{me}, $tdat{total}, $tdat{total} ? 100 * $tdat{me} / $tdat{total} : 0);
$tab5 .= sprintf SUMTAB10, fisherExactTest ($ref,
                                            $tdat{1}->{me}, $tdat{1}->{total} - $tdat{1}->{me},
                                            $tdat{2}->{me}, $tdat{2}->{total} - $tdat{2}->{me});

print $tab1.SUMTAB3.
      sprintf(SUMTAB4,'group1').$tab2.
      sprintf(SUMTAB6,'#D8D8E7').
      sprintf(SUMTAB4,'group2').$tab3.
      sprintf(SUMTAB6,'#E3E3F1').
      sprintf (SUMTAB4,'total' ).
      $tab4.SUMTAB9.$tab5;

$fmt1 = $fmt2 = $fmt3 = '';

if ($data->{format} eq 'SVG') {
    $fmt2 = 'SELECTED';
} elsif ($data->{format} eq 'SVGZ') {
    $fmt3 = 'SELECTED';
} else {
    $fmt1 = 'SELECTED';
}

printf SUMTAB11, ($rows, @{$udat{1}} && @{$udat{2}} ? uTest($udat{1}, $udat{2}) : 1,
                  $sdc1, $sec1, $sds1, $ses1,
                  $sdc2, $sec2, $sds2, $ses2,
                  $sdct, $sect, $sdst, $sest,
                  COMPFIG1.$url1, COMPFIG2.$url1,
                  COMPFIG3.$url1, COMPFIG4.$url1,
                  COMPFIG5.$url1, COMPFIG6.$url1,
		  COMPFIG7.$url1, COMPFIG8.$url1,
                  DOWNCPGG,
                  $fmt1, $fmt2, $fmt3,
                  SAVE,
                  $data->{order}  == 1 ? 'checked' : '',
                  $data->{order}  == 2 ? 'checked' : '',
                  $data->{order}  == 3 ? 'checked' : '',
                  $data->{order}  == 4 ? 'checked' : '',
                  $data->{order}  == 5 ? 'checked' : '',
                  $data->{order}  == 6 ? 'checked' : '',
                  $data->{order}  == 7 ? 'checked' : '',
                  $data->{direct} == 1 ? 'checked' : '',
                  $data->{direct} == 2 ? 'checked' : '',
                  $data->{unconv}, $data->{pconv}, $data->{mis}, $data->{perc}, RSTPARA,
                  RENEW, DOWNSTATD, DOWNALID, MALI);

$conv = $data->{conv} ? '    alert("' . CONVER. '")' : '';
print  $tab;
printf FOOT, RENEW, DOWNSTATD, DOWNALID, MALI, $conv;

###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
