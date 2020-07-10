#_*****************************************************************************
#_*                                                                           *
#_* File name: BFUtils.pm                                                     *
#_* Utility moudule for QUMA                                                  *
#_* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
#_* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
#_*                                                                           *
#_* 2008/02/20 First open source version                                      *
#_* 2008/02/25 Function 'execNeedle' updated to accept output of old version  *
#_*            needle program which use ' ', not '-', as alignment gap.       *
#_* 2008/03/31 Function 'multiFastaParse' updated to fix bug of last line     *
#_*            exclusion of multi-fasta sequences                             *
#_* 2010/11/12 Functions 'fisherExactTest', 'someCombination', 'decPrime'     *
#_*            'uTest', 'exactUTest' updated to improve a performance.        *
#_*            Functions 'combination', 'fractrial', 'someFractrial' were     *
#_*            were deleted.                                                  *
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
package BFUtils;
use 5.6.0;
use strict;
use warnings;
use Exporter;

use Archive::Zip;
use RTF::TEXT::Converter;
use Bio::Trace::ABIF;

use BFSetting;

our (@ISA);
our (@EXPORT);

@ISA = qw (Exporter);
@EXPORT = qw (PI makeTime convName errorAndExit htmlSunitize
	      revComp multiFastaParse fastaPrint
	      parseGenome parseBiseq execNeedle
              getSampleSeq groupSVG ipCheck parCheck
	      fisherExactTest uTest);

use constant PI    => atan2 (1, 1) * 4;
use constant PI2   => 1 / sqrt (2 * PI);
use constant PRIME => [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,
		       71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,
		       149,151,157,163,167,173,179,181,191,193,197,199,211,
		       223,227,229,233,239,241,251,257,263,269,271,277,281,
		       283,293];
use constant EHTML => q[Content-type:text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="en">
 <HEAD>
  <META HTTP-EQUIV="Content-Type" content="text/html; charset=ISO-8859-1">
  <META HTTP-EQUIV="Content-Script-Type" content="text/javascript">
  <META HTTP-EQUIV="Content-Style-Type" content="text/css">
  <LINK REV="MADE" HREF="mailto:yuichi@kumaki.jp">
  <LINK REL="INDEX" HREF="].HL.q[/top/index.html">
  <TITLE>%s</TITLE>
 </HEAD>
 <BODY>
  <H2>%s</H2>
  <TABLE width="60%%"><TR>
   <TD align="left"><A STYLE="text-align:center" HREF="javascript:history.back()"><IMG SRC="].HL.q[/images/icon019.gif" border="0"></A></TD>
   <TD align="left"><A STYLE="text-align:center" HREF="javascript:window.close();void(0);"><IMG SRC="].HL.q[/images/iconClose.gif" border="0"></A></TD>
  </TR></TABLE>
 </BODY>
</HTML>
];

sub makeTime (;$) {

    my $time = shift || time;

    my @time;

    @time = (localtime ($time))[reverse (0..5)];

    $time[1]++;
    $time[0] += 1900;

    sprintf("%04d%02d%02d%02d%02d%02d", @time);
}

sub convName ($) {
    my ($name) = shift;
    $name =~ tr/A-Z/a-z/;
    $name =~ s/(?:%20)+/_/g;
    $name =~ s/%[\da-fA-F]{2}//g;
    return ($name);
}

sub errorAndExit ($$$) {

    my ($title) = shift;
    my ($error) = shift;
    my ($log  ) = shift;

    warn $log;
    printf EHTML, $title, $error;
    exit;
}

sub htmlSunitize ($) {

    my ($in) = shift;
    $in =~ s/&/&amp;/g;
    $in =~ s/</&lt;/g;
    $in =~ s/>/&gt;/g;
    $in =~ s/"/&quot;/g;
    $in =~ s/'/&#39;/g;
    return ($in);
}

sub revComp ($) {

    my $seq = reverse shift;

    $seq =~
	y/ACGTURYMWSKDHBVNacgturymwskdhbvn/TGCAAYRKWSMHDVBNtgcaayrkwsmhdvbn/;
    $seq;
}

sub curateSeq ($) {

    my $seq = shift;

    $seq =~
	y/ACGTURYMWSKDHBVNacgturymwskdhbvn//cd;
    $seq;
}

sub multiFastaParse ($) {

    my ($multi) = shift;
    my ($fa   );
    my ($line );
    my (@biseq);
    my ($size );

    local ($1 );

    $size = 0;
    $multi =~ s/\r\n/\n/g;
    $multi =~ s/\r/\n/g;

    while ($multi =~ /(.*)$/mg) {

	chomp ($line = $1);

	if ($line =~ /^>/) {
	    pop @biseq if ($fa && ! $fa->{seq});
	    $fa = {};
	    push @biseq, $fa;
	    $fa->{com} = $line;
	    $fa->{com} =~ s/^>//;
	    $fa->{com} =~ s/\t//g;
	    $fa->{com} =~ s/\s*$//g;
	} else {
	    $line = curateSeq ($line);
	    $line or next;
	    $fa	or return ();
	    $fa->{seq} .= uc $line; 
	    $size += length $line;
	}
    }

    pop @biseq if ($fa && ! $fa->{seq});
    return ($size, @biseq);
}

sub fastaMake ($$;$) {

    my $seq  = shift;
    my $com  = shift;
    my $line = shift || 60;

    local $1;

    $seq =~ y/0-9 \t\n\r\f//d;

    $seq =~ s/(.{1,$line})/$1\n/g;

    ">$com\n" . $seq;
}

sub fastaPrint ($$$;$$) {

    my $seq  = shift;
    my $com  = shift;
    my $path = shift;
    my $line = shift;
    my $add  = shift;
    my $fh;

    local ($!  );

    if ($add) {
	open ($fh, ">>$path")
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't open $path : $!");

    } else {
	open ($fh, ">$path")
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't open $path : $!");

    }

    print $fh fastaMake ($seq, $com, $line);
    close ($fh);
}

sub parseSeq ($) {

    my ($seq ) = shift;
    my ($com );
    local ($1);

    $seq or return;
    $com = '';
    $seq =~ s/\r\n/\n/g;
    $seq =~ s/\r/\n/g;
    $seq = uc $seq;

    if ($seq =~ /^\s*>.*?\n/m) {
	$seq =~ s/^\s*>(.*)?\n//m;
	$com = $1;
	$com =~ s/\t//g;
	$com =~ s/\s*$//g;

    } elsif ($seq =~ /^ORIGIN\s*\n((\s+(\d+(\s+\w+)+))+)\s*\n\/\//m) {
	$seq = $1;

    } elsif ($seq =~ /^SQ\s+SEQUENCE.*\n((\s+(\w+\s+)+\d+)+)\n\/\//m) {
	$seq = $1;

    } elsif ($seq =~ /\.\.\s*\n((\s+(\d+(\s+\w+)+))+)\s*/m) {
	$seq = $1;
    } elsif ($seq =~ /^\s*>.+\s.+/m) {
	$seq =~ s/^\s*>(.+?)\s(?=.+)//m;
	$com = $1;
    }

    $seq =  curateSeq ($seq);
    return ($seq, $com);
}

sub parseGenome ($$) {

    my ($seq  ) = shift;
    my ($file ) = shift;
    my ($com  );
    my ($fh   );
    my ($size );
    my ($abif );
    my ($rtf  );
    local ($! );
    local ($1 );

    $seq =~ s/^[\r\s]+// if ($seq);
    $seq =~ s/^Content-Type: .*(\r|\n|\r\n){2}//i if ($seq);
    $seq =~ s/^[\r\s]+// if ($seq);
    $seq =~ s/[\r\s]+$// if ($seq);
    $seq =~ s/(\r|\n|\r\n){2}/$1/g if ($seq);

    return unless ($seq || $file);

    ($seq, $com) = parseSeq ($seq);

    if ($seq) {
	$size = length $seq;
	GSEQL && $size > GSEQL and
	    errorAndExit ('Genome sequence is too long!',
			  'Genome sequence is too long!<BR>upper limit of genome sequence length is '. GSEQL . ' bases',
			  "Genome sequence is too long!: $size");
	return ($seq);
    }

    return unless ($file && -e TEMPDIR . $file);

    unless (-s TEMPDIR . $file) {
	unlink TEMPDIR . $file
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$file : $!");
	return;
    }

    if (-B TEMPDIR . $file && $file =~ /\.(ab1|fsa)$/i) {
	$abif = new Bio::Trace::ABIF;

	unless ($abif->open_abif (TEMPDIR . $file)) {
	    unlink TEMPDIR . $file
		or errorAndExit ('File access error!', 'File access error!', 
				 "File access error! : Can't unlink " . TEMPDIR . "$file : $!");
	    errorAndExit ('Invalid genome sequence data is present. File is not sequence text file.',
			  'Invalid genome sequence data is present. File is not sequence text file.',
			  "Invalid genome sequence data is present. File is invalid ABI format file. $file");
	}

	$seq = $abif->edited_sequence;
	$abif->close_abif;
	unlink TEMPDIR . $file
	    or warn "File access error! : Can't unlink " . TEMPDIR . "$file : $!";
	return ($seq);
    }

    if (-B TEMPDIR . $file) {
	unlink TEMPDIR . $file
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$file : $!");

	errorAndExit ('Invalid genome sequence data is present. File is not sequence text file.',
		      'Invalid genome sequence data is present. File is not sequence text file.',
		      "Invalid genome sequence data is present. File is not sequence text file. Binary file. $file");
    }

    (GFILEL && -s TEMPDIR . $file > GFILEL) and
        errorAndExit ('Genome file size is too large!',
		      'Genome file size is too large!<BR>Upper limit of file genome file size is '. GFILEL . ' bytes',
		      'Genome file size is too large!: ' . (    -s TEMPDIR . $file));

    open $fh, TEMPDIR . $file
	or errorAndExit ('File access error!', 'File access error!', 
			 "File access error! : Can't open " . TEMPDIR . "$file : $!");
    $seq = join '', <$fh>;
    close $fh;

    if ($file =~ /\.rtf/i) {
	(new RTF::TEXT::Converter(output => \$rtf))->parse_string ($seq);
	$seq = $rtf;
    }

    $seq =~ s/^[\r\s]+// if ($seq);
    $seq =~ s/^Content-Type: .*(\r|\n|\r\n){2}//i if ($seq);
    $seq =~ s/^[\r\s]+// if ($seq);
    $seq =~ s/[\r\s]+$// if ($seq);
    $seq =~ s/(\r|\n|\r\n){2}/$1/g if ($seq);

    unlink TEMPDIR . $file
	or warn "File access error! : Can't unlink " . TEMPDIR . "$file : $!";

    ($seq, $com) = parseSeq ($seq);

    if ($seq) {
	$size = length $seq;
	(GSEQL && $size > GSEQL) and
	    errorAndExit ('Genome sequence is too long!',
			  'Genome sequence is too long!<BR>upper limit of genome sequence length is '. GSEQL . ' bases',
			  "Genome sequence is too long!: $size");
    }

    return ($seq);
}

sub parseBiseq ($$) {

    my ($seq  ) = shift;
    my ($file ) = shift;

    my ($size );
    my ($abif );
    my (@biseq);
    my ($com  );
    my ($dir  );
    my ($zip  );
    my ($fobj );
    my ($f1   );
    my ($fh   );
    my ($fa   );
    my ($name );
    my ($multi);
    my (%dir  );
    my (%dir2 );
    my ($rtf  );
    local ($! );
    local ($1 );
    local ($2 );
    local ($a );
    local ($b );

    $size = 0;
    $abif = new Bio::Trace::ABIF;

    $seq =~ s/^[\r\s]+// if ($seq);
    $seq =~ s/^Content-Type: .*(\r|\n|\r\n){2}//i if ($seq);
    $seq =~ s/^[\r\s]+// if ($seq);
    $seq =~ s/[\r\s]+$// if ($seq);
    $seq =~ s/(\r|\n|\r\n){2}/$1/g if ($seq);

    return unless ($seq || $file);

    if ($seq) {

	($size, @biseq) = multiFastaParse ($seq);

	unless (@biseq) {

	    # in case of single gb or plain text format sequence is pasted
	    ($seq, $com) = parseSeq ($seq);

	    if ($seq) {
		$com ||= 'seq';
		$size = length $seq;
		@biseq = ({seq => $seq, com => $com});
	    }
	}

	if (@biseq) {
	    (BSEQL && $size > BSEQL) and
		errorAndExit ('Total length of bisulfite sequences is too long!',
			      "Total length of bisulfite sequences is too long!<BR>\n" .
			      "Upper limit of total length of bisulfite sequences is ". BSEQL . ' bases',
			      "Total length of bisulfite sequences is too long!: $size");
	    return (@biseq);
	}
    }

    return unless ($file && -e TEMPDIR . $file);

    unless (-s TEMPDIR . $file) {
	unlink TEMPDIR . $file
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't unlink " . TEMPDIR . "$file : $!");
	return;
    }

    if ($file =~ /\.zip$/i) {

	$dir = $file;
	$dir =~ s/\.zip//i;
        $dir .= $$;

	mkdir TEMPDIR . $dir
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't mkdir " . TEMPDIR . "$dir : $!");

	chdir TEMPDIR . $dir
	    or errorAndExit ('File access error!', 'File access error!', 
			     "File access error! : Can't chdir " . TEMPDIR . "$dir : $!");

	$zip = new Archive::Zip;
	$zip->read (TEMPDIR . $file)
	    and errorAndExit ('File access error!', 'File access error!', 
			      "Read Error at Archive::Zip : " . TEMPDIR . $file);

	foreach $fobj ($zip->members()) {

	    $seq = $name = '';
	    $f1 = $fobj->fileName ();
	    $f1 =~ /__MACOSX/ and next;
	    $f1 =~ /\/\./ and next;
	    $f1 =~ /\.(seq|fa|fas|fasta|txt|text|rtf|ab1|fsa)$/i or next;
	    $zip->extractMember ($f1);

	    if (-B TEMPDIR . "$dir/$f1" && $f1 !~ /\.(ab1|fsa)$/i) {
		unlink TEMPDIR . "$dir/$f1"
		    or warn "File access error! : Can't unlink " . TEMPDIR . "$dir/$f1 : $!";
		$f1 =~ s/^(.*)\/(.*?)$/$1/;
		$dir{$f1}++;
		next;

	    } elsif (-B TEMPDIR . "$dir/$f1") {

		unless ($abif->open_abif (TEMPDIR . "$dir/$f1")) {
		    unlink TEMPDIR . "$dir/$f1"
			or warn "File access error! : Can't unlink " . TEMPDIR . "$dir/$f1 : $!";
		    warn "Invalid bisulfite sequence data is present. File is invalid ABI format file. $dir/$f1";
		}
		$seq = $abif->edited_sequence;
		$name = $abif->sample_name;
		$abif->close_abif;

	    } else {

		open $fh, TEMPDIR . "$dir/$f1"
		    or errorAndExit ('File access error!', 'File access error!', 
				     "File access error! : Can't open " . TEMPDIR . "$dir/$f1 : $!");
		$seq = join '', <$fh>;
		close $fh;

		if ($f1 =~ /\.rtf/i) {
		    (new RTF::TEXT::Converter(output => \$rtf))->parse_string ($seq);
		    $seq = $rtf;
		}

		$seq =~ s/^[\r\s]+// if ($seq);
		$seq =~ s/^Content-Type: .*(\r|\n|\r\n){2}//i if ($seq);
		$seq =~ s/^[\r\s]+// if ($seq);
		$seq =~ s/[\r\s]+$// if ($seq);
		$seq =~ s/(\r|\n|\r\n){2}/$1/g if ($seq);
	    }

	    unlink TEMPDIR . "$dir/$f1"
		or warn "File access error! : Can't unlink " . TEMPDIR . "$dir/$f1 : $!";

	    $f1 =~ s/^(.*)\/(.*?)$/$1/;
	    $name ||= $2 || $f1;
	    $name =~ s/\t//g;
	    $name =~ s/\s*$//g;
	    $dir{$f1}++;
	    $seq or next;

	    $fa = {};
	    push @biseq, $fa;
	    ($fa->{seq}, $fa->{com}) = parseSeq ($seq);
	    unless ($fa->{seq}) {
		pop @biseq;
		next;
	    }
	    $fa->{com} ||= $name;
	    $size += length $fa->{seq};
	}

	unlink TEMPDIR . $file
	    or warn "File access error! : Can't unlink " . TEMPDIR . "$file : $!";

	{
	    foreach $f1 (sort {length($b) <=> length($a)} keys %dir) {
                -d TEMPDIR . "$dir/$f1" or next;
		rmdir TEMPDIR . "$dir/$f1"
		    or warn "File access error! : Can't rmdir " . TEMPDIR . "$dir/$f1 : $!";

	    } continue {
		if ($f1 =~ s/^(.*)\/(.*?)$/$1/) {
		    $dir2{$f1}++ if ($f1);
		}
	    }

	    %dir = ();

    	    if (%dir2) {
		%dir = %dir2;
		%dir2 = ();
		redo;
	    }
	}

	rmdir TEMPDIR . $dir
	    or warn "File access error! : Can't rmdir " . TEMPDIR . "$dir : $!";
    } else {

	if (-B TEMPDIR . $file && $file !~ /\.(ab1|fsa)$/i) {

	    unlink TEMPDIR . $file
		or errorAndExit ('File access error!', 'File access error!', 
				 "File access error! : Can't unlink " . TEMPDIR . "$file : $!");

	    errorAndExit ('Invalid bisulfite sequence data is present. File is not multi-FASTA sequence text file.',
			  'Invalid bisulfite sequence data is present. File is not multi-FASTA sequence text file.',
			  "Invalid bisulfite sequence data is present. File is not multi-FASTA sequence text file. Binary file. $file");
	}

	if (-B TEMPDIR . $file) {

	    unless ($abif->open_abif (TEMPDIR . $file)) {
		unlink TEMPDIR . $file
		    or errorAndExit ('File access error!', 'File access error!', 
				     "File access error! : Can't unlink " . TEMPDIR . "$file : $!");
		errorAndExit ('Invalid bisulfite sequence data is present. File is not multi-FASTA sequence text file.',
			      'Invalid bisulfite sequence data is present. File is not multi-FASTA sequence text file.',
			      "Invalid bisulfite sequence data is present. File is not multi-FASTA sequence text file. Binary file. File is invalid ABI format file. $file");
	    }

	    $multi = $abif->edited_sequence;
	    $name = $abif->sample_name;
	    $abif->close_abif;

	} else {

	    open $fh, TEMPDIR . $file
		or errorAndExit ('File access error!', 'File access error!', 
				 "File access error! : Can't open " . TEMPDIR . "$file : $!");

	    $multi = join '', <$fh>;
	    close $fh;
	    unlink TEMPDIR . $file
		or warn "File access error! : Can't unlink " . TEMPDIR . "$file : $!";

	    if ($file =~ /\.rtf/i) {
		(new RTF::TEXT::Converter(output => \$rtf))->parse_string ($multi);
		$multi = $rtf;
	    }
	}

	$file =~ s/^(.*)\/(.*?)$/$1/;
	$name ||= $2 || $file;
	$name =~ s/\t//g;
	$name =~ s/\s*$//g;

	$multi =~ s/^[\r\s]+// if ($multi);
	$multi =~ s/^Content-Type: .*(\r|\n|\r\n){2}//i if ($multi);
	$multi =~ s/^[\r\s]+// if ($multi);
	$multi =~ s/[\r\s]+$// if ($multi);
	$multi =~ s/(\r|\n|\r\n){2}/$1/g if ($multi);

	return unless ($multi);

	($size, @biseq) = multiFastaParse ($multi);

	unless (@biseq) {

	    # in case of single gb or plain text format sequence is uploaded
	    ($seq, $com) = parseSeq ($multi);

	    if ($seq) {
		$com ||= $name || 'seq';
		$size = length $seq;
		@biseq = ({seq => $seq, com => $com});
	    }
	}
    }

    (BSEQL && @biseq && $size > BSEQL) and
	errorAndExit ('Total length of bisulfite sequences is too long!',
		      "Total length of bisulfite sequences is too long!<BR>\n" .
		      "Upper limit of total length of bisulfite sequences is ". BSEQL . ' bases',
		      "Total length of bisulfite sequences is too long!: $size");

    (BSEQN && @biseq > BSEQN) and
	errorAndExit ('Number of bisulfite sequences is too much!',
		      'Number of bisulfite sequences is too much!<BR>Max number of bisulfite sequences is '. BSEQN,
		      'Number of bisulfite sequences is too much!: ' . @biseq);

    return @biseq;
}

sub execNeedle ($$$;$) {

    my ($gfile) = shift;
    my ($qfile) = shift;
    my ($cpg  ) = shift;
    my ($opt  ) = shift;
    my ($com  );
    my ($fh   );
    my ($ref  );
    my ($gAli );
    my ($qAli );
    my ($i    );
    my ($flag );
    my ($g    );
    my ($q    );
    my ($j    );
    my ($k    );
    my ($t    );
    my ($pos  );
    local ($! );
    local ($_ );
    local ($? );

    $ref = {};
    $ref->{qAli}   = '';
    $ref->{gAli}   = '';
    $ref->{gap}    = 0;
    $ref->{menum}  = 0;
    $ref->{unconv} = 0;
    $ref->{conv}   = 0;
    $ref->{pconv}  = '';
    $ref->{match}  = 0;
    $ref->{val}    = '';
    $ref->{perc}   = '';
    $ref->{aliMis} = 0;

    $com = NEEDLE . " $gfile $qfile " . NDLOPT;

    open $fh, $com
	    or errorAndExit ('System error!', 'System error!',
			     "Needle exec error! : $! : $com");

    while (<$fh>) {

	chomp;

	if (/^>que/../^>genome/) {
	    $ref->{qAli} .= $_ unless (/^>/);
	}
	if (/^>genome/../^$/) {
	    $ref->{gAli} .= $_ unless (/^>/);
	}
    }

    $ref->{qAli} =~ y/ /-/;
    $ref->{gAli} =~ y/ /-/;

    close $fh
	or errorAndExit ('System error!', 'System error!',
			 "Needle close error! : $? : $com");

    length $ref->{gAli} == length $ref->{qAli}
        or errorAndExit ('System error!', 'System error!',
			 "Needle error! gAli len != qAli len : " .
			 (length $ref->{gAli}) . " !=  " . (length $ref->{qAli}) . ";;;" .
			 $ref->{gAli} . "::::" . $ref->{qAli});

    $gAli = $qAli = '';

    for ($i = $flag = 0; $i < length $ref->{gAli}; $i++) {

	$g = uc substr $ref->{gAli}, $i, 1;
	next if ($g eq '-' && $flag == 0);
	$flag = 1;
	$q = uc substr $ref->{qAli}, $i, 1;
	$gAli .= $g;
	$qAli .= $q;
    }

    while ($g = chop $gAli) {
	unless ($g eq '-') {
	    $gAli .= $g;
	    last;
	}
	chop $qAli;
    }

    $ref->{aliLen} = length $qAli;

    for ($i = $j = 0; $i < $ref->{aliLen}; $i++) {

	$g = uc substr $gAli, $i, 1;
	$q = uc substr $qAli, $i, 1;

	$j++ unless ($g eq '-');

	if ($q eq $g ||
	    $g eq 'C' && $q eq 'T') {
	    $ref->{match}++;
	}

	if ($g eq '-') {
	    $ref->{gap}++;
	    next;
	}

	if ($q eq '-') {
	    $ref->{gap}++;
	    if ($cpg->{$j - 1}) {
		$ref->{val} .= '-';
	    }
	    next;
	}

	last if ($i == $ref->{aliLen} - 1);

	next unless ($g eq 'C');

	unless ($cpg->{$j - 1}) {
	    if ($q eq 'C') {
		$ref->{unconv}++;
	    } elsif ($q eq 'T') {
		$ref->{conv}++;
	    }
	    next;
	}

	if ($opt) {

	    for ($k = $i+1; $k < $ref->{aliLen}; $k++) {
		$t = uc substr $qAli, $k, 1;
		last unless ($t eq '-');
	    }

	    if ($t eq 'G') {
		if ($q eq 'C') {
		    $ref->{menum}++;
		    $ref->{val} .= '1';

		} elsif ($q eq 'T') {
		    $ref->{val} .= '0';

		} else {
		    $ref->{val} .= $q;
		}
	    } else {
		$ref->{val} .= '+';

	    }

	} else {
	    if ($q eq 'C') {
		$ref->{menum}++;
		$ref->{val} .= '1';

	    } elsif ($q eq 'T') {
		$ref->{val} .= '0';

	    } else {
		$ref->{val} .= $q;
	    }
	}
    }

    if ($ref->{conv} + $ref->{unconv}) {
        $ref->{pconv} = sprintf "%3.1f", 100 * $ref->{conv}/($ref->{conv} + $ref->{unconv});
    } else {
	$ref->{pconv} = 0;
    }
    $ref->{perc}   = sprintf "%3.1f", 100 * $ref->{match} / $ref->{aliLen};
    $ref->{aliMis} = $ref->{aliLen} - $ref->{match};
    return $ref;
}

sub getSampleSeq ($) {

    my ($idx  ) = shift;
    my ($files);
    my ($file );
    my ($fh   );
    my ($seq  );

    $files = SEQFILES;
    $file  = $files->[$idx];
    open $fh, $file->{file}
        or errorAndExit ('File access error!', 'File access error!', "File access error : $! : " . $file->{file});
    $seq = join '', <$fh>;
    close $fh;
    return ($seq);
}

sub groupSVG ($) {

    my ($in  ) = shift;
    local ($1);

    $in =~ s[^(<svg.*)$][$1\n<g>]m;
    $in =~ s[^(</svg>)$][</g>\n$1]m;

    return ($in);
}


sub ipCheck ($) {

    my ($data) = shift;
    my ($ip1 );
    my ($ip2 );
    my ($sip1);
    my ($sip2);
    my ($f   );
    my (@in  );
    my (%conv);
    local ($_);

    if (open $f, IPCONV) {
	while (<$f>) {
	    chomp;
	    $_ or next;
	    /^#/ and next;
	    s/#.*$//;
	    @in = split /\t/;
	    $conv{join '', map {sprintf "%02X", $_} split /\./, $in[0]} = join '', map {sprintf "%02X", $_} split /\./, $in[1];
	}
	close $f;
    }

    if ($data && exists $data->{id}) {
	$ip1  = substr $data->{id}, -8;
	$sip1 = substr $ip1, 0, 6;
    } else {
	$data->{id} = '';
	$ip1  = '';
	$sip1 = '';
    }

    $ip2  = join '', map {sprintf "%02X", $_} split /\./, $ENV{REMOTE_ADDR};
    $sip2 = substr $ip2, 0, 6;

    $ip1 && ($ip1 eq $ip2 || exists $conv{$ip2} && $ip1 eq $conv{$ip2} || exists $conv{$ip1} && $conv{$ip1} eq $ip2) ||
	$sip1 && exists $conv{$sip1} && exists $conv{$sip2} && $conv{$sip1} eq $conv{$sip2}
	or errorAndExit ('Invalid access',
			 'Invalid access: IP address is different from your data submission access, or your browser cache data is expired. Please resubmit sequence!',
			 "Invalid ID or different IP : $data->{id} : $ip2"); 
    return 1;
}

sub parCheck ($) {

    my ($data) = shift;
    my ($key );
    my ($nkey);


    foreach $key (keys %$data) {
	next unless  ($key =~ /^amp;.+/);
	$nkey = $key;
	$nkey =~ s/^amp;//;
	next if (exists $data->{$nkey});
	$data->{$nkey} = $data->{$key};
    }

    return 1;
}

sub fisherExactTest ($$$$$) {

    my ($ref  ) = shift;
    my ($aa   ) = shift;
    my ($bb   ) = shift;
    my ($cc   ) = shift;
    my ($dd   ) = shift;

    my ($ee   );
    my ($ff   );
    my ($gg   );
    my ($hh   );
    my ($nn   );
    my ($base );
    my ($min  );
    my ($max  );
    my ($ta   );
    my ($tb   );
    my ($tc   );
    my ($td   );
    my ($p    );

    $ref ||= {};
    $ee = $aa + $bb;
    $ff = $cc + $dd;
    $gg = $aa + $cc;
    $hh = $bb + $dd;
    $nn = $aa + $bb + $cc + $dd;

    $base = abs ($aa * $dd - $bb * $cc);
    $max = $ee < $gg ? $ee : $gg;
    $min = $ee < $hh ? 0 : $ee - $hh;

    $p=0;
    for ($ta = $min; $ta <= $max; $ta++) {
	$tb = $ee - $ta;
	$tc = $gg - $ta;
	$td = $ff - $tc;

	next if (abs($ta * $td - $tb * $tc) < $base);
	$p += someCombination ($ref, [{m => $ee, n => $ta}, {m => $ff, n => $tc}], [{m => $nn, n => $gg}]);
    }
    return $p;
}

sub someCombination ($$;$) {

    my ($ref   ) = shift;
    my ($multi ) = shift;
    my ($div   ) = shift;

    my ($tmp   );
    my ($ret   );
    my (%all   );
    my ($max   );
    my ($val   );
    my (%vals  );
    my ($i     );
    my (@plus  );
    my (@minus );
    local ($a  );
    local ($b  );

    $div  ||= [];
    $max = 0;

    foreach $tmp (@$multi) {
	$all{$tmp->{m}}++;
	$all{$tmp->{n}}--;
	$all{$tmp->{m} - $tmp->{n}}--;
	$max = $tmp->{m} if ($max < $tmp->{m});
    }

    foreach $tmp (@$div) {
	$all{$tmp->{m}}--;
	$all{$tmp->{n}}++;
	$all{$tmp->{m} - $tmp->{n}}++;
	$max = $tmp->{m} if ($max < $tmp->{m});
    }

    $val = 0;
    for ($i = $max; $i > 1; $i--) {
	$val += $all{$i} if (exists $all{$i});
	$vals{$i} = $val;
    }

    foreach $val (sort {$b <=> $a} keys %vals) {
	$vals{$val} or next;
	$ref->{$val} ||= decPrime ($val);

	if (@{$ref->{$val}} > 1) {
	    foreach $tmp (@{$ref->{$val}}) {
		$vals{$tmp} += $vals{$val};
	    }
	    delete $vals{$val};
	    next;
	}

	if ($vals{$val} > 0) {
	    push @plus, $val, $vals{$val};
	} else {
	    push @minus, $val, $vals{$val};
	}
    }

    $ret = 1;
    while (@plus || @minus) {
	if ($ret < 2000000000 &&
	    @plus || !@minus) {
	    $val = shift @plus;
	    $tmp = shift @plus;
	} else {
	    $val = shift @minus;
	    $tmp = shift @minus;
	}
	$ret *= $val ** $tmp;
    }

    return $ret;
}

sub decPrime ($);
sub decPrime ($) {

    my ($val) = shift;
    my ($pri);
    my ($sqr);
    my ($i  );
    my ($ret);
    my ($tmp);
    $ret = [];

    $pri = PRIME;
    $sqr = sqrt $val;

    for ($i = 0; $i < @$pri; $i++) {
	last if ($pri->[$i] > $sqr);
	$tmp = $val / $pri->[$i];
	next if ($tmp - int($tmp));
	push @$ret, $pri->[$i];
	push @$ret, @{decPrime($tmp)};
	return $ret;
    }
    return [$val];
}

sub uTest ($$) {

    my ($dat1) = shift;
    my ($dat2) = shift;

    my ($i   );
    my (%num );
    my (%grp );
    my ($n1  );
    my ($n2  );
    my ($n   );
    my ($ub1 );
    my ($ub2 );
    my ($rank);
    my ($rgrp);
    my ($rnum);
    my ($rall);
    my ($same);
    my ($ref );
    my ($eu  );
    my ($vu  );
    my ($z0  );
    my ($p   );
    my ($tmp );

    local ($a);
    local ($b);

    ($dat1, $dat2) = ($dat2, $dat1) if (@$dat1 > @$dat2);

    $n1 = @$dat1;
    $n2 = @$dat2;
    $n = $n1 + $n2;

    $ub1 = $n1 * $n2 + $n1 * ($n1 + 1) / 2; 
    $ub2 = $n1 * $n2 + $n2 * ($n2 + 1) / 2;

    foreach $i (@$dat1) {
	$num{$i}++;
	$grp{$i}++;
    }

    foreach $i (@$dat2) {
	$num{$i}++;
    }

    $rank = 0;
    $rgrp = [];
    $rnum = [];
    $rall = [];

    foreach $i (sort {$a <=> $b} keys %num) {

	$rank++;
	$rank += ($num{$i} - 1) / 2;

	push @$rgrp, $grp{$i} || 0;
	push @$rnum, $num{$i} || 0;
	push @$rall, $rank;

	$rank += ($num{$i} - 1) / 2;
	$same += $num{$i} ** 3 - $num{$i};
    }

    $ref = {ub1 => $ub1, ub2 => $ub2, rank => $rall, num => $rnum,
	    rem => [], n => $n1, all => $n};

    $ref->{uval} = uVal ($ref, $rgrp);

    if ($n > 20) {
	$eu = $n1 * $n2 / 2;
	$vu = $n1 * $n2 / (12 * ($n ** 2 - $n)) * ($n ** 3 - $n - $same);
	$z0 = $vu ? abs ($ref->{uval} - $eu) / sqrt ($vu) : 0;
	$p = gxp ($z0);
	return (2 * $p);
    }

    $ref->{rem}[@$rnum - 1] = $rnum->[@$rnum - 1];

    for ($i = @$rnum - 2; $i >= 0; $i--) {
	$ref->{rem}[$i] = $ref->{rem}[$i+1] + $rnum->[$i];
    }

    $tmp = {};
    return (exactUTest ($tmp, $ref, 0, $n1, ()));
}

sub uVal ($$) {

    my $ref = shift;
    my $rgr = shift;

    my ($i );
    my ($r1);
    my ($r2);

    for ($i = 0; $i < @{$ref->{rank}}; $i++) {
	$r1 += $rgr->[$i] * $ref->{rank}[$i];
	$r2 += ($ref->{num}[$i] - $rgr->[$i]) * $ref->{rank}[$i];
    }

    return ($ref->{ub1} - $r1 < $ref->{ub2} - $r2 ? $ref->{ub1} - $r1 : $ref->{ub2} - $r2)
}

sub exactUTest ($$$$@);
sub exactUTest ($$$$@) {

    my ($tmp) = shift;
    my ($ref) = shift;
    my ($pos) = shift;
    my ($num) = shift;
    my (@lst) = @_;

    my ($i);
    my ($n1);
    my ($n2);
    my ($t);
    my ($m) = [];
    my ($d) = [];
    my ($r) = 0;

    if ($pos >= @{$ref->{num}}) {

	return (0) if ($num);
	return (0) if ($ref->{uval} < uVal ($ref, \@lst));

	$t = $ref->{all};
	$n1 = $ref->{n};
	$n2 = $t - $n1;

	for ($i = 0; $i < @{$ref->{num}}; $i++) {

	    $lst[$i] ||= 0;
	    push @$m, {m => $n1, n => $lst[$i]};
	    push @$m, {m => $n2, n => $ref->{num}[$i] -$lst[$i]};
	    $n1 -= $lst[$i];
	    $n2 -= $ref->{num}[$i] -$lst[$i];

	    push @$d, {m => $t, n => $ref->{num}[$i]};
	    $t -= $ref->{num}[$i];
	}
	return (someCombination ($tmp, $m, $d));
    }

    for ($i = 0; $i <= $ref->{num}[$pos]; $i++) {

	return ($r) if ($num - $i < 0);
	next if ($pos < @{$ref->{num}} -1 && $num - $i > $ref->{rem}[$pos+1]);
	$r += exactUTest ($tmp, $ref, $pos + 1, $num - $i, (@lst, $i));
    }
    return $r;
}

sub gxp ($) {

    my ($x) = shift;

    my ($is);
    my ($y );
    my ($c );
    my ($p );
    my ($z );
    my ($i );

    $is = -1;
    $y  = abs ($x);
    $c  = $y ** 2;
    $p  = 0;
    $z  = exp (- $c / 2) * PI2;

    if ($y < 2.5) {

	for ($i = 20; $i > 0; $i--) {
	    $p = $i * $c / ($i * 2 + 1 + $is * $p);
	    $is = - $is;
	}

	$p = 0.5 - $z * $y / (1 - $p);

    } else {

	for ($i = 20; $i > 0; $i--) {
	    $p = $i / ($y + $p);
	}

	$p = $z / ($y + $p);
    }

    return ($x < 0 ? 1 - $p : $p);
}

###########################  End of Main ######################################
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
