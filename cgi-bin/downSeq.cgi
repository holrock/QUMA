#!/usr/bin/perl
#_*****************************************************************************
#_*                                                                           *
#_* File name: downSeq.cgi                                                    *
#_* cgi for downloading sample sequence file                                  *
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

my ($cgi  );
my ($data );
my ($files);
my ($file );
my ($fh   );
my ($cont );
my ($size );
local ($! );

$cgi = new CGI::Lite;
$data = $cgi->parse_form_data;

$data->{seq} && $data->{seq} =~ /^\d+$/
    or $data->{seq} = 0;
$files = SEQFILES;

$file = $files->[$data->{seq}];

open $fh, $file->{file}
or errorAndExit ('File access error!', 'File access error!', "File access error : $! : " . $file->{file});

$cont = join '', <$fh>;
$size = length $cont;

print qq{Content-Disposition: attachment; filename="$file->{name}"\n};
print qq{Content-Length: $size\n};
print qq{Content-Type: $file->{mime}\n};
print qq{Status: 200 OK\n\n};
print $cont;

###########################  End of Main ######################################
exit; #--1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###########################  End of Main ######################################

#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----
###############################################################################
1;
###############################################################################
