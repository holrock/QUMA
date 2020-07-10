README file for source code of the QUMA                    5/15/2019


ABSTRACT:

QUMA (QUantification tool for Methylation Analysis) is interactive and
easy-to-use web-based tool for the bisulfite sequencing analysis of
CpG methylation. QUMA includes most of the data-processing functions
necessary for the analysis of bisulfite sequences. It also provides
a platform for consistent quality control of the analysis.
The QUMA web server is available at <http://quma.cdb.riken.jp/>.

COPYRIGHT INFO:

The QUMA source code is copyright 2008-2019, Yuichi Kumaki. This is
released under the GNU General Public License (GPLv3)

These programs are free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

These programs are distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with these programs. If not, see <http://www.gnu.org/licenses/>.


PREREQUISITES:

The QUMA is written in Perl and can be installed locally. We tested
that the QUMA can work at many Linux distributions, Mac OS X and
Windows 2000/XP (with cygwin), and will probably work at any
UNIX-like OS.

(1) Perl open source scripting language
    <http://www.cpan.org/src/README.html>
    You need version 5.6.0 or higher.

(2) Web server program
    The QUMA will probably work with many web server programs which
    enable to run a perl CGI script. But, we only tested Apache web
    server program (both version 1.3 and version 2.2).
    <http://httpd.apache.org/dist/httpd/>

(3) Perl modules
    Some of these modules may require additional libraries and/or perl modules.

 (a) CGI::Lite
     <http://search.cpan.org/CPAN/modules/by-module/CGI/CGI-Lite-2.02.tar.gz>

 (b) Compress::Zlib
     <http://search.cpan.org/CPAN/modules/by-module/Compress/Compress-Zlib-2.015.tar.gz>

 (c) Archive::Zip
     <http://search.cpan.org/CPAN/modules/by-module/Archive/Archive-Zip-1.24.tar.gz>

 (d) RTF::Parser
     <http://search.cpan.org/CPAN/modules/by-module/RTF/RTF-Parser-1.09.tar.gz>

 (e) GD
     <http://search.cpan.org/CPAN/modules/by-module/GD/GD-2.41.tar.gz>
     You need version 2.07 or higher (and libgd version 2.0.12 or higher).

 (f) GD::SVG
     <http://search.cpan.org/CPAN/modules/by-module/GD/GD-SVG-0.31.tar.gz>

 (g) SVG
     <http://search.cpan.org/CPAN/modules/by-module/SVG/SVG-2.44.tar.gz>

 (h) Statistics-Lite
     <http://search.cpan.org/CPAN/modules/by-module/Statistics/Statistics-Lite-3.2.tar.gz>

 (i) Bio-Trace-ABIF
     <http://search.cpan.org/CPAN/modules/by-module/Bio/Bio-Trace-ABIF-1.05.tar.gz>

(4) needle program of the EMBOSSS software package
    <httd://emboss.sourceforge.net/>


INSTALLATION:

Installation and setting up of the QUMA is not difficult but skill to
set up a UNIX/Linux web server is required. Installation to Windows
or Mac OS X is more difficult than general Linux distributions,
because some additional installations are required to setting up the
prerequisites.


(1) Change the permission of files/directories in "htdocs" directory as
    readable from web server program.

(2) Change the permission of files/directories in "cgi-bin" directory as
    executable from web server program.

(3) Move all files/directories in "htdocs" directory to web server's
    DocumentRoot directory.
    If necessary, change the "index.html" and "index_j.html" to other
    file name.

(4) Move all files in "cgi-bin" directory to web server's cgi-bin
    directory.

(5) Change the setting of the paths of "cgi-bin" directory, needle
    program and true type font by editing the BFSetting.pm file in
    "cgi-bin" directory.
    (a) If necessary, change some other paths at BFSetting.pm file.
    (b) At UNIX/Linux OS with the X Window System, path of true type
        font (monospace font is recommended) is usually 
           /usr/X11R6/lib/X11/fonts/TTF/luximr.ttf
        or /usr/share/X11/fonts/TTF/luximr.ttf
        or /usr/share/fonts/truetype/freefont/FreeMonoBold.ttf
        If true type font is not exists in your system, you can
        download from
        <http://xorg.freedesktop.org/release/individual/font/font-bh-ttf-1.0.0.tar.bz2>        

(6) If necessary, comment out the "AddDefaultCharset" line of the
    web server's configuration file. Then restart the web server
    program.


WHAT'S NEW:

05/15/2019      1.1.16
                 Minor modification.
07/19/2014      1.1.15
                 Minor modification.
01/16/2014      1.1.14
                 Minor modification.
04/09/2013      1.1.13
                 Minor modification.
10/25/2012      1.1.12
                 Minor bug fixed.
08/23/2012      1.1.11
                 ABI format file (with ".ab1" extension) is now acceptable for bisuflite sequece file.
05/23/2012      1.1.10
                 Exclude identical bisulfite sequences option is added.
01/13/2012      1.1.9
                 Minor bug fixed.
09/14/2011      1.1.8
                 Minor bug fixed.
01/29/2011      1.1.7
                 Strict CpG site check option for repeptive sequence analysis is added.
11/12/2010      1.1.6
                 Performance of Fisher's exact test is improved.
06/14/2010      1.1.5
                 Minor bug fixed.
02/02/2010      1.1.4
                 Minor modification.
02/04/2009      1.1.3
                 Bug of the conversion options ("G => A conversion" and "Both") are fiexed.
01/30/2009      1.1.2
                 Minor bug fix.
01/28/2009      1.1.1
      	         Bug of the "G => A conversion" option is fixed.
01/08/2009      1.1.0
                 1. Support of "Save and Restore" function.
                 2. Multiple-alignment format display added.
                 3. Support of circle graph style methylation pattern figure.
                 4. CpG number display function at the methylation pattern
                    figures added.
                 5. Standard deviation (S.D) and standard error (S.E.) indicated
                    at the CpG methylation status.
                 6. Some of minor modification.
09/25/2008      1.0.2
                 1. Support of SVG and SVGZ file formats for graphical data
                    download.
                 2. Minor changes of web codes.
05/02/2008      1.0.1
                 1. More options about CpG positions added to the function
                    of making methylation pattern figure.
                 2. Function of addition/replacemnt of bisulfite seqeunces is
                    added to the result page of the methylation status analysis
                    mode.
                 3. Acknowledgements section updated.
                 4. "Links" section now available and "Acknowledgements" section
                    was integrated into "Reference" section.
                 5. Minor bug fixed and description updated.
04/17/2008      1.0.0
	         First open source version.


CONTACT:

Yuichi Kumaki & Masaki Okano
quma@cdb.riken.jp
<http://quma.cdb.riken.jp/>


REFERENCE:

QUMA: quantification tool for methylation analysis
Yuichi Kumaki, Masaaki Oda &amp; Masaki Okano*, Nucleic Acids Res. 36, W170-W175 (2008).
<http://dx.doi.org/10.1093/nar/gkn294>
PubMed Central ID: PMC2447804, PubMed ID: 18487274

*To whom correspondence should be addressed.
Correspondence may also be addressed to Yuichi Kumaki.


ACKNOWLEDGEMENTS:

We thank Akiko Yamagiwa for sample bisulfite sequences of the mouse
Gm9 region (1), Morito Sakaue and Masahumi Kawaguchi for constructive
feedback on the website, Hazuki S. Hiraga for proofreading of the
web site, Yoko Dote for helpful feedback on the "Terms of Use"
section, and the Information Networks Office of RIKEN Kobe Institute
for helpful suggestions in setting up the Internet connection for
the server. This work was supported in part by Grants-in-Aid from
the Ministry of Education, Culture, Sports, Science, and Technology
of Japan to M. Okano.

(1) Oda, M., Yamagiwa, A., Yamamoto, S., Nakayama, T., Tsumura, A.,
    Sasaki, H., Nakao, K., Li, E. and  Okano, M.
    DNA methylation regulates long-range gene silencing of an
    X-linked homeobox gene cluster in a lineage-specific manner.
    Genes & Development, 20, 3382-3394 (2006).
    <http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&amp;db=PubMed&amp;dopt=Citation&amp;list_uids=17182866>


AUTHOR:

Yuichi Kumaki
yuichi@kumaki.jp
