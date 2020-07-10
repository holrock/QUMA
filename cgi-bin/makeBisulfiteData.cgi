#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: makeBisulfiteData.cgi                                          *
#_* cgi for processing input data (but not create HTML)                       *
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

my ($time   );
my ($id     );
my ($dfh    );
my ($cgi    );
my ($data   );
my ($gen    );
my (@gen    );
my (@que    );
my (@oseq   );
my ($rfile  );
my ($gfile  );
my ($biseq1 );
my ($biseq2 );
my ($genseq );
my ($in     );
my (@in     );
my (@out    );
my ($i      );
my (%parame );
my ($numc   );
my ($numg   );
my ($numcg  );
my ($conv   );
my (@biseq  );
my (@biseq2 );
my ($num    );
my ($static );
my (@pos    );
my ($pos    );
my ($len    );
my ($cpgf   );
my ($cpgr   );
my ($gfileF );
my ($gfileR );
my ($qfileF );
my ($qfileR );
my ($gfilepF);
my ($gfilepR);
my ($qfilepF);
my ($qfilepR);
my ($fa     );
my ($ffres  );
my ($frres  );
my ($rfres  );
my ($rrres  );
my ($fres   );
my ($rres   );
my ($res    );
my ($fdir   );
my ($rdir   );
my ($dir    );
my ($gdir   );
local ($_   );
local ($!   );

$time = makeTime;
$id = sprintf "$time%06d", $$;
$id .= join '', map {sprintf "%02X", $_} split /\./, $ENV{REMOTE_ADDR};

$cgi = new CGI::Lite;
$cgi->set_directory (TEMPDIR)
    or errorAndExit ('File access error!', 'File access error!', "Set directory error : $! : " . TEMPDIR);

$cgi->set_platform(PLATFORM);
$cgi->set_buffer_size ($ENV{CONTENT_LENGTH});
$cgi->filter_filename (\&convName);
$data = $cgi->parse_form_data;

errorAndExit ('Unknown error!', 'Unknown error!', "CGi error : \$cgi->is_error() : " . $cgi->get_error_message())
    if ($cgi->is_error());

if (exists $data->{id}) {

    ipCheck ($data);

    open $dfh, DATADIR . $data->{id}
	or errorAndExit ('File access error!',
			 'File access error!',
			 "File access error : $! : " . DATADIR . $data->{id});

    chomp ($gen = <$dfh>);
    @gen = split /\t/, $gen;
    shift @gen;
    $data->{project} = shift @gen;
    $data->{gname1}  = shift @gen;
    $data->{gname2}  = shift @gen;
    $data->{convdir} = shift @gen;
    $genseq          = shift @gen;

    if ($data->{resubtype}) {
	while (<$dfh>) {
	    @que = split /\t/;
	    push @oseq, {com => $que[1], seq => $que[2]};
	}
    }

    close $dfh;

    errorAndExit ('Please try again!',
		  'Sorry, unfortunately bisulfite sequence was not transferd well. Please try again!', 
		  "No bisulfite sequence! : $0 line 145")
	unless ($data->{biseq1});

    $biseq1 = $data->{biseq1};

    if (-e TEMPDIR . $biseq1 && ! -s TEMPDIR . $biseq1) {
	unlink TEMPDIR . $biseq1
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$biseq1 : $!");
    }

} elsif (exists $data->{ressub}) {

    errorAndExit ('Please try again!',
		  'Sorry, unfortunately QUMA restore file not transferd well. Please try again!', 
		  "No restore file! ; $0 line 160")
	unless ($data->{restorefile});

    $rfile  = $data->{restorefile};

    unless (-e TEMPDIR . $rfile) {
	errorAndExit ('Please try again!',
		      'Sorry, unfortunately QUMA save file was not transferd well. Please try again!', 
		      "No quma data file; $0 line 190");
    }

    unless (-s TEMPDIR . $rfile  && -B TEMPDIR . $rfile) {
	unlink TEMPDIR . $rfile
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$rfile : $!; $0 line 174");

	errorAndExit ('Invalid QUMA restore file format', 'Invalid QUMA restore file format',
		      "Invalid QUMA restore file format: size = 0 or text file; $0 line 177");
    }

    unless ($rfile =~ /\.qma$/i) {
	unlink TEMPDIR . $rfile
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$rfile : $!; $0 line 183");

	errorAndExit ('Please try again!',
		      'The file name must have the suffix ".qma"! Please try again!', 
		      "No quma data file; $0 line 187");
    }


    open $dfh, TEMPDIR . $rfile
	or errorAndExit ('File access error!', 'File access error!',
			 "File access error : $! : " . TEMPDIR ."$rfile; $0 line 193");

    $| = 1;

    defined (sysread ($dfh, $in, -s TEMPDIR . $rfile))
	or errorAndExit ('File access error!', 'File access error!',
			 "File sysread error : $! : " . TEMPDIR ."$rfile; $0 line 199");

    close $dfh;

    unlink TEMPDIR . $rfile
	or errorAndExit ('File access error!', 'File access error!', 
			 "File access error! : Can't unlink " . TEMPDIR . "$rfile : $!; $0 line 205");

    use Compress::Zlib;

    defined ($in = Compress::Zlib::memGunzip $in)
	or errorAndExit ('Invalid QUMA save file format', 'Invalid QUMA save file format',
			 "Invalid QUMA save file format at gunzip: $0 line 211");

    open $dfh, '>' . DATADIR . $id
	or errorAndExit ('File access error!', 'File access error!',
			 "File access error : $! : " . DATADIR . "$id: $0 line 215");

    @in = split /\n/, $in;
    $in = shift @in;

    $in eq "QUMA_data_file"
	or errorAndExit ('Invalid QUMA save file format', 'Invalid QUMA save file format',
			 "Invalid QUMA save file format: no header: $0 line 222");

    $in = shift @in;
    $in =~ /^genome\t([^\t]*\t){3}\d\t\w+(\t\d+)+$/
	or errorAndExit ('Invalid QUMA save file format', 'Invalid QUMA save file format',
			 "Invalid QUMA save file format: invalid genome data: $in : $0 line 227");

    push @out, $in;

    $i = 0;
    while ($in = shift @in) {
	$i++;
	if ($in =~ /^=====\t(\d)$/) {
	    $static = $1 == 1 ? 0 : 1;
	    last;
	}

	$in =~ /^$i\t[^\t]*(\t[\w-]+){3}(\t\d+){3}(\.\d+)?(\t\d+){5}(\.\d+)?\t[\w+-]+(\t-?\d+){2}(\tS\t\d)?$/
	    or errorAndExit ('Invalid QUMA save file format', 'Invalid QUMA save file format',
			     "Invalid QUMA save file format: invalid bisulfite data : $in : $0 line 241");

	push @out, $in;
    }

    defined $static
	or errorAndExit ('Invalid QUMA save file format', 'Invalid QUMA save file format',
			 "Invalid QUMA save file format: invalid delimiter line: $0 line 248");

    print $dfh map {"$_\n"} @out;
    close $dfh;

    while ($in = shift @in) {
	@out = split /\t/, $in;
	$parame{$out[0]} = $out[1];
    }

    delete $parame{id};

    if ($static) {
	printf REPHEAS2, $id, join ("&", map {"$_=$parame{$_}"} grep {/^\w+$/} keys %parame);

    } else {
	printf REPHEA2,  $id, join ("&", map {"$_=$parame{$_}"} grep {/^\w+$/} keys %parame);
    }
    exit;

} else {

    errorAndExit ('Please try again!',
		  'Sorry, unfortunately genome sequence was not transferd well. Please try again!', 
		  "No genome sequence! ; $0 line 272")
	unless ($data->{genomefile} || $data->{genome} || $data->{sampleData});

    errorAndExit ('Please try again!',
		  'Sorry, unfortunately bisulfite sequence was not transferd well. Please try again!', 
		  "No bisulfite sequence! : $0 line 277")
	unless ($data->{biseq1} || $data->{multifasta} || $data->{sampleData});

    $gfile  = $data->{genomefile};
    $biseq1 = $data->{biseq1};
    $biseq2 = $data->{biseq2};

    if ($gfile && -e TEMPDIR . $gfile && ! -s TEMPDIR . $gfile) {
	unlink TEMPDIR . $gfile
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$gfile : $!");
    }

    if ($biseq1 && -e TEMPDIR . $biseq1 && ! -s TEMPDIR . $biseq1) {
	unlink TEMPDIR . $biseq1
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$biseq1 : $!");
    }

    if ($biseq2 && -e TEMPDIR . $biseq2 && ! -s TEMPDIR . $biseq2) {
	unlink TEMPDIR . $biseq2
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$biseq2 : $!");
    }
    unless ($data->{optionShow}) {

	if ($gfile && -e TEMPDIR . $gfile && -s TEMPDIR . $gfile) {
	    $data->{genome} = '';
	} else {
	    $gfile = $data->{genomefile};
	}

	if ($biseq1 && -e TEMPDIR . $biseq1 && -s TEMPDIR . $biseq1) {
	    $data->{multifasta} = '';
	} else {
	    $biseq1 = $data->{biseq1};
	}

	if ($biseq2 && -e TEMPDIR . $biseq2 && -s TEMPDIR . $biseq2) {
	    $data->{multifasta2} = '';

	} else {
	    $biseq2 = $data->{biseq2};
	}
    }

    unless ($genseq = parseGenome ($data->{genome}, $gfile)) {
	if ($data->{sampleData}) {
	    $genseq = parseGenome (getSampleSeq (2), '');

	} else {
	    errorAndExit ('No valid genome sequence data is present.',
			  'No valid genome sequence data is present.',
			  'No valid genome sequence data is present.');
	}
    }
}

$numc = $numg = $numcg = $conv = 0;
$numc  = $genseq =~ y/C/C/;
$numg  = $genseq =~ y/G/G/;
$numcg = $genseq =~ s/CG/CG/g;

$conv = 1 if ($numc <= $numcg || $numg <= $numcg);

unless (@biseq = parseBiseq ($data->{multifasta}, $biseq1)) {
    if ($data->{sampleData}) {
        @biseq = parseBiseq (getSampleSeq (3), '');

    } else {
        errorAndExit ('No valid bisulfite sequence data is present.',
		      'No valid bisulfite sequence data is present.',
 		      'No valid bisulfite sequence data is present.');
    }
}

push @biseq, @oseq;

$num = @biseq;

if (! $data->{multifasta} && ! $data->{multifasta2} && ! $data->{sampleData} &&
    $biseq1 && $biseq2 && $biseq1 eq $biseq2) {
    @biseq2 = @biseq;
} else {
    @biseq2 = parseBiseq ($data->{multifasta2}, $biseq2);
}

if (@biseq2) {
    push @biseq, @biseq2;
    $static = 1;
}

$pos  = -1;
$cpgf = {};
$cpgr = {};
$len = length $genseq;

while (($pos = index $genseq, 'CG', ++$pos) != -1) {
    push @pos, $pos;
    $cpgf->{$pos} = 1;
    $cpgr->{$len - $pos - 2} = 1;
}

open $dfh, '>' . DATADIR . $id
    or errorAndExit ('File access error!', 'File access error!', "File access error : $! : " . DATADIR . $id);

$data->{convdir} ||= 0;
$data->{project} ||= '';
$data->{project} =~ y/&;`'"|*?~<>^()[]{}$\\\n\r//d;
$data->{project} =~ s/[^\w-]//g;
$data->{gname1}  ||= '';
$data->{gname2}  ||= '';
$data->{gname1}  =~ y/&;`'"|*?~<>^()[]{}$\\\n\r//d;
$data->{gname2}  =~ y/&;`'"|*?~<>^()[]{}$\\\n\r//d;

print $dfh join "\t", ('genome', $data->{project}, $data->{gname1}, $data->{gname2}, $data->{convdir}, $genseq, @pos.'', @pos);
print $dfh "\n";

$qfileF  = "que${id}F";
$qfileR  = "que${id}R";
$gfileF  = "genome${id}F";
$gfileR  = "genome${id}R";
$qfilepF = TEMPDIR . $qfileF;
$qfilepR = TEMPDIR . $qfileR;
$gfilepF = TEMPDIR . $gfileF;
$gfilepR = TEMPDIR . $gfileR;

fastaPrint $genseq, "$gfileF", $gfilepF;
fastaPrint revComp $genseq, "$gfileR", $gfilepR;

$pos = 0;

foreach $fa (@biseq) {

    ++$pos;
    $fa->{pos} = $pos;

    fastaPrint $fa->{seq}, "$qfileF", $qfilepF;
    fastaPrint revComp $fa->{seq}, "$qfileR", $qfilepR;

    unless ($data->{convdir} == 1) {
	$ffres = execNeedle ($qfilepF, $gfilepF, $cpgf, $data->{cpgcheck});
	$frres = execNeedle ($qfilepR, $gfilepF, $cpgf, $data->{cpgcheck});

	{
	    if ($ffres->{'aliMis'} > $frres->{'aliMis'}) {
		$fres = $frres;
		$fdir = -1;
		last;
	    }

	    if ($ffres->{'aliMis'} < $frres->{'aliMis'}) {
		$fres = $ffres;
		$fdir = 1;
		last;
	    }

	    if ($ffres->{perc} > $frres->{perc}) {
		$fres = $ffres;
		$fdir = 1;
		last;
	    }

	    if ($ffres->{perc} < $frres->{perc}) {
		$fres = $frres;
		$fdir = -1;
		last;
	    }

	    if ($ffres->{unconv} > $frres->{unconv}) {
		$fres = $frres;
		$fdir = -1;
		last;
	    }

	    if ($ffres->{unconv} < $frres->{unconv}) {
		$fres = $ffres;
		$fdir = 1;
		last;
	    }

	    if ($ffres->{pconv} < $frres->{pconv}) {
		$fres = $frres;
		$fdir = -1;
		last;
	    }

	    if ($ffres->{pconv} > $frres->{pconv}) {
		$fres = $ffres;
		$fdir = 1;
		last;
	    }

	    $fres = $ffres;
	    $fdir = 1;
	}
    }

    unless ($data->{convdir} == 0) {
	$rfres = execNeedle ($qfilepF, $gfilepR, $cpgr, $data->{cpgcheck});
	$rrres = execNeedle ($qfilepR, $gfilepR, $cpgr, $data->{cpgcheck});

	{
	    if ($rfres->{'aliMis'} > $rrres->{'aliMis'}) {
		$rres = $rrres;
		$rdir = -1;
		last;
	    }

	    if ($rfres->{'aliMis'} < $rrres->{'aliMis'}) {
		$rres = $rfres;
		$rdir = 1;
		last;
	    }

	    if ($rfres->{perc} > $rrres->{perc}) {
		$rres = $rfres;
		$rdir = 1;
		last;
	    }

	    if ($rfres->{perc} < $rrres->{perc}) {
		$rres = $rrres;
		$rdir = -1;
		last;
	    }

	    if ($rfres->{unconv} > $rrres->{unconv}) {
		$rres = $rrres;
		$rdir = -1;
		last;
	    }

	    if ($rfres->{unconv} < $rrres->{unconv}) {
		$rres = $rfres;
		$rdir = 1;
		last;
	    }

	    if ($rfres->{pconv} < $rrres->{pconv}) {
		$rres = $rrres;
		$rdir = -1;
		last;
	    }

	    if ($rfres->{pconv} > $rrres->{pconv}) {
		$rres = $rfres;
		$rdir = 1;
		last;
	    }

	    $rres = $rfres;
	    $rdir = 1;
	}
    }

    if ($data->{convdir} == 0) {
	$res  = $fres;
	$dir  = $fdir;
	$gdir = 1;

    } elsif ($data->{convdir} == 1) {
	$res = $rres;
	$dir  = $rdir;
	$gdir = -1;

    } else {
	{
	    if ($fres->{'aliMis'} > $rres->{'aliMis'}) {
		$res  = $rres;
		$dir  = $rdir;
		$gdir = -1;
		last;
	    }

	    if ($fres->{'aliMis'} < $rres->{'aliMis'}) {
		$res  = $fres;
		$dir  = $fdir;
		$gdir = 1;
		last;
	    }

	    if ($fres->{perc} > $rres->{perc}) {
		$res  = $fres;
		$dir  = $fdir;
		$gdir = 1;
		last;
	    }

	    if ($fres->{perc} < $rres->{perc}) {
		$res  = $rres;
		$dir  = $rdir;
		$gdir = -1;
		last;
	    }

	    if ($fres->{unconv} > $rres->{unconv}) {
		$res  = $rres;
		$dir  = $rdir;
		$gdir = -1;
		last;
	    }

	    if ($fres->{unconv} < $rres->{unconv}) {
		$res  = $fres;
		$dir  = $fdir;
		$gdir = 1;
		last;
	    }


	    if ($fres->{pconv} < $rres->{pconv}) {
		$res  = $rres;
		$dir  = $rdir;
		$gdir = -1;
		last;
	    }

	    if ($fres->{pconv} > $rres->{pconv}) {
		$res  = $fres;
		$dir  = $fdir;
		$gdir = 1;
		last;
	    }

	    $res  = $fres;
	    $dir  = $fdir;
	    $gdir = 1;
	}
    }

    unless ($gdir == 1) {
	$res->{qAli} = revComp $res->{qAli};
	$res->{gAli} = revComp $res->{gAli};
	$res->{val}  = reverse revComp $res->{val};
    }

    print $dfh join "\t", @{$fa}{'pos', 'com', 'seq'}, 
                          @{$res}{'qAli', 'gAli', 'aliLen',
				  'aliMis', 'perc', 'gap', 'menum',
				  'unconv', 'conv', 'pconv', 'val'}, 
                          $dir, $gdir;

    if ($static) {
	if ($pos > $num) {
	    print $dfh "\tS\t2";
	} else {
	    print $dfh "\tS\t1";
	}
    }
    print $dfh "\n";
}

unlink $gfilepF
    or errorAndExit ('File access error!', 'File access error!', "unlink error : $gfilepF");

unlink $gfilepR
    or errorAndExit ('File access error!', 'File access error!', "unlink error : $gfilepR");

unlink $qfilepF
    or errorAndExit ('File access error!', 'File access error!', "unlink error : $qfilepF");

unlink $qfilepR
    or errorAndExit ('File access error!', 'File access error!', "unlink error : $qfilepR");


$data->{unconv} = UNCONVL
    unless (exists $data->{unconv}   && $data->{unconv} =~ /^\d{1,3}$/);
$data->{pconv}  = PCONVL
    unless (exists $data->{pconv}    && $data->{pconv}   =~ /^\d{1,3}(\.\d+)?$/);
$data->{mis}    = MISL
    unless (exists $data->{mis}      && $data->{mis}    =~ /^\d{1,3}$/);
$data->{perc}   = PERCL
    unless (exists $data->{perc}     && $data->{perc}   =~ /^\d{1,3}(\.\d+)?$/);
$data->{cpgcheck} = 0
    unless (exists $data->{cpgcheck} && $data->{cpgcheck} eq 'on');
$data->{uniq} = 0
    unless (exists $data->{uniq}     && $data->{uniq} eq 'on');

if ($static) {
    printf REPHEADS, $id, $data->{unconv}, $data->{mis}, $data->{perc}, $data->{pconv}, $conv, $data->{cpgcheck}, $data->{uniq};
} else {
    printf REPHEAD,  $id, $data->{unconv}, $data->{mis}, $data->{perc}, $data->{pconv}, $conv, $data->{cpgcheck}, $data->{uniq};
}

###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
