#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeBiFig.cgi                                                  *
#_* cgi for creating methylation analysis result page                         *
#_* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
#_* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
#_*                                                                           *
#_* 2008/02/20 First open source version                                      *
#_* 2008/03/31 "unselect all" link is added                                   *
#_* 2008/04/02 new sorting option "sequence name" is added                    *
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
  <TITLE>Results of bisulfite sequencing analysis</TITLE>

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
	    document.allform.graphShow.value = 5;
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
	   document.getElementById("optImage").src = "].HL.q[/images/icon033.gif";
	   newText = document.createTextNode(" Hide options");
           document.allform.optionShow.value = "1";

         } else {
           document.getElementById("optionList").style.display = "none";
           document.getElementById("optionOrder").style.display = "none";
	   document.getElementById("optImage").src = "].HL.q[/images/icon030.gif";
	   newText = document.createTextNode(" Show options");
           document.allform.optionShow.value = "0";
	 }

         optionAnc.appendChild(newText);

       } else if (browser == "IE46") {
         if (document.allform.optionShow.value == 0) {
           optionList.style.display = "block";
           optionOrder.style.display = "block";
           document.images[17].src = "].HL.q[/images/icon033.gif";
	   options.innerText = " Hide options";
           document.allform.optionShow.value = "1";

         } else {
           optionList.style.display= "none";
           optionOrder.style.display = "none";
           document.images[17].src = "].HL.q[/images/icon030.gif";
	   options.innerText = " Show options";
           document.allform.optionShow.value = "0";
         }
       }
    }

    function fgraph () {
       if (browser == "IE56NN6") {

         if (document.allform.graphShow.value == 0) {
	   document.getElementById("methGraph1").style.display = "none";
	   document.getElementById("methGraph2").style.display = "block";
	   document.getElementById("methGraph3").style.display = "none";
	   document.getElementById("methGraph4").style.display = "none";
	   document.getElementById("methGraph5").style.display = "none";
	   document.getElementById("methGraph6").style.display = "none";
           document.allform.graphShow.value = 1;

         } else if (document.allform.graphShow.value == 1) {
	   document.getElementById("methGraph1").style.display = "none";
	   document.getElementById("methGraph2").style.display = "none";
	   document.getElementById("methGraph3").style.display = "block";
	   document.getElementById("methGraph4").style.display = "none";
	   document.getElementById("methGraph5").style.display = "none";
	   document.getElementById("methGraph6").style.display = "none";
           document.allform.graphShow.value = 2;

         } else if (document.allform.graphShow.value == 2) {
	   document.getElementById("methGraph1").style.display = "none";
	   document.getElementById("methGraph2").style.display = "none";
	   document.getElementById("methGraph3").style.display = "none";
	   document.getElementById("methGraph4").style.display = "block";
	   document.getElementById("methGraph5").style.display = "none";
	   document.getElementById("methGraph6").style.display = "none";
           document.allform.graphShow.value = 3;

         } else if (document.allform.graphShow.value == 3) {
	   document.getElementById("methGraph1").style.display = "none";
	   document.getElementById("methGraph2").style.display = "none";
	   document.getElementById("methGraph3").style.display = "none";
	   document.getElementById("methGraph4").style.display = "none";
	   document.getElementById("methGraph5").style.display = "block";
	   document.getElementById("methGraph6").style.display = "none";
           document.allform.graphShow.value = 4;

         } else if (document.allform.graphShow.value == 4) {
	   document.getElementById("methGraph1").style.display = "none";
	   document.getElementById("methGraph2").style.display = "none";
	   document.getElementById("methGraph3").style.display = "none";
	   document.getElementById("methGraph4").style.display = "none";
	   document.getElementById("methGraph5").style.display = "none";
	   document.getElementById("methGraph6").style.display = "block";
           document.allform.graphShow.value = 5;

         } else {
	   document.getElementById("methGraph1").style.display = "block";
	   document.getElementById("methGraph2").style.display = "none";
	   document.getElementById("methGraph3").style.display = "none";
	   document.getElementById("methGraph4").style.display = "none";
	   document.getElementById("methGraph5").style.display = "none";
	   document.getElementById("methGraph6").style.display = "none";
           document.allform.graphShow.value = 0;
	 }

       } else if (browser == "IE46") {
         if (document.allform.graphShow.value == 0) {
           methGraph1.style.display = "none";
           methGraph2.style.display = "block";
           methGraph3.style.display = "none";
           methGraph4.style.display = "none";
           methGraph5.style.display = "none";
           methGraph6.style.display = "none";
           document.allform.graphShow.value = 1;

         } else if (document.allform.graphShow.value == 1) {
           methGraph1.style.display = "none";
           methGraph2.style.display = "none";
           methGraph3.style.display = "block";
           methGraph4.style.display = "none";
           methGraph5.style.display = "none";
           methGraph6.style.display = "none";
           document.allform.graphShow.value = 2;

         } else if (document.allform.graphShow.value == 2) {
           methGraph1.style.display = "none";
           methGraph2.style.display = "none";
           methGraph3.style.display = "none";
           methGraph4.style.display = "block";
           methGraph5.style.display = "none";
           methGraph6.style.display = "none";
           document.allform.graphShow.value = 3;

         } else if (document.allform.graphShow.value == 3) {
           methGraph1.style.display = "none";
           methGraph2.style.display = "none";
           methGraph3.style.display = "none";
           methGraph4.style.display = "none";
           methGraph5.style.display = "block";
           methGraph6.style.display = "none";
           document.allform.graphShow.value = 4;

         } else if (document.allform.graphShow.value == 4) {
           methGraph1.style.display = "none";
           methGraph2.style.display = "none";
           methGraph3.style.display = "none";
           methGraph4.style.display = "none";
           methGraph5.style.display = "none";
           methGraph6.style.display = "block";
           document.allform.graphShow.value = 5;

         } else {
           methGraph1.style.display = "block";
           methGraph2.style.display = "none";
           methGraph3.style.display = "none";
           methGraph4.style.display = "none";
           methGraph5.style.display = "none";
           methGraph6.style.display = "none";
           document.allform.graphShow.value = 0;
         }
       }
    }

    function checkResub() {

        if (! document.resub.biseq1.value) {
	    alert ("Please select file of bisulfite sequences!");
	    document.resub.biseq1.focus();
	    return false;
        }
        return true;
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
    Results of bisulfite sequencing analysis
    </TD>
   </TR>
   <TR style="background-color:#3333CC">
    <TD><IMG src="].HL.q[/images/spacer.gif" width="800" height="5" alt="space"></TD>
   </TR>
  </TABLE>
  <BR>
  <TABLE ALIGN="left" border="0" cellspacing="0" cellpadding="0" summary="form table">
   <TR>
    <TD><FORM ACTION="%s" method="post" target="downner" name="allform"
     ><INPUT TYPE="hidden" NAME="id" VALUE="%s"
     ><INPUT TYPE="hidden" NAME="optionShow" VALUE="%s"
     ><INPUT TYPE="hidden" NAME="graphShow" VALUE="%d"
     ><INPUT TYPE="hidden" NAME="cpgcheck" VALUE="%s"
     ><INPUT TYPE="hidden" NAME="uniq" VALUE="%s"
     ><TABLE ALIGN="left" border="0" cellspacing="0" cellpadding="0" summary="overall table">
     <TR>
      <TD><TABLE border="0" cellspacing="3" cellpadding="3" summary="summary information table">
       <TR style="background-color:#F3F3FF">
        <TD colspan="%d"><DIV style="font-size:large;font-weight:bold">&nbsp;<IMG width="13" height="13" src="].HL.q[/images/icon034.gif" alt="list">&nbsp;
         Summary of information</DIV></TD>
       </TR>
       <TR style="background-color:#E7E7F8">
%s        <TH>Length of target<BR>genome sequence</TH>
        <TH>Number of CpGs</TH>
        <TH>Number of bisulfite sequences<BR>(used / excluded / total)</TH>
       </TR>
       <TR style="background-color:#EEEEFF">
%s        <TD align="right">%d</TD>
        <TD align="right">%d</TD>
        <TD align="right">%d / %d / %d</TD>
       </TR>
      </TABLE></TD>
     </TR>
     <TR>
      <TD><IMG src="].HL.q[/images/spacer.gif" width="800" height="2" alt="space"></TD>
     </TR>
     <TR>
      <TD><TABLE border="0" cellspacing="4" cellpadding="3" summary="methylation status table">
       <TR style="background-color:#E3E3F1">
        <TD><DIV style="font-size:large;font-weight:bold">&nbsp;<IMG width="13" height="13" src="].HL.q[/images/icon034.gif" alt="list">
        Methylation status of each CpG site</DIV></TD>
       </TR>
       <TR>
        <TD style="background-color:#EEEEF8"><TABLE border="0" cellspacing="2" cellpadding="3" summary="methylation status each table" style="font-size:small">
];

use constant SUMTAB1 =>  q[         <TR style="background-color:#D1D1E1">
          <TH>CpG position</TH>
];

use constant SUMTAB2 =>  q[          <TH ALIGN="right">%s</TH>
];
use constant SUMTAB3 =>  q[         </TR>
         <TR style="background-color:#DDDDEE">
          <TH>Me-CpG</TH>
];
use constant SUMTAB4 =>  q[          <TD ALIGN="right">%d/%d<BR>%.1f%%</TD>
];
use constant SUMTAB5 =>  q[         </TR>
];
use constant SUMTAB6 =>  q[         <TR>
          <TD></TD>
         </TR>
         <TR style="background-color:#D1D1E1">
          <TH>CpG position</TH>
];

use constant SUMTAB7 =>  q[          <TD></TD>
];
use constant SUMTAB8 =>  q[        </TABLE></TD>
       </TR>
       <TR>
        <TD style="background-color:#EEEEF8"><TABLE border="0" cellspacing="2" cellpadding="3" summary="SD table" style="font-size:small">
         <TR style="background-color:#D1D1E1">
          <TH rowspan="2"><A HREF="http://en.wikipedia.org/wiki/Standard_deviation" target="_blank">S.D.</A> and
                          <A HREF="http://en.wikipedia.org/wiki/Standard_error_(statistics)" target="_blank">S.E.</A>
                          of<BR>percent methylated CpGs</TH>
          <TH>S.D. between CpGs</TH>
          <TH>S.E. between CpGs</TH>
          <TH>S.D. between sequences</TH>
          <TH>S.E. between sequences</TH>
         </TR>
         <TR style="background-color:#DDDDEE">
          <TD align="right">%.1f%%</TD>
          <TD align="right">%.2f%%</TD>
          <TD align="right">%.1f%%</TD>
          <TD align="right">%.2f%%</TD>
         </TR>
        </TABLE></TD>
       </TR>
       <TR style="background-color:#D1D1E1">
        <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="graph show table">
         <TR>
          <TD><TABLE id="methGraph1" style="display:block" border="0" cellspacing="0" cellpadding="0" summary="graph1 table">
           <TR>
            <TD><IMG SRC="%s" alt="graph1"></TD>
           </TR>
          </TABLE><TABLE id="methGraph2" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph2 table">
           <TR>
            <TD><IMG SRC="%s" alt="graph2"></TD>
           </TR>
          </TABLE><TABLE id="methGraph3" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph3 table">
           <TR>
            <TD><IMG SRC="%s" alt="graph3"></TD>
           </TR>
          </TABLE><TABLE id="methGraph4" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph4 table">
           <TR>
            <TD><IMG SRC="%s" alt="graph4"></TD>
           </TR>
          </TABLE><TABLE id="methGraph5" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph5 table">
           <TR>
            <TD><IMG SRC="%s" alt="graph5"></TD>
           </TR>
          </TABLE><TABLE id="methGraph6" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="graph6 table">
           <TR>
            <TD><IMG SRC="%s" alt="graph6"></TD>
           </TR>
          </TABLE></TD>
         </TR>
         <TR>
          <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="graph option table">
           <TR>
            <TD><IMG src="].HL.q[/images/spacer.gif" width="15" height="30" alt="space"></TD>
            <TD><DIV onmousedown="fgraph()" onkeydown="fgraph()" style="cursor: pointer;">
                <IMG src="].HL.q[/images/icon034.gif" alt="list"><A
                 style="color: blue;text-decoration: underline">&nbsp;Change graph</A></DIV></TD>
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
];
use constant TABH    =>  q[     <TR>
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
          <TD><IMG src="].HL.q[/images/spacer.gif" width="40" height="2" alt="space"></TD>
          <TD><DIV onmousedown="foption()" onkeydown="foption()" style="cursor: pointer;">
              <IMG id="optImage" src="].HL.q[/images/icon030.gif" alt="option"><A
               id="options" style="color: blue;text-decoration: underline">&nbsp;Show options</A></DIV></TD>
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
            <TD align="right"><A HREF="javascript:window.open('].HL.q[/help/cutoffHelp2.html','help','width=600,height=420,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A>&nbsp;</TD>
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
          <TD><INPUT onmousedown="document.allform.target='figswin';" onkeydown="document.allform.target='figswin';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='mali';"    onkeydown="document.allform.target='mali';"    TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD>&nbsp;<A HREF="javascript:window.open('].HL.q[/help/buttonsHelp.html','help','width=600,height=500,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
         </TR>
        </TABLE></TD>
       </TR>
       <TR>
        <TD><TABLE border="0" cellspacing="2" cellpadding="2" width="100%%" summary="bisulfite information result table">
         <TR style="background-color:#D9D9F9">
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

use constant TAB    => q[         <TR style="background-color:%s">
          <TD align="right"><A HREF="javascript:window.open('%s','alignment','width=700,height=500,resizable,scrollbars').focus();void(0);">%d</A></TD>
          <TD align="right"><INPUT TYPE="text" NAME="ord%d" SIZE="3" VALUE="%d"></TD>
          <TD ALIGN="center"><INPUT TYPE="checkbox" NAME="exc%d" value="%s" %s></TD>
          <TD %s style="font-size:%s">%s</TD>
          <TD align="right" nowrap>%s (%d) / %d (<TT>%s</TT>)</TD>
          <TD align="right">%d (<TT>%s</TT>)</TD>
          <TD align="right">%s (<TT>%s</TT>)</TD>
          <TD>%s</TD>
         </TR>
];

use constant COLS   => ['#F1F1FF', '#CFCFF3'];

use constant FOOT   => q[        </TABLE></TD>
       </TR>
       <TR style="background-color:#E9E9F9">
        <TD colspan="2"><TABLE border="0" cellspacing="0" cellpadding="0" summary="bisulfite information submit2 table">
         <TR>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT TYPE="reset" value="Reset"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='figswin';" onkeydown="document.allform.target='figswin';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='downner';" onkeydown="document.allform.target='downner';" TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
          <TD><INPUT onmousedown="document.allform.target='mali';"    onkeydown="document.allform.target='mali';"    TYPE="submit" NAME="submit" VALUE="%s"></TD>
          <TD>&nbsp;<A HREF="javascript:window.open('].HL.q[/help/buttonsHelp.html','help','width=600,height=500,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
          <TD><IMG src="].HL.q[/images/spacer.gif" width="10" height="30" alt="space"></TD>
         </TR>
        </TABLE></TD>
       </TR>
      </TABLE></TD>
     </TR>
    </TABLE></FORM></TD>
   </TR>
   <TR>
    <TD><FORM onSubmit="if(checkResub()){return true;}else{return false;}" ACTION="%s"
         ENCTYPE="multipart/form-data" METHOD="POST" target="downner" name="resub"
        ><INPUT TYPE="hidden" NAME="id" VALUE="%s"
        ><INPUT TYPE="hidden" NAME="unconv" VALUE="%d"
        ><INPUT TYPE="hidden" NAME="pconv" VALUE="%f"
        ><INPUT TYPE="hidden" NAME="mis" VALUE="%d"
        ><INPUT TYPE="hidden" NAME="perc" VALUE="%f"
        ><INPUT TYPE="hidden" NAME="cpgcheck" VALUE="%s"
        ><INPUT TYPE="hidden" NAME="uniq" VALUE="%s"
        ><TABLE align="left" width="800" border="0" cellspacing="0" cellpadding="0" summary="resubmit table">
     <TR>
      <TD colspan="3"><HR></TD>
     </TR>
     <TR>
      <TD colspan="3"><HR></TD>
     </TR>
     <TR>
      <TD>Upload&nbsp;&nbsp;<B><INPUT TYPE="radio" NAME="resubtype" VALUE="0" checked
       >new/<INPUT TYPE="radio" NAME="resubtype" VALUE="1"
       >additional</B>&nbsp;&nbsp;&nbsp;bisulfite sequence file</TD>
      <TD><INPUT TYPE="file" NAME="biseq1"></TD>
      <TD><INPUT TYPE="submit" NAME="submit" VALUE="Resubmit"></TD>
     </TR>
     <TR>
      <TD colspan="3"><HR></TD>
     </TR>
    </TABLE></FORM></TD>
   </TR>
  </TABLE>
  <SCRIPT type="text/javascript" language="JavaScript">
  <!--
  checkValue ();
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
"Number of bisulfite sequences (used)",%d
"Number of bisulfite sequences (excluded)",%d
"Number of bisulfite sequences (total)",%d

"Condition to exclude low quality sequences"
"Upper limit of unconverted CpHs",%d
"Lower limit of percent converted CpHs","%f%%"
"Upper limit of alignment mismatches",%d
"Lower limit of percent identity","%f%%"

"Methylation status of each CpG site"
"CpG position",%s
"Number of methylated CpGs",%s
"Number of CpGs",%s
"ratio of methylated (%%)",%s
"S.D. of %% methylatied (between CpGs)","%.1f"
"S.E. of %% methylatied (between CpGs)","%.2f"
"S.D. of %% methylatied (between sequences)","%.1f"
"S.E. of %% methylatied (between sequences)","%.2f"

"Bisulfite sequence information"
"No.","sequence name","mismatches(include gaps)","gaps","alignment length","percent identity","methylated CpGs","percent methylated CpGs","unconverted CpHs","number of CpHs","percent converted CpHs","methylation pattern (U: unmethylated, M: methylated, A,C,G,T,N: mismatch,%s -: gap)"
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
my ($que );
my ($glen);
my ($stt );
my ($stp );
my ($g   );
my (%useq);
my (%que );
my ($mis );
my ($cpg );
my ($cpgp);
my ($perc);
my ($pat );
my ($out );
my ($name);
my ($size);
my ($unc );
my ($pcon);
my ($url1);
my ($url2);
my ($val1);
my ($val2);
my ($val3);
my ($val4);
my ($val5);
my ($opt );
my ($i   );
my ($js1 );
my ($js2 );
my ($ref );
my ($ord );
my (@refs);
my (@dsds);
my ($sds );
my ($ses );
my (@dsdc);
my ($sdc );
my ($sec );
my ($pos );
my ($down);
my ($meth);
my (%meth);
my ($allC);
my ($allM);
my ($m   );
my ($j   );
my ($tab );
my ($tab1);
my ($tab2);
my ($fmt1);
my ($fmt2);
my ($fmt3);
my ($numU);
my ($numE);
my ($numT);
my ($num );
my ($max );
my ($wrap);
my ($rows);
my ($chk );
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
    $out .= "=====\t1\n";
    $out .= join '', map {"$_\t$data->{$_}\n"} keys %$data;
    $out = Compress::Zlib::memGzip ($out);
    $size = length $out;
    $name = substr $data->{id}, 0, 12;
    $name .= "_$proj" if ($proj);
    $name .= "_quma_restore_analysis.qma";
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
$val1 = join (',', @cpg);
chomp (@que = <$fh>);
close $fh;

$i = 0;
$js1 = '';
$js2 = '';

foreach $que (@que) {
    $ref = {};
    @{$ref}{'pos', 'com', 'seq', 'qAli', 'gAli', 'aliLen', 'aliMis', 'perc',
	    'gap', 'menum', 'unc', 'conv', 'pconv', 'val', 'dir', 'gdir'} = split /\t/, $que;

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
        if (exists $useq{$ref->{aseq}}) {
	    $ref->{exc} = 1;
	    $ref->{nuniq} = 1;
	}
	$useq{$ref->{aseq}}++;
    }

    $ord = 'ord' . $ref->{pos};
    if (defined $data->{$ord}) {
        $data->{$ord} =~ s/\D//g;
        $data->{$ord} = 1000000 unless ($data->{$ord} =~ /\d/);
    } else {
        $data->{$ord} = 1000000;
    }

    push @refs, $ref;

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

@refs = sort {$a->{exc} <=> $b->{exc}} @refs;

$pos = join ',', map {$_->{pos}} grep {$_->{'exc'} == 0} @refs;

if (exists $data->{submit} && $data->{submit} eq DOWNFIG) {
    printf REPDOWN, $id, $pos, $proj;
    exit;
}

if (exists $data->{submit} && $data->{submit} eq MALI) {
    printf SHOWMALI, $id, $pos, $data->{cpgcheck};
    exit;
}

if (exists $data->{submit} && $data->{submit} eq GETFIG) {
    printf REPFIG, $id, $pos, $cpgn, $proj, $val1, $len, $data->{cpgcheck};
    exit;
}

for ($j = 1; $j <= $cpgn; $j++) {

    $meth{$j}{total} = 0;
    $meth{$j}{unmeth} = 0;
    $meth{$j}{meth} = 0;
    $meth{$j}{ng} = 0;
}

$allM = $allC = 0;
$numT = @refs;
$numU = 0;
$numE = 0;
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
	$numE++;

    } else {

	$numU++;
	for ($j = 1; $j <= $cpgn; $j++) {

	    $m = chop $meth;

	    if ($m eq '0') {
		$meth{$j}{total}++;
		$meth{$j}{unmeth}++;
		$allC++;
		$pat .= 'U';
	    } elsif ($m eq '1') {
		$meth{$j}{total}++;
		$meth{$j}{meth}++;
		$allC++;
		$allM++;
		$pat .= 'M';
	    } else {
		$meth{$j}{ng}++;
	        $m =~ y/MRWSYKVHDB/mrwsykvhdb/;
		$pat .= $m;
	    }
	}
    }

    $mis = $ref->{aliMis};
    $unc = "$ref->{unc}/" . ($ref->{unc} + $ref->{conv});

    $pat ||= 'excluded';
    $cpg  = $ref->{val} =~ y/01//;
    $cpgp = $cpg ? 100 * $ref->{menum} / $cpg : 0;
    push @dsds, $cpgp unless ($ref->{exc}); 
    $cpgp = sprintf "%5.1f", $cpgp;

    $out .= join ',', ($i+1, qq{"$ref->{com}"}, $mis, $ref->{gap},
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

    $tab .= sprintf TAB, ($cols->[$i % @$cols], $url1, ++$i, $ref->{pos},
			  $i, $ref->{pos}, 'on', $chk,
			  $wrap, $max, htmlSunitize($ref->{com}), 
                          $mis, $ref->{gap}, $ref->{aliLen},
			  $perc, $ref->{menum}, $cpgp, $unc, $pcon, $url2);
}

$val2 = join (',', map  {"$_->{meth}%7C$_->{total}"}
	           map  {$meth{$_}}
	           sort {$a <=> $b}
	           keys %meth);
$opt = sprintf CPGOPT, ($id, $len, $val1, $val2);

if (exists $data->{submit} && $data->{submit} eq DOWNCPGG) {
    $url1 = $data->{graphShow} == 0 ? REPCPGG1 :
	    $data->{graphShow} == 1 ? REPCPGG2 :
	    $data->{graphShow} == 2 ? REPCPGG3 :
	    $data->{graphShow} == 3 ? REPCPGG4 :
	    $data->{graphShow} == 4 ? REPCPGG5 :
	                              REPCPGG6 ;
    printf $url1, $id, $len, $val1, $val2, $proj, $data->{format};
    exit;
}

@dsdc = map {$_->{total} ? 100 * $_->{meth}/$_->{total} : 0}
        map {$meth{$_}} sort {$a <=> $b} keys %meth;

$sds = @dsds ? stddev @dsds : 0;
$sdc = @dsdc ? stddev @dsdc : 0;
$ses = $sds / sqrt(@dsds || 1);
$sec = $sdc / sqrt($cpgn || 1);

if (exists $data->{submit} && $data->{submit} eq DOWNCPGD) {
    $val3 = join (',', map {$_->{meth}}
		       map {$meth{$_}}
		       sort {$a <=> $b}
	               keys %meth);
    $val4 = join (',', map {$_->{total}}
	               map {$meth{$_}}
	               sort {$a <=> $b}
	               keys %meth);
    $val5 = join (',', map {sprintf "%.1f", $_} @dsdc);

    $val1 .= ',"total"';
    $val3 .= ",$allM";
    $val4 .= ",$allC";
    $val5 .= sprintf ",%.1f", ($allC ? 100 * $allM / $allC : 0);
    $val2  = '';
    $proj =~ s/"//g;
    $val2 .= qq{"Project name","$proj"\n} if ($proj);
    $grp1 =~ s/"//g;
    $val2 .= qq{"Sequence group name","$grp1"\n} if ($grp1);
    $out = sprintf OUTFORM, $val2, $len, $cpgn, $numU, $numE, $numT,
                            $data->{unconv}, $data->{pconv}, $data->{mis}, $data->{perc},
                            $val1, $val3, $val4, $val5, $sdc, $sec, $sds, $ses, $cchk, $out;
    $size = length $out;
    $name = substr $data->{id}, 0, 12;
    $name .= "_$proj" if ($proj);
    $name .= "_quma_analy_data.csv";
    print qq{Content-Disposition: attachment; filename="$name"\n};
    print qq{Content-Length: $size\n};
    print qq{Content-Type: text/csv\n};
    print qq{Status: 200 OK\n\n};
    print $out;
    exit;
}

$data->{graphShow}  ||= 0;
$data->{optionShow} ||= 0;

$proj = htmlSunitize ($proj) if ($proj);
$grp1 = htmlSunitize ($grp1) if ($grp1);
$val1  = 3;
$val2  = '';
$val3  = '';
$val1++ if ($proj);
$val2 .= qq{      <TH>Project<BR>name</TH>\n} if ($proj);
$val3 .= qq{      <TD align="center">$proj</TD>\n} if ($proj);
$val1++ if ($grp1);
$val2 .= qq{      <TH>sequence<BR>group name</TH>\n} if ($grp1);
$val3 .= qq{      <TD align="center">$grp1</TD>\n\n} if ($grp1);
printf HEAD, $js1, $js2, BFS, $id, $data->{optionShow}, $data->{graphShow}, $data->{cpgcheck}, $data->{uniq},
             $val1, $val2, $val3, $len, $cpgn, $numU ||= 0, $numE ||= 0, $numT ||=0;

$num = int (($cpgn + 1)/ CPGROWL1) + 1;
$rows = int (($cpgn + 1)/$num);
$rows++ if ($cpgn + 1 - $rows * $num);

print  SUMTAB1;

for ($i = 0; $i < $rows * $num - 1; $i++) {
    if($i && ! ($i % $rows)) {
	print $tab1.SUMTAB3.$tab2.SUMTAB5.SUMTAB6;
	$tab1 = $tab2 = '';
    }

    if ($i > @cpg - 1) {
	$tab1 .= SUMTAB7;
	$tab2 .= SUMTAB7;
	next;
    }

    $cpgp  = $meth{$i+1}->{total} ? 100 * $meth{$i+1}->{meth}/$meth{$i+1}->{total} : 0;
    $tab1 .= sprintf SUMTAB2, $cpg[$i];
    $tab2 .= sprintf SUMTAB4, $meth{$i+1}->{meth}, $meth{$i+1}->{total}, $cpgp;
}

$tab1 .= sprintf SUMTAB2, 'Total';
$tab2 .= sprintf SUMTAB4, ($allM, $allC,
			   $allC ? 100 * $allM / $allC : 0);

print $tab1.SUMTAB3.$tab2.SUMTAB5;

$fmt1 = $fmt2 = $fmt3 = '';

if ($data->{format} eq 'SVG') {
    $fmt2 = 'SELECTED';
} elsif ($data->{format} eq 'SVGZ') {
    $fmt3 = 'SELECTED';
} else {
    $fmt1 = 'SELECTED';
}

printf SUMTAB8, ($sdc, $sec, $sds, $ses, CPGFIG1.$opt,CPGFIG2.$opt,CPGFIG3.$opt,
		 CPGFIG4.$opt,CPGFIG5.$opt,CPGFIG6.$opt,
		 DOWNCPGG, $fmt1, $fmt2, $fmt3);

printf TABH, (SAVE,
              $data->{order}  == 1 ? 'checked' : '',
	      $data->{order}  == 2 ? 'checked' : '',
	      $data->{order}  == 3 ? 'checked' : '',
	      $data->{order}  == 4 ? 'checked' : '',
	      $data->{order}  == 5 ? 'checked' : '',
	      $data->{order}  == 6 ? 'checked' : '',
	      $data->{order}  == 7 ? 'checked' : '',
	      $data->{direct} == 1 ? 'checked' : '',
	      $data->{direct} == 2 ? 'checked' : '',
	      $data->{unconv}, $data->{pconv}, $data->{mis}, $data->{perc},
	      RSTPARA, RENEW, GETFIG, DOWNFIG, DOWNCPGD, DOWNALID, MALI);

$conv = $data->{conv} ? '    alert("' . CONVER. '")' : '';
print $tab;

printf FOOT, RENEW, GETFIG, DOWNFIG, DOWNCPGD, DOWNALID, MALI, MAKEBI, $id,
             $data->{unconv}, $data->{pconv}, $data->{mis}, $data->{perc}, $data->{cpgcheck}, $data->{uniq}, $conv;
###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
