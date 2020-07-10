#_*****************************************************************************
#_*                                                                           *
#_* File name: BFSetting.pm                                                   *
#_* Parameter moudule for QUMA                                                *
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
package BFSetting;

use 5.6.0;
use strict;
use warnings;
use Exporter;

############ Please change these values for your environment! ##################
                                                                               #
###  full path of this directory                                               #
use constant CGIDIR   => '/var/www/cgi-bin';                                   #
                                                                               #
###  full path of the needle program                                           #
use constant NEEDLE   => '/usr/local/bin/needle';                              #
                                                                               #
###  full path of the true type font                                           #
use constant FONTPATH => '/usr/X11R6/lib/X11/fonts/TTF/luximr.ttf';            #
#use constant FONTPATH => '/usr/share/X11/fonts/TTF/luximr.ttf';                #
#use constant FONTPATH => '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf';#
                                                                               #
###  full path of the data file directory                                      #
###  (necessary to writable from web server program)                           #
use constant DATADIR  => '/tmp/';                                              #
                                                                               #
###  full path of the temporary file directory                                 #
###  (necessary to writable from web server program)                           #
use constant TEMPDIR  => '/tmp/';                                              #
                                                                               #
###  URL path to the html file directory                                       #
use constant HTMLLOC  => '/';                                                  #
                                                                               #
###  URL path of this cgi-bin directory                                        #
use constant CGILOC   => '/cgi-bin';                                           #
                                                                               #
################################################################################

our (@ISA);
our (@EXPORT);

@ISA = qw (Exporter);
@EXPORT = qw (NEEDLE FONTPATH DATADIR TEMPDIR HL CL
	      CPGMAT FIGURL BFS STAT ALIDATA MAKEBI
              SHOWURL SHOW2URL SHOW3URL SHOW4URL
              DATAURL SGLURL SGLURL2
              CPGFIG1 CPGFIG2 CPGFIG3 CPGFIG4
	      CPGFIG5 CPGFIG6 CPGOPT
	      COMPFIG1 COMPFIG2 COMPFIG3 COMPFIG4
	      COMPFIG5 COMPFIG6 COMPFIG7 COMPFIG8 COMPOPT
	      MALIGN REPHEAD REPHEADS REPHEA2 REPHEAS2
              REPFIG REPDOWN
	      REPDOWNO REP2DOWN REP3DOWN REP4DOWN
	      REPCPGG1 REPCPGG2 REPCPGG3 REPCPGG4
	      REPCPGG5 REPCPGG6
	      REPCOMP1 REPCOMP2 REPCOMP3 REPCOMP4
	      REPCOMP5 REPCOMP6 REPCOMP7 REPCOMP8
	      REPALI SHOWMALI
	      PLATFORM UNCONVL PCONVL MISL PERCL
	      NDLOPT
	      EACHW  EACHH  DIAME  LINEW
              EACHW2 EACHH2 DIAME2 LINEW2 SCALE
              EACHW3 EACHH3 DIAME3 LINEW3 SCALE3 CLINEW
              EACHH4 DIAME4 LINEW4 SCALE4 CLINEW2 BSCALE
              EACHH5 DIAME5 LINEW5 SCALE5 CLINEW3 BSCALE2
	      SPOS POSRATIO FRATIO MISTYPE
              FIGMRG LINEMRG FIGMRG2 LINE
	      POSDIS SPNUM NAMEG
	      RENEW GETFIG DOWNFIG RSTPARA
	      DOWNCPGG DOWNCPGD DOWNSTATD DOWNALID SAVE MALI
              CPGROWL1 CPGROWL2
	      FONTWRP FONTXXS FONTXS FONTS
	      WINMRGW WINMRGH
	      MARGL MARGL2 MARGR HIGHT HIGHT2 BMARG HLINE LFMARG LFMARG2
	      FONTH1 FONTH2 GMARGB GMARGB2 GMARGH LLABLEN LLABMRG
	      GWIDTH GWIDTH2 GLEGW
              CONVER
	      GFILEL GSEQL BSEQL BSEQN
	      SEQFILES
	      IPCONV
	      );

use constant HL => HTMLLOC =~ /\/$/ ? substr HTMLLOC, 0, length(HTMLLOC) - 1 : HTMLLOC;
use constant CL => CGILOC  =~ /\/$/ ? substr CGILOC,  0, length(CGILOC ) - 1 : CGILOC ;
use constant CPGMAT   => CGIDIR . '/EDNA_CPG';
use constant FIGURL   => CL . '/makeAllBiFig.cgi';
use constant SHOWBASE => CL . '/showAllBiFig.cgi';
use constant SHOW2BAS => CL . '/showAllBiFig2.cgi';
use constant SHOW3BAS => CL . '/showAllBiFig3.cgi';
use constant SHOW4BAS => CL . '/showAllBiFig4.cgi';
use constant BFS      => CL . '/makeBiFig.cgi';
use constant STAT     => CL . '/makeStatData.cgi';
use constant ALIDATA  => CL . '/downAliData.cgi';
use constant MAKEBI   => CL . '/makeBisulfiteData.cgi';
use constant CPGFIG1  => CL . '/makeCpGFig.cgi';
use constant CPGFIG2  => CL . '/makeCpGFig2.cgi';
use constant CPGFIG3  => CL . '/makeCpGFig3.cgi';
use constant CPGFIG4  => CL . '/makeCpGFig4.cgi';
use constant CPGFIG5  => CL . '/makeCpGFig5.cgi';
use constant CPGFIG6  => CL . '/makeCpGFig6.cgi';
use constant CPGOPT   => '?id=%s&amp;len=%d&amp;pos=%s&amp;val=%s';
use constant COMPFIG1 => CL . '/makeCompFig1.cgi';
use constant COMPFIG2 => CL . '/makeCompFig2.cgi';
use constant COMPFIG3 => CL . '/makeCompFig3.cgi';
use constant COMPFIG4 => CL . '/makeCompFig4.cgi';
use constant COMPFIG5 => CL . '/makeCompFig5.cgi';
use constant COMPFIG6 => CL . '/makeCompFig6.cgi';
use constant COMPFIG7 => CL . '/makeCompFig7.cgi';
use constant COMPFIG8 => CL . '/makeCompFig8.cgi';
use constant MALIGN   => CL . '/makeMAli.cgi';
use constant COMPOPT  => '?id=%s&amp;len=%d&amp;pos=%s&amp;val1=%s&amp;val2=%s';
use constant SHOWURL  => SHOWBASE . '?id=%s&amp;pos=%s&amp;eachw=%d&amp;eachh=%d&amp;diame=%d&amp;line=%d&amp;mistype=%d&amp;showcpg1=%s&amp;spos1=%s&amp;' .
                         'revpos1=%s&amp;pospos1=%s&amp;showno1=%s&amp;cpgno1=%s&amp;revno1=%s';
use constant SHOW2URL => SHOW2BAS . '?id=%s&amp;pos=%s&amp;eachw=%d&amp;eachh=%d&amp;diame=%d&amp;line=%d&amp;center=%d&amp;showcpg2=%s&amp;spos2=%s&amp;' .
                         'revpos2=%s&amp;pospos2=%s&amp;showno2=%s&amp;cpgno2=%s&amp;revno2=%s';
use constant SHOW3URL => SHOW3BAS . '?id=%s&amp;pos=%s&amp;eachh=%d&amp;diame=%d&amp;line=%d&amp;center=%d&amp;bscale=%d&amp;showcpg=%s&amp;pospos3=%s';
use constant SHOW4URL => SHOW4BAS . '?id=%s&amp;pos=%s&amp;eachh=%d&amp;diame=%d&amp;line=%d&amp;center=%d&amp;bscale=%d&amp;showcpg4=%s&amp;spos4=%s&amp;' .
                         'revpos4=%s&amp;pospos4=%s&amp;showno4=%s&amp;cpgno4=%s&amp;revno4=%s&amp;circle4=%s';
use constant DATAURL  => CL . '/showData.cgi?id=%s&amp;pos=%d&amp;cpgcheck=%s';
use constant SGLURL   => SHOWBASE . '?id=%s&amp;pos=%d&amp;eachw=9&amp;eachh=21&amp;diame=7&amp;line=1';
use constant SGLURL2  => SHOWBASE . '?id=%s&amp;pos=%d&amp;eachw=7&amp;eachh=21&amp;diame=5&amp;line=1';
use constant REPHEAD  => 'Location: ' . BFS      . "?id=\%s&unconv=\%d&mis=\%d&perc=\%f&pconv=\%f&conv=\%d&cpgcheck=\%s&uniq=\%s\n\n";
use constant REPHEADS => 'Location: ' . STAT     . "?id=\%s&unconv=\%d&mis=\%d&perc=\%f&pconv=\%f&conv=\%d&cpgcheck=\%s&uniq=\%s\n\n";
use constant REPHEA2  => 'Location: ' . BFS      . "?id=\%s&\%s\n\n";
use constant REPHEAS2 => 'Location: ' . STAT     . "?id=\%s&\%s\n\n";
use constant REPFIG   => 'Location: ' . FIGURL   . "?id=\%s&pos=\%s&cpgn=\%d&proj=\%s&cpgpos=\%s&glen=\%d&showcpg=on&cpgcheck=\%s\n\n";
use constant REPDOWN  => 'Location: ' . SHOWBASE . "?id=\%s&pos=\%s&down=1&proj=\%s\n\n";
use constant REPDOWNO => 'Location: ' . SHOWBASE . "?id=\%s&format=\%s&pos=\%s&down=1" .
                         "&eachw=\%d&eachh=\%d&diame=\%d&line=\%d&proj=\%s&mistype=\%d&showcpg1=\%s&spos1=\%s&revpos1=\%s&pospos1=\%s" .
                         "&showno1=\%s&cpgno1=\%s&revno1=\%s\n\n";
use constant REP2DOWN => 'Location: ' . SHOW2BAS . "?id=\%s&format=\%s&pos=\%s&down=1" .
                         "&eachw=\%d&eachh=\%d&diame=\%d&line=\%d&proj=\%s&center=\%s&showcpg2=\%s&spos2=\%s&revpos2=\%s&pospos2=\%s" .
                         "&showno2=\%s&cpgno2=\%s&revno2=\%s\n\n";
use constant REP3DOWN => 'Location: ' . SHOW3BAS . "?id=\%s&format=\%s&pos=\%s&down=1" .
                         "&eachh=\%d&diame=\%d&line=\%d&proj=\%s&center=\%s&bscale=\%d&showcpg=\%s&pospos3=\%s\n\n";
use constant REP4DOWN => 'Location: ' . SHOW4BAS . "?id=\%s&format=\%s&pos=\%s&down=1" .
                         "&eachh=\%d&diame=\%d&line=\%d&proj=\%s&center=\%s&bscale=\%d&showcpg4=\%s&spos4=\%s&revpos4=\%s&pospos4=\%s" .
                         "&showno4=\%s&cpgno4=\%s&revno4=\%s&circle4=\%s\n\n";
use constant REPCPGG1 => 'Location: ' . CPGFIG1 . "?id=\%s&down=1&len=\%d&pos=\%s&val=\%s&proj=\%s&format=\%s\n\n";
use constant REPCPGG2 => 'Location: ' . CPGFIG2 . "?id=\%s&down=1&len=\%d&pos=\%s&val=\%s&proj=\%s&format=\%s\n\n";
use constant REPCPGG3 => 'Location: ' . CPGFIG3 . "?id=\%s&down=1&len=\%d&pos=\%s&val=\%s&proj=\%s&format=\%s\n\n";
use constant REPCPGG4 => 'Location: ' . CPGFIG4 . "?id=\%s&down=1&len=\%d&pos=\%s&val=\%s&proj=\%s&format=\%s\n\n";
use constant REPCPGG5 => 'Location: ' . CPGFIG5 . "?id=\%s&down=1&len=\%d&pos=\%s&val=\%s&proj=\%s&format=\%s\n\n";
use constant REPCPGG6 => 'Location: ' . CPGFIG6 . "?id=\%s&down=1&len=\%d&pos=\%s&val=\%s&proj=\%s&format=\%s\n\n";
use constant REPCOMP1 => 'Location: ' . COMPFIG1 . "?id=\%s&down=1&len=\%d&pos=\%s&val1=\%s&val2=\%s&proj=\%s&format=\%s\n\n";
use constant REPCOMP2 => 'Location: ' . COMPFIG2 . "?id=\%s&down=1&len=\%d&pos=\%s&val1=\%s&val2=\%s&proj=\%s&format=\%s\n\n";
use constant REPCOMP3 => 'Location: ' . COMPFIG3 . "?id=\%s&down=1&len=\%d&pos=\%s&val1=\%s&val2=\%s&proj=\%s&format=\%s\n\n";
use constant REPCOMP4 => 'Location: ' . COMPFIG4 . "?id=\%s&down=1&len=\%d&pos=\%s&val1=\%s&val2=\%s&proj=\%s&format=\%s\n\n";
use constant REPCOMP5 => 'Location: ' . COMPFIG5 . "?id=\%s&down=1&len=\%d&pos=\%s&val1=\%s&val2=\%s&proj=\%s&format=\%s\n\n";
use constant REPCOMP6 => 'Location: ' . COMPFIG6 . "?id=\%s&down=1&len=\%d&pos=\%s&val1=\%s&val2=\%s&proj=\%s&format=\%s\n\n";
use constant REPCOMP7 => 'Location: ' . COMPFIG7 . "?id=\%s&down=1&len=\%d&pos=\%s&val1=\%s&val2=\%s&proj=\%s&format=\%s\n\n";
use constant REPCOMP8 => 'Location: ' . COMPFIG8 . "?id=\%s&down=1&len=\%d&pos=\%s&val1=\%s&val2=\%s&proj=\%s&format=\%s\n\n";
use constant REPALI   => 'Location: ' . ALIDATA . "?id=\%s&cpgcheck=\%s\n\n";
use constant SHOWMALI => 'Location: ' . MALIGN . "?id=%s&pos=%s&cpgcheck=%s\n\n";
use constant PLATFORM => 'Unix';
use constant UNCONVL  => 5;
use constant PCONVL   => 95.0;
use constant MISL     => 10;
use constant PERCL    => 90.0;
use constant NDLOPT   => ' -stdout -auto -gapopen 10.0 -gapextend 0.5 ' .
                         '-aformat markx3 -datafile ' . CPGMAT . '|';
use constant EACHW    => 100;
use constant EACHH    => 100;
use constant DIAME    => 81;
use constant LINEW    => 5;
use constant EACHW2   => 40;
use constant EACHH2   => 40;
use constant DIAME2   => 33;
use constant LINEW2   => 2;
use constant SCALE    => 2;
use constant EACHW3   => 36;
use constant EACHH3   => 40;
use constant DIAME3   => 27;
use constant LINEW3   => 2;
use constant CLINEW   => 3;
use constant SCALE3   => 2;
use constant EACHH4   => 40;
use constant DIAME4   => 27;
use constant LINEW4   => 2;
use constant CLINEW2  => 3;
use constant SCALE4   => 2;
use constant BSCALE   => 2;
use constant EACHH5   => 40;
use constant DIAME5   => 27;
use constant LINEW5   => 2;
use constant CLINEW3  => 3;
use constant SCALE5   => 2;
use constant BSCALE2  => 2;
use constant SPOS     => 1;
use constant POSRATIO => 2;
use constant FRATIO   => 7 / 9;
use constant MISTYPE  => 1;
use constant FIGMRG   => 10;
use constant LINEMRG  =>  5;
use constant FIGMRG2  =>  5;
use constant LINE     => 60;
use constant POSDIS   => 10;
use constant SPNUM    => 5;
use constant NAMEG    => 'Genomic';
use constant RENEW    => 'Renew';
use constant GETFIG   => 'Show figure';
use constant DOWNFIG  => 'Download figure';
use constant RSTPARA  => 'Reset with new parameters';
use constant DOWNCPGG => 'Download graph';
use constant DOWNCPGD => 'Methylation status data';
use constant DOWNSTATD=> 'Statistical data';
use constant DOWNALID => 'All alignment data';
use constant SAVE     => 'Save analysis to restore file';
use constant MALI     => 'Mulitple alignment';
use constant CPGROWL1 => 18;
use constant CPGROWL2 => 15;
use constant FONTS    => 40;
use constant FONTXS   => 60;
use constant FONTXXS  => 80;
use constant FONTWRP  => 90;
use constant WINMRGW  => 200;
use constant WINMRGH  => 250;

use constant MARGL    => 100;
use constant MARGL2   => 120;
use constant MARGR    => 10;
use constant HIGHT    => 125;
use constant HIGHT2   => 130;
use constant BMARG    => 11;
use constant HLINE    => 3;
use constant LFMARG   => 10;
use constant LFMARG2  => 5;
use constant FONTH1   => 4;
use constant FONTH2   => 7;
use constant GMARGB   => 20;
use constant GMARGB2  => 23;
use constant GMARGH   => 7;
use constant LLABLEN  => 25;
use constant LLABMRG  => 15;
use constant GWIDTH   => 11;
use constant GWIDTH2  => 10;
use constant GLEGW    => 20;

use constant CONVER   => 'The input genomic sequence seems to have converted. Did you really use unconverted genome sequence?';
use constant GFILEL   => 0;
use constant GSEQL    => 0;
use constant BSEQL    => 0;
use constant BSEQN    => 0;
use constant SEQFILES => [{file => CGIDIR . "/seqfile/sample_genome_gb.txt", name => "sample_genome_gb.txt", mime => 'text/plain'},               # 0
			  {file => CGIDIR . "/seqfile/sample_genome_fasta.txt", name => "sample_genome_fasta.txt", mime => 'text/plain'},         # 1
			  {file => CGIDIR . "/seqfile/sample_genome_plain_seq.txt", name => "sample_genome_plain_seq.txt", mime => 'text/plain'}, # 2
			  {file => CGIDIR . "/seqfile/Gm9_J1_multi_fasta.txt", name => "Gm9_J1_multi_fasta.txt", mime => 'text/plain'},           # 3
			  {file => CGIDIR . "/seqfile/Gm9_J1_plain_seq.zip", name => "Gm9_J1_plain_seq.zip", mime => 'application/zip'},          # 4
			  {file => CGIDIR . "/seqfile/Gm9_J1_fasta_seq.zip", name => "Gm9_J1_fasta_seq.zip", mime => 'application/zip'},          # 5
			  {file => CGIDIR . "/seqfile/Gm9_16aabb_multi_fasta.txt", name => "Gm9_16aabb_multi_fasta.txt", mime => 'text/plain'},   # 6
			  {file => CGIDIR . "/seqfile/Gm9_16aabb_plain_seq.zip", name => "Gm9_16aabb_plain_seq.zip", mime => 'application/zip'},  # 7
			  {file => CGIDIR . "/seqfile/Gm9_16aabb_fasta_seq.zip", name => "Gm9_16aabb_fasta_seq.zip", mime => 'application/zip'},  # 8
		  ];
use constant IPCONV    => CGIDIR . '/IPConvFile.txt';

###########################  End of Main ######################################
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
