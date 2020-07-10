#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeAllBiFig.cgi                                               *
#_* cgi for creating show methylation pattern figure view                     *
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

use constant HTML => q[Content-type:text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="en">
 <HEAD>
  <META HTTP-EQUIV="Content-Type" content="text/html; charset=ISO-8859-1">
  <META HTTP-EQUIV="Content-Script-Type" content="text/javascript">
  <META HTTP-EQUIV="Content-Style-Type" content="text/css">
  <LINK REV="MADE" HREF="mailto:yuichi@kumaki.jp">
  <LINK REL="INDEX" HREF="].HL.q[/top/index.html">
  <TITLE>Methylation pattern</TITLE>
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

	document.allform.figureShow.value--;
	if (document.allform.figureShow.value < 0) {
	    document.allform.figureShow.value = 3;
	}
	ffigure();
    }

    function foption() {
       if (browser == "IE56NN6") {
         optionAnc  = document.getElementById("options");
	 optionText = document.getElementById("options").childNodes.item(0);
	 optionAnc.removeChild(optionText);

         if (document.allform.optionShow.value == 0) {
           if (document.allform.figureShow.value == 0) {
	     document.getElementById("optionstab1").style.display = "block";
	     document.getElementById("optionstab2").style.display = "none";
	     document.getElementById("optionstab3").style.display = "none";
	     document.getElementById("optionstab4").style.display = "none";
	   } else if (document.allform.figureShow.value == 1) {
	     document.getElementById("optionstab1").style.display = "none";
	     document.getElementById("optionstab2").style.display = "block";
	     document.getElementById("optionstab3").style.display = "none";
	     document.getElementById("optionstab4").style.display = "none";
	   } else if (document.allform.figureShow.value == 2) {
	     document.getElementById("optionstab1").style.display = "none";
	     document.getElementById("optionstab2").style.display = "none";
	     document.getElementById("optionstab3").style.display = "block";
	     document.getElementById("optionstab4").style.display = "none";
	   } else {
	     document.getElementById("optionstab1").style.display = "none";
	     document.getElementById("optionstab2").style.display = "none";
	     document.getElementById("optionstab3").style.display = "none";
	     document.getElementById("optionstab4").style.display = "block";
	   }

           document.getElementById("optionSpace").style.background = "#FFFFFF";
	   document.getElementById("optImage1").src = "].HL.q[/images/icon033.gif";
	   newText = document.createTextNode(" Hide options");
           document.allform.optionShow.value = "1";

         } else {
	   document.getElementById("optionstab1").style.display = "none";
	   document.getElementById("optionstab2").style.display = "none";
           document.getElementById("optionstab3").style.display = "none";
           document.getElementById("optionstab4").style.display = "none";
           document.getElementById("optionSpace").style.background = "#EAEAFB";
	   document.getElementById("optImage1").src = "].HL.q[/images/icon030.gif";
	   newText = document.createTextNode(" Show options");
           document.allform.optionShow.value = "0";
	 }

         optionAnc.appendChild(newText);

       } else if (browser == "IE46") {
         if (document.allform.optionShow.value == 0) {
           if (document.allform.figureShow.value == 0) {
             optionstab1.style.display = "block";
             optionstab2.style.display = "none";
             optionstab3.style.display = "none";
             optionstab4.style.display = "none";
	   } else if (document.allform.figureShow.value == 1) {
             optionstab1.style.display = "none";
             optionstab2.style.display = "block";
             optionstab3.style.display = "none";
             optionstab4.style.display = "none";
	   } else if (document.allform.figureShow.value == 2) {
             optionstab1.style.display = "none";
             optionstab2.style.display = "none";
             optionstab3.style.display = "block";
             optionstab4.style.display = "none";
	   } else {
             optionstab1.style.display = "none";
             optionstab2.style.display = "none";
             optionstab3.style.display = "none";
             optionstab4.style.display = "block";
	   }

           optionSpace.style.backgroundcolor = "#FFFFFF";
           document.images[5].src = "].HL.q[/images/icon033.gif";
	   options.innerText = " Hide options";
           document.allform.optionShow.value = "1";

         } else {
           optionstab1.style.display = "none";
           optionstab2.style.display = "none";
           optionstab3.style.display = "none";
           optionstab4.style.display = "none";
           optionSpace.style.backgroundcolor = "#EAEAFB";
           document.images[5].src = "].HL.q[/images/icon030.gif";
	   options.innerText = " Show options";
           document.allform.optionShow.value = "0";
         }
       }
    }

    function ffigure() {
      if (browser == "IE56NN6") {
        if (document.allform.figureShow.value == 0) {
	  document.getElementById("methFigure1").style.display = "none";
	  document.getElementById("methFigure2").style.display = "block";
          document.getElementById("methFigure3").style.display = "none";
          document.getElementById("methFigure4").style.display = "none";
          document.allform.figureShow.value = 1;

      } else if (document.allform.figureShow.value == 1) {
	  document.getElementById("methFigure1").style.display = "none";
	  document.getElementById("methFigure2").style.display = "none";
	  document.getElementById("methFigure3").style.display = "block";
          document.getElementById("methFigure4").style.display = "none";
          document.allform.figureShow.value = 2;
      } else if (document.allform.figureShow.value == 2) {
	  document.getElementById("methFigure1").style.display = "none";
	  document.getElementById("methFigure2").style.display = "none";
	  document.getElementById("methFigure3").style.display = "none";
          document.getElementById("methFigure4").style.display = "block";
          document.allform.figureShow.value = 3;
      } else {
	  document.getElementById("methFigure1").style.display = "block";
	  document.getElementById("methFigure2").style.display = "none";
          document.getElementById("methFigure4").style.display = "none";
	  document.getElementById("methFigure3").style.display = "none";
          document.allform.figureShow.value = 0;
	 }

      } else if (browser == "IE46") {
        if (document.allform.figureShow.value == 0) {
          methFigure1.style.display = "none";
          methFigure2.style.display = "block";
          methFigure3.style.display = "none";
          methFigure4.style.display = "none";
          document.allform.figureShow.value = 1;

        } else if (document.allform.figureShow.value == 1) {
          methFigure1.style.display = "none";
          methFigure2.style.display = "none";
          methFigure3.style.display = "block";
          methFigure4.style.display = "none";
          document.allform.figureShow.value = 2;

        } else if (document.allform.figureShow.value == 2) {
          methFigure1.style.display = "none";
          methFigure2.style.display = "none";
          methFigure3.style.display = "none";
          methFigure4.style.display = "block";
          document.allform.figureShow.value = 3;

        } else {
          methFigure1.style.display = "block";
          methFigure2.style.display = "none";
          methFigure3.style.display = "none";
          methFigure4.style.display = "none";
          document.allform.figureShow.value = 0;
        }
      }

      if (document.allform.optionShow.value == 0) {
	document.allform.optionShow.value = 1;
      } else {
	document.allform.optionShow.value = 0;
      }

      foption();
    }

    if(opener) {
       opener.document.allform.target="downner";
    }
    focus();
  //-->
  </SCRIPT>
 </HEAD>
 <BODY style="background-color:#FFFFFF">
  <DIV align="left">
  <TABLE border="0" cellspacing="0" cellpadding="0" summary="title table">
   <TR style="background-color:#3333CC">
    <TD><IMG src="].HL.q[/images/spacer.gif" width="500" height="5" alt="space"></TD>
   </TR>
   <TR>
    <TD align="center" style="color:#333399;font-size:x-large;font-weight:bold;font-style:italic">
    Methylation pattern
    </TD>
   </TR>
   <TR style="background-color:#3333CC">
    <TD><IMG src="].HL.q[/images/spacer.gif" width="500" height="5" alt="space"></TD>
   </TR>
  </TABLE>
  <DIV STYLE="text-align:right"><A HREF="javascript:close();void(0);"><IMG SRC="].HL.q[/images/iconClose.gif" alt="close" border="0"></A></DIV>
  <FORM ACTION="%s" METHOD="post" name="allform">
  <INPUT TYPE="hidden" NAME="id" VALUE="%s">
  <INPUT TYPE="hidden" NAME="pos" VALUE="%s">
  <INPUT TYPE="hidden" NAME="cpgn" VALUE="%s">
  <INPUT TYPE="hidden" NAME="proj" VALUE="%s">
  <INPUT TYPE="hidden" NAME="cpgpos" VALUE="%s">
  <INPUT TYPE="hidden" NAME="glen" VALUE="%d">
  <INPUT TYPE="hidden" NAME="optionShow" VALUE="%d">
  <INPUT TYPE="hidden" NAME="figureShow" VALUE="%d">
  <INPUT TYPE="hidden" NAME="cpgcheck" VALUE="%s">
  <TABLE border="0" cellspacing="0" cellpadding="0" summary="main table">
   <TR style="background-color:#EAEAFB">
    <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="summary table">
     <TR>
      <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="common table">
       <TR>
        <TD><IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
            <INPUT TYPE="submit" NAME="submit" VALUE="%s">
            <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space"></TD>
        <TD><TABLE border="0" cellspacing="0" cellpadding="0" summary="change table">
         <TR>
          <TD align="left" onmousedown="foption()" onkeydown="foption()" style="cursor: pointer;">
           <IMG id="optImage1" src="].HL.q[/images/icon030.gif" alt="option switch"><A id="options" style="color:blue;text-decoration:underline">&nbsp;Show options</A></TD>
         </TR>
         <TR>
          <TD align="left" onmousedown="ffigure()" onkeydown="ffigure()" style="cursor: pointer;">
           <IMG src="].HL.q[/images/icon034.gif" alt="list"><A style="color: blue;text-decoration: underline">&nbsp;Change figure</A></TD>
         </TR>
        </TABLE></TD>
       </TR>
       <TR>
        <TD colspan="2" align="center">(file format
             <SELECT NAME="format">
              <OPTION VALUE="PNG" %s>PNG
              <OPTION VALUE="SVG" %s>SVG
              <OPTION VALUE="SVGZ" %s>SVGZ
             </SELECT>&nbsp;<A HREF="javascript:window.open('].HL.q[/help/formatHelp.html','help','width=600,height=420,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A>&nbsp;)</TD>
       </TR>
      </TABLE></TD>
      <TD><IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space"></TD>
      <TD id="optionSpace" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
      <TD><TABLE id="optionstab1" style="display:none;font-size:small" border="0" cellspacing="0" cellpadding="0" summary="option table 1">
       <TR>
        <TD colspan="7" valign="middle"><TABLE border="0" cellspacing="0" cellpadding="0" summary="mismatch table" style="font-size:small" >
         <TR>
          <TD valign="middle">&nbsp;In case of mismatch : &nbsp;</TD>
          <TD style="background-color:#FFFFFF" valign="middle"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
          <TD valign="middle"><INPUT TYPE="radio" NAME="mistype" VALUE="1" %s></TD>
          <TD valign="middle">show &quot;X&quot;&nbsp;</TD>
          <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
          <TD valign="middle"><INPUT TYPE="radio" NAME="mistype" VALUE="2" %s></TD>
          <TD valign="middle">show bases&nbsp;</TD>
          <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
          <TD valign="middle"><INPUT TYPE="radio" NAME="mistype" VALUE="3" %s></TD>
          <TD valign="middle">do not show&nbsp;</TD>
         </TR>
        </TABLE></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="8">&nbsp;<INPUT TYPE="checkbox" NAME="showno1" VALUE="on" %s>&nbsp;Show CpG No.
            (<INPUT TYPE="radio" NAME="cpgno1" VALUE="0" %s>top
             <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
             <INPUT TYPE="radio" NAME="cpgno1" VALUE="1" %s>bottom
             <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
             <INPUT TYPE="checkbox" NAME="revno1" VALUE="on" %s>&nbsp;Reverse)</TD>
       </TR>
       <TR>
        <TD colspan="7" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="9" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
       </TR>
       <TR>
        <TD>&nbsp;Width of column</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="eachw" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD rowspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD>&nbsp;Diameter of circle</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="diame" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD rowspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="8">&nbsp;<INPUT TYPE="checkbox" NAME="showcpg1" VALUE="on" %s>&nbsp;Show CpG position
            (<INPUT TYPE="radio" NAME="pospos1" VALUE="1" %s>top
             <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
             <INPUT TYPE="radio" NAME="pospos1" VALUE="0" %s>bottom
             <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
             <INPUT TYPE="checkbox" NAME="revpos1" VALUE="on" %s>&nbsp;Reverse)</TD>
       </TR>
       <TR>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="1" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="7" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
       </TR>
       <TR>
        <TD>&nbsp;Height of row</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="eachh" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD>&nbsp;Line width</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="line" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD>&nbsp;Start postion&nbsp;:&nbsp;<INPUT TYPE="text" NAME="spos1" VALUE="%s" SIZE="4"></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD>&nbsp;Scale to show</TD><TD>&nbsp;:&nbsp;</TD><TD>1/<INPUT TYPE="text" NAME="scale" VALUE="%d" SIZE="2"></TD>
        <TD align="right"><INPUT TYPE="submit" NAME="submit" VALUE="Renew"></TD>
	<TD></TD>
        <TD align="right"><A HREF="javascript:window.open('].HL.q[/help/%s','help','width=700,height=500,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
       </TR>
      </TABLE></TD>
      <TD><TABLE id="optionstab2" style="display:none;font-size:small" border="0" cellspacing="0" cellpadding="0" summary="option table 2">
       <TR>
        <TD colspan="3" valign="middle">&nbsp;Center line width&nbsp;:&nbsp;<INPUT TYPE="text" NAME="center" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD rowspan="5" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD>&nbsp;Scale to show</TD><TD>&nbsp;:&nbsp;</TD><TD>1/<INPUT TYPE="text" NAME="scale2" VALUE="%d" SIZE="2"></TD>
        <TD rowspan="5" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="5">&nbsp;<INPUT TYPE="checkbox" NAME="showno2" VALUE="on" %s>&nbsp;Show CpG No.
                        (<INPUT TYPE="radio" NAME="cpgno2" VALUE="0" %s>top
                         <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
                         <INPUT TYPE="radio" NAME="cpgno2" VALUE="1" %s>bottom
                         <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
                         <INPUT TYPE="checkbox" NAME="revno2" VALUE="on" %s>&nbsp;Reverse)</TD>
       </TR>
       <TR>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="5" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
       </TR>
       <TR>
        <TD>&nbsp;Width of column</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="eachw2" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD>&nbsp;Diameter of circle</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="diame2" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD colspan="5">&nbsp;<INPUT TYPE="checkbox" NAME="showcpg2" VALUE="on" %s>&nbsp;Show CpG position
                       (<INPUT TYPE="radio" NAME="pospos2" VALUE="1" %s>top
                        <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
                        <INPUT TYPE="radio" NAME="pospos2" VALUE="0" %s>bottom
                        <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
                        <INPUT TYPE="checkbox" NAME="revpos2" VALUE="on" %s>Reverse)&nbsp;</TD>
       </TR>
       <TR>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="5" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
       </TR>
       <TR>
        <TD>&nbsp;Height of row</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="eachh2" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD>&nbsp;Line width</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="line2" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD>&nbsp;Start postion&nbsp;:&nbsp;<INPUT TYPE="text" NAME="spos2" VALUE="%s" SIZE="4"></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD align="right"><INPUT TYPE="submit" NAME="submit2" VALUE="Renew"></TD>
	<TD></TD>
        <TD align="right"><A HREF="javascript:window.open('].HL.q[/help/figOptionHelp2.html','help','width=550,height=550,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
       </TR>
      </TABLE></TD>
      <TD><TABLE id="optionstab3" style="display:none;font-size:small" border="0" cellspacing="0" cellpadding="0" summary="option table 3">
       <TR>
        <TD colspan="3" valign="middle">&nbsp;Center line width&nbsp;:&nbsp;<INPUT TYPE="text" NAME="center2" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD>&nbsp;Scale of width</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="bscale" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels/base</A></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="3">&nbsp;<INPUT TYPE="checkbox" NAME="showcpg" VALUE="on" %s>&nbsp;Show CpG position</TD>
       </TR>
       <TR>
        <TD colspan="11" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
       </TR>
       <TR>
        <TD>&nbsp;Diameter of circle</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="diame3" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD rowspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD>&nbsp;Scale to show</TD><TD>&nbsp;:&nbsp;</TD><TD>1/<INPUT TYPE="text" NAME="scale3" VALUE="%d" SIZE="2"></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="3"><INPUT TYPE="radio" NAME="pospos3" VALUE="1" %s>top
                        <IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space">
                        <INPUT TYPE="radio" NAME="pospos3" VALUE="0" %s>bottom</TD>
       </TR>
       <TR>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD rowspan="2" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
       </TR>
       <TR>
        <TD>&nbsp;Height of row</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="eachh3" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD>&nbsp;Line width</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="line3" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD align="right"><INPUT TYPE="submit" NAME="submit3" VALUE="Renew"></TD>
	<TD></TD>
        <TD align="right"><A HREF="javascript:window.open('].HL.q[/help/figOptionHelp3.html','help','width=600,height=650,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
       </TR>
      </TABLE></TD>
      <TD><TABLE id="optionstab4" style="display:none;font-size:small" border="0" cellspacing="0" cellpadding="0" summary="option table 4">
       <TR>
        <TD colspan="3" valign="middle">&nbsp;Center line width&nbsp;:&nbsp;<INPUT TYPE="text" NAME="center3" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD>&nbsp;Scale of width</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="bscale2" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels/base</A></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="6">&nbsp;<INPUT TYPE="checkbox" NAME="showno4" VALUE="on" %s>&nbsp;Show CpG No.
                        (<INPUT TYPE="radio" NAME="cpgno4" VALUE="0" %s>top
                         <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
                         <INPUT TYPE="radio" NAME="cpgno4" VALUE="1" %s>bottom
                         <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
                         <INPUT TYPE="checkbox" NAME="revno4" VALUE="on" %s>&nbsp;Reverse)</TD>
       </TR>
       <TR>
        <TD colspan="14" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
       </TR>
       <TR>
        <TD>&nbsp;Diameter of circle</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="diame4" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD rowspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD>&nbsp;Scale to show</TD><TD>&nbsp;:&nbsp;</TD><TD>1/<INPUT TYPE="text" NAME="scale4" VALUE="%d" SIZE="2"></TD>
        <TD rowspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="6">&nbsp;<INPUT TYPE="checkbox" NAME="showcpg4" VALUE="on" %s>&nbsp;Show CpG position
                        (<INPUT TYPE="radio" NAME="pospos4" VALUE="1" %s>top
                         <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
                         <INPUT TYPE="radio" NAME="pospos4" VALUE="0" %s>bottom
                         <IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space">
                         <INPUT TYPE="checkbox" NAME="revpos4" VALUE="on" %s>&nbsp;Reverse)&nbsp;</TD>
       </TR>
       <TR>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="3" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
        <TD colspan="6" style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="3" height="2" alt="space"></TD>
       </TR>
       <TR>
        <TD>&nbsp;Height of row</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="eachh4" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD>&nbsp;Line width</TD><TD>&nbsp;:&nbsp;</TD><TD><INPUT TYPE="text" NAME="line4" VALUE="%d" SIZE="4"><A style="font-size:x-small">pixels</A></TD>
        <TD>Start postion&nbsp;:&nbsp;<INPUT TYPE="text" NAME="spos4" VALUE="%s" SIZE="4"></TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space"></TD>
        <TD><INPUT TYPE="checkbox" NAME="circle4" VALUE="on" %s>&nbsp;Show as circle graph</TD>
        <TD style="background-color:#FFFFFF"><IMG src="].HL.q[/images/spacer.gif" width="2" height="2" alt="space"></TD>
        <TD align="right"><IMG src="].HL.q[/images/spacer.gif" width="10" height="4" alt="space"><INPUT TYPE="submit" NAME="submit3" VALUE="Renew"></TD>
        <TD align="right"><A HREF="javascript:window.open('].HL.q[/help/figOptionHelp4.html','help','width=700,height=520,resizable,scrollbars').focus();void(0);"><IMG width="14" height="14" src="].HL.q[/images/help.gif" alt="help" border="0"></A></TD>
       </TR>
      </TABLE></TD>
     </TR>
    </TABLE></TD>
   </TR>
   <TR>
    <TD><IMG src="].HL.q[/images/spacer.gif" width="5" height="4" alt="space"></TD>
   </TR>
   <TR>
    <TD><TABLE id="methFigure1" style="display:block" border="0" cellspacing="0" cellpadding="0" summary="figure1 table">
     <TR>
      <TD><IMG SRC="%s" alt="figure1" width="%d" height="%d"></TD>
     </TR>
    </TABLE><TABLE id="methFigure2" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="figur2 table">
     <TR>
      <TD><IMG SRC="%s" alt="figure2" width="%d" height="%d"></TD>
     </TR>
    </TABLE><TABLE id="methFigure3" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="figure3 table">
     <TR>
      <TD><IMG SRC="%s" alt="figure3" width="%d" height="%d"></TD>
     </TR>
    </TABLE><TABLE id="methFigure4" style="display:none" border="0" cellspacing="0" cellpadding="0" summary="figure4 table">
     <TR>
      <TD><IMG SRC="%s" alt="figure4" width="%d" height="%d"></TD>
     </TR>
    </TABLE></TD>
   </TR>
  </TABLE>
  </FORM>
  </DIV>
  <DIV STYLE="text-align:right"><A HREF="javascript:close();void(0);"><IMG SRC="].HL.q[/images/iconClose.gif" alt="close" border="0"></A></DIV>
  <SCRIPT type="text/javascript" language="JavaScript">
  <!--
  checkValue();
  //-->
  </SCRIPT>
 </BODY>
</HTML>
];

my ($cgi    );
my ($data   );
my ($help   );
my (@pos    );
my (@cpg    );
my ($num    );
my ($fmt1   );
my ($fmt2   );
my ($fmt3   );
my (%chk    );
my ($url1   );
my ($min    );
my ($max    );
my ($mlen   );
my ($posdi  );
my ($width1 );
my ($height1);
my ($url2   );
my ($width2 );
my ($height2);
my ($start  );
my ($stop   );
my ($url3   );
my ($width3 );
my ($height3);
my ($url4   );
my ($width4 );
my ($height4);
local ($_   );

$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;
ipCheck ($data);
$data->{pos}
    or errorAndExit ('No data to show', 'No data to show', "No data to show : $data->{pos}");
$data->{pos} =~ /^\d+(,\d+)*$/
    or errorAndExit ('Invalid access', 'Invalid access', "Invalid POS value : $data->{pos}");
$data->{cpgn}
    or errorAndExit ('No data to show', 'No data to show', "No data to show : $data->{cpgn}");
$data->{cpgn} =~ /^\d+$/
    or errorAndExit ('Invalid access', 'Invalid access', "Invalid CpG num value : $data->{cpgn}");
$data->{cpgpos}
    or errorAndExit ('No data to show', 'No data to show', "No data to show : $data->{cpgpos}");
$data->{cpgpos} =~ /^\d+(\,\d+)*$/
    or errorAndExit ('Invalid access', 'Invalid access', "Invalid CpG num value : $data->{cpgpos}");
$data->{glen}
    or errorAndExit ('No data to show', 'No data to show', "No data to show : $data->{glen}");
$data->{glen} =~ /^\d+$/
    or errorAndExit ('Invalid access', 'Invalid access', "Invalid CpG num value : $data->{glen}");
$data->{cpgcheck} = 0
    unless (exists $data->{cpgcheck} && $data->{cpgcheck} eq 'on');
$help = $data->{cpgcheck} ? 'figOptionHelpC.html': 'figOptionHelp.html';

$data->{proj} ||= '';
$data->{proj} =~ y/&;`'"|*?~<>^()[]{}$\\\n\r//d;
$data->{proj} =~ s/[^\w-]//g;
@pos = split ',', $data->{pos};
$num = @pos;
@cpg = split ',', $data->{cpgpos};

$data->{eachw} = EACHW2
    unless (exists $data->{eachw}  && $data->{eachw}  =~ /^\d+$/ && $data->{eachw} > 0);
$data->{eachh} = EACHH2
    unless (exists $data->{eachh}  && $data->{eachh}  =~ /^\d+$/ && $data->{eachh}  > 0);
$data->{diame} = DIAME2
    unless (exists $data->{diame}  && $data->{diame}  =~ /^\d+$/ && $data->{diame}  > 0);
$data->{line}  = LINEW2
    unless (exists $data->{line}   && $data->{line}   =~ /^\d+$/ && $data->{line}   > 0);
$data->{scale} = SCALE
    unless (exists $data->{scale}  && $data->{scale}  =~ /^\d+$/ && $data->{scale}  > 0);
$data->{spos1}  = SPOS
    unless (exists $data->{spos1}  && $data->{spos1} =~ /^-?\d+$/);

$data->{center} = CLINEW
    unless (exists $data->{center} && $data->{center} =~ /^\d+$/ && $data->{center} > 0);
$data->{eachw2} = EACHW3
    unless (exists $data->{eachw2} && $data->{eachw2} =~ /^\d+$/ && $data->{eachw2} > 0);
$data->{eachh2} = EACHH3
    unless (exists $data->{eachh2} && $data->{eachh2} =~ /^\d+$/ && $data->{eachh2} > 0);
$data->{diame2} = DIAME3
    unless (exists $data->{diame2} && $data->{diame2} =~ /^\d+$/ && $data->{diame2} > 0);
$data->{line2}  = LINEW3
    unless (exists $data->{line2}  && $data->{line2}  =~ /^\d+$/ && $data->{line2}  > 0);
$data->{scale2} = SCALE3
    unless (exists $data->{scale2} && $data->{scale2} =~ /^\d+$/ && $data->{scale2} > 0);
$data->{spos2}  = SPOS
    unless (exists $data->{spos2}  && $data->{spos2} =~ /^-?\d+$/);

$data->{center2} = CLINEW2
    unless (exists $data->{center2} && $data->{center2} =~ /^\d+$/ && $data->{center2} > 0);
$data->{eachh3} = EACHH4
    unless (exists $data->{eachh3} && $data->{eachh3} =~ /^\d+$/ && $data->{eachh3} > 0);
$data->{diame3} = DIAME4
    unless (exists $data->{diame3} && $data->{diame3} =~ /^\d+$/ && $data->{diame3} > 0);
$data->{line3}  = LINEW4
    unless (exists $data->{line3}  && $data->{line3}  =~ /^\d+$/ && $data->{line3}  > 0);
$data->{scale3} = SCALE4
    unless (exists $data->{scale3} && $data->{scale3} =~ /^\d+$/ && $data->{scale3} > 0);
$data->{bscale} = BSCALE
    unless (exists $data->{bscale} && $data->{bscale} =~ /^\d+$/ && $data->{bscale} > 0);

$data->{center3} = CLINEW3
    unless (exists $data->{center3} && $data->{center3} =~ /^\d+$/ && $data->{center3} > 0);
$data->{eachh4} = EACHH5
    unless (exists $data->{eachh4} && $data->{eachh4} =~ /^\d+$/ && $data->{eachh4} > 0);
$data->{diame4} = DIAME5
    unless (exists $data->{diame4} && $data->{diame4} =~ /^\d+$/ && $data->{diame4} > 0);
$data->{line4}  = LINEW5
    unless (exists $data->{line4}  && $data->{line4}  =~ /^\d+$/ && $data->{line4}  > 0);
$data->{scale4} = SCALE5
    unless (exists $data->{scale4} && $data->{scale4} =~ /^\d+$/ && $data->{scale4} > 0);
$data->{bscale2}= BSCALE2
    unless (exists $data->{bscale2} && $data->{bscale2} =~ /^\d+$/ && $data->{bscale2} > 0);
$data->{spos4}  = SPOS
    unless (exists $data->{spos4}  && $data->{spos4} =~ /^-?\d+$/);

$data->{optionShow} ||= 0;
$data->{figureShow} ||= 0;
$data->{showno1}    ||= '';
$data->{revno1}     ||= '';
$data->{cpgno1}     ||= 0;
$data->{showcpg1}   ||= '';
$data->{revpos1}    ||= '';
$data->{pospos1}    ||= 0;
$data->{showno2}    ||= '';
$data->{revno2}     ||= '';
$data->{cpgno2}     ||= 0;
$data->{showcpg2}   ||= '';
$data->{revpos2}    ||= '';
$data->{pospos2}    ||= 0;
$data->{showcpg}    ||= '';
$data->{pospos3}    ||= 0;
$data->{showno4}    ||= '';
$data->{revno4}     ||= '';
$data->{cpgno4}     ||= 0;
$data->{showcpg4}   ||= '';
$data->{revpos4}    ||= '';
$data->{pospos4}    ||= 0;
$data->{format}     ||= 'PNG';
$data->{circle4}    ||= '';

$data->{mistype} ||= MISTYPE;
$data->{mistype} =~ /^[123]$/ or $data->{mistype} = MISTYPE;

if (exists $data->{submit} && $data->{submit} eq DOWNFIG) {
    if ($data->{figureShow} == 0) {
        printf REPDOWNO, $data->{id}, $data->{format}, $data->{pos}, $data->{eachw},
                         $data->{eachh}, $data->{diame}, $data->{line}, 
                         $data->{proj}, $data->{mistype}, $data->{showcpg1},
                         $data->{spos1}, $data->{revpos1}, $data->{pospos1},
                         $data->{showno1}, $data->{cpgno1}, $data->{revno1};

    } elsif ($data->{figureShow} == 1) {
        printf REP2DOWN, $data->{id}, $data->{format}, $data->{pos}, $data->{eachw2},
                         $data->{eachh2}, $data->{diame2}, $data->{line2}, 
                         $data->{proj}, $data->{center}, $data->{showcpg2},
                         $data->{spos2}, $data->{revpos2}, $data->{pospos2},
                         $data->{showno2}, $data->{cpgno2}, $data->{revno2};

    } elsif ($data->{figureShow} == 2) {
        printf REP3DOWN, $data->{id}, $data->{format}, $data->{pos},
                         $data->{eachh3}, $data->{diame3}, $data->{line3}, 
                         $data->{proj}, $data->{center2}, $data->{bscale},
                         $data->{showcpg}, $data->{pospos3};

    } else {
        printf REP4DOWN, $data->{id}, $data->{format}, $data->{pos},
                         $data->{eachh4}, $data->{diame4}, $data->{line4}, 
                         $data->{proj}, $data->{center3}, $data->{bscale2}, $data->{showcpg4},
                         $data->{spos4}, $data->{revpos4}, $data->{pospos4},
                         $data->{showno4}, $data->{cpgno4}, $data->{revno4}, $data->{circle4};

    }
    exit;
}

$fmt1 = $fmt2 = $fmt3 = '';

if ($data->{format} eq 'SVG') {
    $fmt2 = 'SELECTED';
} elsif ($data->{format} eq 'SVGZ') {
    $fmt3 = 'SELECTED';
} else {
    $fmt1 = 'SELECTED';
}

map {$chk{$_} = ''}
   qw(mistype1 mistype2 mistype3 showno1 cpgno1t cpgno1b revno1
      showcpg1 pospos1t pospos1b revpos1
      showno2 cpgno2t cpgno2b revno2
      showcpg2 pospos2t pospos2b revpos2
      showcpg pospos3t pospos3b
      showno4 cpgno4t cpgno4b revno4
      showcpg4 pospos4t pospos4b revpos4 circle4);

$chk{mistype1} = 'checked' if ($data->{mistype} == 1);
$chk{mistype2} = 'checked' if ($data->{mistype} == 2);
$chk{mistype3} = 'checked' if ($data->{mistype} == 3);
$chk{showno1}  = 'checked' if ($data->{showno1});
$chk{cpgno1t}  = 'checked' unless ($data->{cpgno1});
$chk{cpgno1b}  = 'checked' if ($data->{cpgno1});
$chk{revno1}   = 'checked' if ($data->{revno1});
$chk{showcpg1} = 'checked' if ($data->{showcpg1});
$chk{pospos1t} = 'checked' if ($data->{pospos1});
$chk{pospos1b} = 'checked' unless ($data->{pospos1});
$chk{revpos1}  = 'checked' if ($data->{revpos1});
$chk{showno2}  = 'checked' if ($data->{showno2});
$chk{cpgno2t}  = 'checked' unless ($data->{cpgno2});
$chk{cpgno2b}  = 'checked' if ($data->{cpgno2});
$chk{revno2}   = 'checked' if ($data->{revno2});
$chk{showcpg2} = 'checked' if ($data->{showcpg2});
$chk{pospos2t} = 'checked' if ($data->{pospos2});
$chk{pospos2b} = 'checked' unless ($data->{pospos2});
$chk{revpos2}  = 'checked' if ($data->{revpos2});
$chk{showcpg}  = 'checked' if ($data->{showcpg});
$chk{pospos3t} = 'checked' if ($data->{pospos3});
$chk{pospos3b} = 'checked' unless ($data->{pospos3});
$chk{showno4}  = 'checked' if ($data->{showno4});
$chk{cpgno4t}  = 'checked' unless ($data->{cpgno4});
$chk{cpgno4b}  = 'checked' if ($data->{cpgno4});
$chk{revno4}   = 'checked' if ($data->{revno4});
$chk{showcpg4} = 'checked' if ($data->{showcpg4});
$chk{pospos4t} = 'checked' if ($data->{pospos4});
$chk{pospos4b} = 'checked' unless ($data->{pospos4});
$chk{revpos4}  = 'checked' if ($data->{revpos4});
$chk{circle4}  = 'checked' if ($data->{circle4});

$data->{line}  = int(($data->{diame}+1)/2)
    if ($data->{line} > int(($data->{diame}+1)/2));

$url1 = sprintf SHOWURL, $data->{id}, $data->{pos}, $data->{eachw},
                         $data->{eachh}, $data->{diame}, $data->{line},
                         $data->{mistype}, $data->{showcpg1},
                         $data->{spos1}, $data->{revpos1}, $data->{pospos1},
                         $data->{showno1}, $data->{cpgno1}, $data->{revno1};

$height1  = $data->{eachh} * $num;

if ($data->{showcpg1}) {

    $posdi = $data->{eachh} / POSRATIO;

    if ($data->{revpos1}) {
         $min = $data->{glen} - $cpg[@cpg-1] - 1 + $data->{spos1};
         $max = $data->{glen} - $cpg[0]      - 1 + $data->{spos1};
    } else {
         $min = $cpg[0]      + $data->{spos1};
         $max = $cpg[@cpg-1] + $data->{spos1};
    }
    $mlen = length (abs($min)) > length (abs($max)) ? length (abs($min)) : length (abs($max));
    $mlen++ if ($min < 0);
}

$height1 += int ($posdi + $data->{diame} * FRATIO/2 * $mlen + 1)
    if ($data->{showcpg1});
$height1 += int (3*$data->{eachh}/4) if ($data->{showno1});

$height1++ if ($height1 - 2*int($height1/2));
$width1  = int ($data->{eachw} * $data->{cpgn} / $data->{scale}) || 1;
$height1 = int ($height1 / $data->{scale}) || 1;

$url2 = sprintf SHOW2URL, $data->{id}, $data->{pos}, $data->{eachw2},
                          $data->{eachh2}, $data->{diame2}, $data->{line2},
                          $data->{center}, $data->{showcpg2},
                          $data->{spos2}, $data->{revpos2}, $data->{pospos2},
                          $data->{showno2}, $data->{cpgno2}, $data->{revno2};

$height2  = $data->{eachh2} * $num;

if ($data->{showcpg2}) {

    $posdi = $data->{eachh2} / POSRATIO;

    if ($data->{revpos2}) {
         $min = $data->{glen} - $cpg[@cpg-1] - 1 + $data->{spos2};
         $max = $data->{glen} - $cpg[0]      - 1 + $data->{spos2};
    } else {
         $min = $cpg[0]      + $data->{spos1};
         $max = $cpg[@cpg-1] + $data->{spos1};
    }
    $mlen = length (abs($min)) > length (abs($max)) ? length (abs($min)) : length (abs($max));
    $mlen++ if ($min < 0);
}

$height2 += int ($posdi + $data->{diame2} * FRATIO/2 * $mlen + 1)
    if ($data->{showcpg2});
$height2 += int (3*$data->{eachh2}/4) if ($data->{showno2});

$height2++ if ($height2 - 2*int($height2/2));
$width2  = int (($data->{eachw2} * $data->{cpgn} + FIGMRG * 2) / $data->{scale2}) || 1;
$height2 = int ($height2 / $data->{scale2}) || 1;

$url3 = sprintf SHOW3URL, $data->{id}, $data->{pos},
                          $data->{eachh3}, $data->{diame3}, $data->{line3},
                          $data->{center2}, $data->{bscale}, $data->{showcpg}, $data->{pospos3};

$start = $stop = 0;

$start = int(($data->{diame3} + 1)/2) - 1 - ($cpg[0] -1) * $data->{bscale}
    if (($cpg[0] -1) * $data->{bscale} < int(($data->{diame3}+1)/2) - 1);

$stop = ($data->{glen} - $cpg[$data->{cpgn}-1] - 1) * $data->{bscale} + int(($data->{diame3}+1)/2) - 1
    if (($data->{glen} - $cpg[$data->{cpgn}-1] - 1) * $data->{bscale} < int(($data->{diame3}+1)/2) - 1);

$width3  = int (($start + $data->{glen} * $data->{bscale} + FIGMRG2 * 2 + $stop )/ $data->{scale3}) || 1;

$height3  = $data->{eachh3} * $num;
$height3 += $data->{eachh3} if ($data->{showcpg});
$height3  = int($height3 / $data->{scale3}) || 1;

$url4 = sprintf SHOW4URL, $data->{id}, $data->{pos},
                          $data->{eachh4}, $data->{diame4}, $data->{line4},
                          $data->{center3}, $data->{bscale2}, $data->{showcpg4},
                          $data->{spos4}, $data->{revpos4}, $data->{pospos4},
                          $data->{showno4}, $data->{cpgno4}, $data->{revno4}, $data->{circle4};

$height4  = $data->{eachh4} * $num;
$height4  = $data->{eachh4} if ($data->{circle4});

if ($data->{showcpg4}) {

    $posdi = $data->{eachh4} / POSRATIO;

    if ($data->{revpos4}) {
         $min = $data->{glen} - $cpg[@cpg-1] - 1 + $data->{spos4};
         $max = $data->{glen} - $cpg[0]      - 1 + $data->{spos4};
    } else {
         $min = $cpg[0]      + $data->{spos4};
         $max = $cpg[@cpg-1] + $data->{spos4};
    }
    $mlen = length (abs($min)) > length (abs($max)) ? length (abs($min)) : length (abs($max));
    $mlen++ if ($min < 0);
}

$height4 += int ($posdi + $data->{diame4} * FRATIO/2 * $mlen + 1)
    if ($data->{showcpg4});
$height4 += int (3*$data->{eachh4}/4) if ($data->{showno4});

$height4++ if ($height4 - 2*int($height4/2));
$width4  = int(($data->{cpgn} * $data->{diame4} + ($data->{glen} - 2*$data->{cpgn}) * $data->{bscale2} + FIGMRG2 * 2) / $data->{scale4}) || 1;
$height4 = int($height4 / $data->{scale4}) || 1;

printf HTML, FIGURL, $data->{id}, $data->{pos}, $data->{cpgn}, $data->{proj},
             $data->{cpgpos}, $data->{glen},
             $data->{optionShow}, $data->{figureShow}, $data->{cpgcheck},
             DOWNFIG,
             $fmt1, $fmt2, $fmt3,
             @chk{qw(mistype1 mistype2 mistype3 showno1 cpgno1t cpgno1b revno1)},
             $data->{eachw}, $data->{diame},
             @chk{qw(showcpg1 pospos1t pospos1b revpos1)},
             $data->{eachh}, $data->{line}, $data->{spos1}, $data->{scale},
             $help,
             $data->{center}, $data->{scale2},
             @chk{qw(showno2 cpgno2t cpgno2b revno2)},
             $data->{eachw2}, $data->{diame2},
             @chk{qw(showcpg2 pospos2t pospos2b revpos2)},
             $data->{eachh2}, $data->{line2}, $data->{spos2},
             $data->{center2},$data->{bscale}, $chk{showcpg}, $data->{diame3},
             $data->{scale3}, $chk{pospos3t}, $chk{pospos3b},
             $data->{eachh3}, $data->{line3},
             $data->{center3},$data->{bscale2},
             @chk{qw(showno4 cpgno4t cpgno4b revno4)},
             $data->{diame4}, $data->{scale4},
             @chk{qw(showcpg4 pospos4t pospos4b revpos4)},
             $data->{eachh4}, $data->{line4},
             $data->{spos4}, # start pos
             $chk{circle4},
             $url1, $width1, $height1,
             $url2, $width2, $height2,
             $url3, $width3, $height3,
             $url4, $width4, $height4,
;
###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
