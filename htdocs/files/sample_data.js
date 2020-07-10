/*
//*****************************************************************************
//*                                                                           *
//* File name: sample_data.js                                                 *
//* JavaScript to apply sample genomic and bisulfite seqeunce data            *
//* Author: Yuichi Kumaki (yuichi@kumaki.jp)                                  *
//* Copyright (C) 2008-2019 Yuichi Kumaki                                     *
//*                                                                           *
//* 2008/02/20 First open source version                                      *
//*                                                                           *
//*****************************************************************************
//*                                                                           *
//* This program is free software: you can redistribute it and/or modify      *
//* it under the terms of the GNU General Public License as published by      *
//* the Free Software Foundation, either version 3 of the License, or         *
//* (at your option) any later version.                                       *
//*                                                                           *
//* This program is distributed in the hope that it will be useful,           *
//* but WITHOUT ANY WARRANTY; without even the implied warranty of            *
//* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             *
//* GNU General Public License for more details.                              *
//*                                                                           *
//* You should have received a copy of the GNU General Public License         *
//* along with this program.  If not, see http://www.gnu.org/licenses/.       *
//*                                                                           *
//*****************************************************************************
*/

var gen = "CAAGAGAGCTGAGCTTGGAGAAACTCGATCTTCCAGTTCTACGTAGCTCGAGGCGGGAAGGCATCACACC\n\
ATAAATGCGCATGCACACGCGCACCTTGAAGGCTGGGCTTTTCTCAGCGAGCTCAGAGGCTCTCGTGAGA\n\
TTTCATCCTTAGTCTCGCTCTTCTGCCCCTTCCCCCACAAGACACAGGTTTTCCCTCCGAAAAACCACAC\n\
CCGGAAGCGTGTCACTCAATCCCCACAACAGCGTGCGTGCCCTTTGCAATCTGCGCAGTCCCCAACATCA\n\
CACATATGCACATTCTAGCCCTCCAATCTCTAGGGTTGTGTGAATGTGCCTCCCCACCGATCCGATCCCT\n\
AAGAACAGAAGACCTCTAGACAATCGAAACTGCAGCATCAAAAGCATCACAGCACATACAATCACAAACT\n\
TTATGTGTCTCCTAGCCTGTCCAATCCCCCACT\n\
";

var bi1 = ">Gm9_J1_seq_01\n\
AGATCGCATGCTCCGGCCGCCATGGCGGCCGCGCGATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTCGATTTTTTAGT\n\
TTTACGTAGTTTGAGGCGGGAAGGTATTATATTATAAATGCGTATGTATACGCGTATTTTGAAGGTTGGGTTTTTTTTAG\n\
CGAGTTTAGAGGTTTTCGTGAGATTTTATTTTTAGTTTCGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTT\n\
CGAAAAATTATATTCGGAAGCGTGTTATTTAATTTTTATAATAGCGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATA\n\
TTATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGAATA\n\
GAAGATTTTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTG\n\
TGTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGA\n\
TGCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGT\n\
TATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACT\n\
CACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACG\n\
CGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGC\n\
GGCGAGCGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGA\n\
>Gm9_J1_seq_02\n\
TGTCGCTGCTCCGGCCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTCGATTTTTTAGTT\n\
TTACGTAGTTCGAGGCGGGAAGGTATTATATTATAAATGCGTATGTATACGCGTATTTTGAAGGTTGGGTTTTTTTTGGC\n\
GAGTTTAGAGGTTTTCGTGAGATTTTATTTTTAGTTTCGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTC\n\
GAAAAATTATATTCGGAAGCGTGTTATTTAATTTTTATAATAGCGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATAT\n\
TATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTCATCGATTCGATTTTTAAGAATAG\n\
AAGATTTTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTT\n\
GTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGAT\n\
GCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTT\n\
ATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTC\n\
ACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACG\n\
CGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGC\n\
GGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGA\n\
GCAAAAGGCCAGCAAAAGGCCAGGA\n\
>Gm9_J1_seq_03\n\
TCTCCCGGCGCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGTTTTACGTAG\n\
TTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTAGTGAGTTTAG\n\
AGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTCGAAAAATT\n\
ATATTTGGAAGTGTGTTATTTAATTTTTATAATAGTGTGTGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTATATATA\n\
TGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGAATAGAAGATTTT\n\
TAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAATT\n\
TTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCT\n\
TGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTC\n\
ACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAAT\n\
TGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGA\n\
GAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCG\n\
GTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGG\n\
CCAGCAAAAGGCCAG\n\
>Gm9_J1_seq_04\n\
ACTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTCGATTTTTTAGTTTTATGTAG\n\
TTTGAGGTGGGAAGGTATTATATTATAAATGCGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTAGTGAGTTTAG\n\
AGGTTTTCGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTCGAAAAATT\n\
ATATTCGGAAGCGTGTTATTTAATTTTTATAATAGCGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTATATATA\n\
TGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGAATAGAAGATTTT\n\
TAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAATT\n\
TTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCT\n\
TGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTC\n\
ACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAAT\n\
TGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGA\n\
GAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCG\n\
GTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGG\n\
CCAGCAAAAGGCCAGGAA\n\
>Gm9_J1_seq_05\n\
AGTCGCCATGCGCGGCGCGCATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTCGATTTTTTAGTTTTACGTAGTTGGAG\n\
GCGGGAAGGTATTATATTATAAATGCGTATGTATACGCGTATTTTGAAGGTTGGGTTTTTTTTAGCGAGTTTAGAGGTTT\n\
TCGTGAGATTTTATTTTTAGTCTCGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTCCTCTTTTCGAAAAATTATATTC\n\
GGAAGCGTGTTATTTAATTTTTATAATAGCGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTATATATATGTATA\n\
TTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGAATAGAAGATTTTTAGATA\n\
ATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAATTTTTTAT\n\
TAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTTGAGTA\n\
TTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAATT\n\
CCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATTGCGTT\n\
GCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAGGCG\n\
GTTTGCGTATTGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGCGAGCGTATCAGCT\n\
CACTCAAAGGCGTATACGGTTATCCACAGAATCAGGGATACGCAGGAAAGACATGTGAGCAAAGGCCAGCAAAAGGCCAG\n\
GACCGTAAAAGGCCGCG\n\
>Gm9_J1_seq_06\n\
GTCGTAGTCGCTGCTCCGGCGCCATGGCGGCCGCGGGAATTCGATTGAGAATGGGTTAGAATTTTGAGGTAGGAGTTGAT\n\
GTAGAGGTTATGGAGGGGTGTTGTTTATTGGTTTGTTTTTTTATAGAATTAGGGTATTAGTTTAGGGGTGGTAATATTTA\n\
TTATGGGTTGATTTTTTTTTTATTGATTATTGATTGAAAAAAATGTTTTATAGTTGGATTTTATGGAGGTATTTTTTTAA\n\
TTGAAGTTTTTTTTTTGTGATGGTTCGATTTTGTGTTAAGTTGATATATAAAATTAGTTAGTATAAGTATTTAGATGTTA\n\
TTTATTGTTTATTTTTTTGTTTTTGTTTTATTTAATTTTTTGTGTTTTTTAGTTTGTTTAATTTTTTATTAATCACTAGT\n\
GAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTTGAGTATTCTATAGTGT\n\
CACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAATTCCACACAACAT\n\
ACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATTGCGTTGCGCTCACTGC\n\
CCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAGGCGGTTTGCGTATT\n\
GGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAA\n\
GGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGA\n\
ACCGTAAAAAGGCCGCGTTGCTGGCGTTTTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGT\n\
CAGAGGTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCTGGAAGCTCC\n\
>Gm9_J1_seq_07\n\
GCCGAGTCGCATGCTCCGGCCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTCGATTTTT\n\
TAGTTTTACGTAGTTTGAGGCGGGAAGGTATTATATTATAAATGCGTATGTATACGCGTATTTTGAAGGTTGGGTTTTTT\n\
TTAGCGAGTTTAGAGGTTTTCGTGAGATTTTATTTTTAGTTTCGTTTTTTTGTTTTTTTTTTATAAGATATAGGTTTTTT\n\
TTTCGAAAAATTATATTCGGAAGCGTGTTATTTAATTTTTATAATAGCGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTA\n\
ATATTATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGA\n\
ATAGAAGATTTTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTA\n\
GTTTGTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTT\n\
GGATGCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAAT\n\
TGTTATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTA\n\
ACTCACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCC\n\
AACGCGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGG\n\
CTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACAT\n\
GTGAGCAAAAGGCCA\n\
>Gm9_J1_seq_08\n\
GTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTCGATTTTTTAGTTTTACGTAGT\n\
TCGAGGCGGGAAGGTATTATATTATAAATGCGTATGTATACGCGTATTTTGAAGGTTGGGTTTTTTTTAGTGAGTTTAGA\n\
GGTTTTCGTGAGATTTTATTTTTAGTTTCGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTCGAAAAATTA\n\
TATTCGGAAGTGTGTTATTTAATTTTTATAATAGCGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTATATATAT\n\
GTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTTGATTTTTAAGAATAGAAGATTTTT\n\
AGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAATTT\n\
TTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTT\n\
GAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCA\n\
CAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATT\n\
GCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAG\n\
AGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGG\n\
TATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGC\n\
CAGCAAAGGCCAGGAACC\n\
>Gm9_J1_seq_09\n\
CCCCCGGCCCCCCCGTGGGGGGCGCCGGGGAACCCACGATTCGATGAGTGGTGGTTCGCCCCCCCTACTCTCCCCTCCCC\n\
TACACACATCGTCCGGAGGCGACAATATTATATATGAGAAGGGCATCTGGACCCGTGAGATTGGGGGTGTCTTTTTTTTG\n\
GGCCGGGGTGAGCGGGAGACGAGACTTCAATACTTATCGCTCCTTTTTTGTGTTATTTATAAAGAAAAGAAACTTTTCTT\n\
TCCAAAAAACAACAGTATCCGAGGGTAATACATACCAATTATATGCCCCCCGCCCTTTTTTTTTCAAGCGGGCATATTCT\n\
TCAAACCAACGTACTTTCTGTTCCTCCTAATTTACGGGGGGGGGGAGGGTGATGTCTGCCCCCACCCGCGCTTACCACAA\n\
AAAAAGATCTATACCTCCCCAATCGAATTTGTCGGCGAAACGGGTTAAATAGTAAATATAGAATCAAACGTGTTCTG\n\
>Gm9_J1_seq_10\n\
TGCATGCTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGTTTTA\n\
TGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTAGTGAG\n\
CTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTGAAA\n\
AATTATATTTGGAAGCGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTATA\n\
TATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGAACAGAAGA\n\
TTTTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTT\n\
AATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCAT\n\
AGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCC\n\
GCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACAT\n\
TAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCG\n\
GGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCG\n\
AGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAA\n\
AAGGCCAGCAAAAGGCCAGGAACCGTAAAAAGGCCGCGTTGCTGGC\n\
>Gm9_J1_seq_11\n\
AATCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTCGATTTTTTAGTTTTACGTAGTTTG\n\
AGGCGGGAAGGTATTATATTATAAATGCGTATGTATACGCGTATTTTGAAGGTTGGGTTTTTTTTAGCGAGTTTAGAGGT\n\
TTTCGTGAGATTTTATTTTTAGTTTCGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTCGAAAAATTATAT\n\
TCGGAAGCGTGTTATTTAATTTTTATAATAGCGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATACTATATATATGTA\n\
TATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGAATAGAAGATTTTTAGA\n\
TAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATCATAAATTTTATGTGTTTTTTAGTTTGTTTAATTTTTT\n\
ATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTTGAG\n\
TATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAA\n\
TTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATTGCG\n\
TTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAGG\n\
CGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGTATC\n\
AGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCA\n\
AAAGGCCAGGACCGT\n\
>Gm9_J1_seq_12\n\
CTAGTCGCTGCTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGT\n\
TTTACGTAGTTCGAGGCGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTTA\n\
GTGAGTTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTATAAGATATAGGTTTTTTTTT\n\
CGAAAAATTATATTCGGAAGTGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATA\n\
TTATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTTGATTTTTAAGAATA\n\
GAAGATTTTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTT\n\
TGTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGA\n\
TGCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGT\n\
TATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACT\n\
CACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAAC\n\
GCGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTG\n\
CGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGT\n\
GAGCAAAAGGCCAGCAAAAGGCCAGGAACCGTAAAAAGGCCGCGTTGCT\n\
>Gm9_J1_seq_13\n\
ATGCTCCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTCGATTTTTTAGTTTTACG\n\
TAGTTCGAGGCGGGAAGGTATTATATTATAAATGCGTATGTATACGCGTATTTTGAAGGTTGGGTTTTTTTTAGCGAGTT\n\
TAGAGGTTTTCGTGAGATTTTATTTTTAGTTTCGTTTTTTTGTTTTTTTTTTTTATAAGATATAGGTTTTTTTTTCGAAA\n\
AATTATATTCGGAAGCGTGTTATTTAATTTTTATAATAGCGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTATA\n\
TATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTCATCGATTCGATTTTTAAGAATAGAAGA\n\
TTTTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTT\n\
AATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCAT\n\
AGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCC\n\
GCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACAT\n\
TAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCG\n\
GGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCG\n\
AGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAA\n\
AAGGCCAGCAAAAGGCCA\n\
>Gm9_J1_seq_14\n\
GGTGTCGCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGTTTTACGTAGTTC\n\
GAGGCGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTAGTGAGTTTAGAGG\n\
TTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTCGAAAAATTATA\n\
TTCGGAAGTGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTATATATATGT\n\
ATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTTGATTTTTAAGAATAGAAGATTTTTAG\n\
ATAATTGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAATTTTT\n\
TATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTTGA\n\
GTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACA\n\
ATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATTGC\n\
GTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAG\n\
GCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTA\n\
TCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCA\n\
GCAAAGGCCAGGAACCGT\n\
>Gm9_J1_seq_15\n\
CTCCGGCCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGATTTGGAGAAATTCGATCTTCCAGTTCTACATAGT\n\
TTGAGGCGGGAAGGCATCACACCATAAATGCGTATGTACACGCGTATCTTGAAGGCTGGGTTTTTCTCAGCGAGCTCAGA\n\
GGCTCTCGTGAGATTTCATCCTTAGTCTCGCTCTTTTGTTGTTTTTTTTATAAGATATAGGTTTTTTTTTCGAAAAACCA\n\
CACCCGGAAGCGTGTCACTCAATCCCCACAACAGCGTGCGTGCCCTTTGCAATCTGCGCAGTCCTCAACATCACACATAT\n\
GCACATTCTAGCCCTCCAATTTCTAGGGTTGTGTGAATGTGCCTTTCCACCGATCCGATTTTTAAGAATAGAAGATTTTT\n\
AGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAATTT\n\
TTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTT\n\
GAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCA\n\
CAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATT\n\
GCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAG\n\
AGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGG\n\
TATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAGGCC\n\
AGC\n\
>Gm9_J1_seq_16\n\
CGGAGTCGCATGCTCCCGGCGCATGGCGGCCGCGGGAATTCGATATAAGAGAGTTGAGTTTGGAGAAATTCGATTTTTTA\n\
GTTTTACGTAGTTCGAGGCGGGAAGGTATTATATTATAAATGCGTATGTATACGTGTATTTTGAAGGTTGGGTTTTTTTT\n\
AGTGAGTTTAGAGGTTTTCGTGAGATTTTATTTTTAGTTTCGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTT\n\
TTCGAAGAATTATATTCGGAAGCGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAA\n\
TATTATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATTGATTCGATTTTTAAGAA\n\
TAGAAGACTTTTAGATAGTCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAG\n\
TTTGTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTG\n\
GATGCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATT\n\
GTTATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAA\n\
CTCACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCAA\n\
CGCGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCT\n\
GCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGT\n\
GAGCAAAAGGCCA\n\
";

var bi2 = ">Gm9_16aabb_seq_01\n\
ACTCGCATGCTCCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGT\n\
TTTATGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTAG\n\
TGAGTTTAGAGGTTTTTGTGAGATTTTGTTTTTAGTTTTGTTTTTTTGTTTTTTTTTTATAAGATATAGGTTTTTTTTTT\n\
GAAAAATTATATTTGGAAGTGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGTGTAGTTCTTAATAT\n\
TATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGACTCGATTTTTAAGGATAG\n\
AAGATTTTTAGATAATTGAAATTGTAGTATTAAAGGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTT\n\
GTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGAT\n\
GCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTT\n\
ATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTC\n\
ACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACG\n\
CGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGC\n\
GGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGA\n\
GCAAAAGGCCA\n\
>Gm9_16aabb_seq_02\n\
TTCGAGTCGCATGCTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTT\n\
AGTTTTATGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGCGTGTTTTGAAGGTTGGGTTTTTTT\n\
TAGTGAGTTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTCTGTTTTTTTTTTTATAAGATATAGGTTTTTT\n\
TTTTGAAAAATTATATTTGGAAGCGTGTTATTTAATTTTTATAATAGTGTGTGTGTTTTTTGTAATTTGTGTAGTTTTTA\n\
ATATTATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATTGATTTGATTTTTAAGA\n\
ATAGAAGATTTTTAGATAATTGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTA\n\
GTTTGTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTT\n\
GGATGCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAAT\n\
TGTTATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTA\n\
ACTCACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCC\n\
AACGCGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGG\n\
CTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACAT\n\
GTGAGCAAAGGCCAGCA\n\
>Gm9_16aabb_seq_03\n\
GGCCTATCGCTTCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGG\n\
TAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGAACCGT\n\
AAAAAGGCCGCGTTGCTGGCGTTTTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCAGAG\n\
GTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTCCTGTTCCGACCC\n\
TGCCGCTTACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGCTGTAGGTATCTC\n\
AGTTCGGTGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTGCGCCTTATCCGG\n\
TAACTATCGTCTTGAGTCCAACCCGGTAAGACACGACTTATCGCCACTGGCAGCAGCCACTGGTAACAGGATTAGCAGAG\n\
CGAGGTATGTAGGCGGTGCTACAGAGTTCTTGAAGTGGTGGCCTAACTACGGCTACACTAGAAGAACAGTATTTGGTATC\n\
TGCGCTCTGCTGAAGCCAGTTACCTTCGGAAAAAGAGTTGGTAGCTCTTGATCCGGCAAACAAACCACCGCTGGTAGCGG\n\
TGGTTTTTTTGTTTGCAAGCAGCAGATTACGCGCAGAAAAAAAGGATCTCAAGAAGATCCTTTGATCTTTTCTACGGGGT\n\
CTGACGCTCAGTGGAACGAAAACTCACGTTAAGGGATTTTGGTCATGAGATTATCAAAAAGGATCTTCACCTAGATCCTT\n\
TTAAATTAAAAATGAAGTTTTAAATCAATCTAAAGTATATATGAGTAAACTTGGTCTGACAGTTACCAATGCTTAATCAG\n\
TGAGGCACCTATCTCAGCGATCTGTCTATTTCGTTCATCCATAGG\n\
>Gm9_16aabb_seq_04\n\
ATGCTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTGGTTTTATGT\n\
AGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTAGTGAGTTT\n\
AGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTCGAAAAA\n\
TTATATTCGGAAGCGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTATATA\n\
TATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTTGATTTTTAAGAATAGAAGATT\n\
TTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAA\n\
ATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATA\n\
GCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCG\n\
CTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATT\n\
AATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGG\n\
GGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGA\n\
GCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAA\n\
AGGCCAGCAAAGGC\n\
>Gm9_16aabb_seq_05\n\
AGATGCCTGCTCCCGGCCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAG\n\
TTTTACGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATACGCGTATTTTGAAGGTTGGGTTTTTTTTA\n\
GTGAGTTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTCTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTT\n\
TTGAAAAATTATATTTGGAAGTGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAAT\n\
ATTATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATTGATTTGATTTTTAAGAAT\n\
AGAAGATTTTTAGATAATTGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGT\n\
TTGAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTTGAG\n\
TATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAA\n\
TTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATTGCG\n\
TTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAGG\n\
CGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTAT\n\
CAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCGGAAAGAACATGTGAGCAAAAGGCCAGC\n\
AAAAGGCAGGAACCGTAAGAAGG\n\
>Gm9_16aabb_seq_06\n\
TGCATGCTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGTTTTA\n\
TGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTGTGTATATGCGTATTTTGAAGGTTGGGTTTTTTTTAGTGAG\n\
TTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTTGAA\n\
AAATTATATTTGGAAGCGTGTTATTTAATTTTTATAATAGTGTGTGTGTTTTTTGTAATTTGCGTAGTTTTTAATATTAT\n\
ATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGAATAGAAG\n\
ATTTTTAGATAATTGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTT\n\
TAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCA\n\
TAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATC\n\
CGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACA\n\
TTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGC\n\
GGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGC\n\
GAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCA\n\
AAAGGCCAGCAAAAGGCCAGGAACCG\n\
>Gm9_16aabb_seq_07\n\
CCTCCCCCCGGCCCCCCTGTGCGGCCGCGGGATTCCATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGTTTTA\n\
TGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTAATGAG\n\
TTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAAATATAGGTTTTTTTTTCGAA\n\
AAATTATATTCGGAAGCGGGTTATTTAATTTTTATAATAGTGTGGGTGTTTTTTGTAATTTGGGTAATTTTTAATATTAT\n\
AAATATGTATATTTTAGTTTTTTAATTTTCAGGGTTGGGGGAATGGGTTTTTTTATTGCTTCGATTTTTAACAATACAAG\n\
ATTTTTAGATAATTGAAATTGCAGTATTAAAAGGATTAAAGTATATATAAATATAAATTTCATGTGTTTTTTAGTTTGTT\n\
TAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCA\n\
TAGCTTGAGTATTCTATACTGTCACCTAAATAGCTTGGCCTAGTCATGGCCCTAGCTGTTTCCTGTGTGAACTCGTTATC\n\
CGCTCACACTTCCACACAACATACAAGCCGGAAGCTTACAGCGTAAAGCATGGGGTGCCTAATCACAGAGCTAACTCACA\n\
TTAATTGCCTTGCTCTCACTGCGCGCTTTCCACTCAGCAAACCTGTCTTGCCAGCTGCCTTATTGAATCGGCCAACGCGC\n\
GCCGAAACGCGGATTGCTTATTGGGCGCTCTCCCGCTTACTCACTCACTGACTCCCTGCGCTCGGTCGCTCGGGTGCGGC\n\
GAGCGAATCAGCTCACTCAAAGGACGGAAGACGCGTATCTCCCCAATCGGGGGCTACGCACGAACCACATCGGACCAGAG\n\
GCTAGCACAACCCAC\n\
>Gm9_16aabb_seq_08\n\
GCGTAGTCGCTGCTCCGGCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTTGAGTATTCT\n\
ATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAATTCCAC\n\
ACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATTGCGTTGCGC\n\
TCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAGGCGGTTT\n\
GCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTC\n\
ACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAG\n\
GCCAGGAACCGTAAAAAGGCCGCGTTGCTGGCGTTTTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACG\n\
CTCAAGTCAGAGGTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTC\n\
CTGTTCCGACCCTGCCGCTTACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGC\n\
TGTAGGTATCTCAGTTCGGTGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTG\n\
CGCCTTATCCGGTAACTATCGTCTTGAGTCCAACCCGGTAAGACACGACTTATCGCCACTGGCAGCAGCCACTGGTAACA\n\
GGATTAGCAGAGCGAGGTATGTAGGCGGTGCTACAGAGTTCTTGAAGTGGTGGCCTAACTACGGCTACACTAGAAGAACA\n\
GTATTTGGTATCTGCGCTCTGCTGAAGCCAGTT\n\
>Gm9_16aabb_seq_09\n\
TGCTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGTTTTATGTA\n\
GTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGCGTGTTTTGAAGGTTGGGTTTTTTTTAGTGAGTTTA\n\
GAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTATAAGATATAGGTTTTTTTTTTGAAAAATT\n\
ATATTTGGAAGCGTGTTATTTAATTTTTATAATAGTGTGTGTGTTTGTTGTAATTTGTGTAGTTTTTAATATTATATATA\n\
TGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATTGATTTGATTTTTAAGAATAGAAGATTTT\n\
TAGATAATTGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAATT\n\
TTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCT\n\
TGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTC\n\
ACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAAT\n\
TGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGA\n\
GAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCG\n\
GTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGG\n\
CCAGCAAAGGCCAGGAACCGTAAAAGGCCGCGTTGC\n\
>Gm9_16aabb_seq_10\n\
GGACCAAGTTGAATGTTCCCGGCCGCGATGGGGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATT\n\
TTTTAGTTTTATGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGCGTATTTTGAAGGTTGGGTTT\n\
TTTTTAGTGAGTTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTT\n\
TTTTTTTCGAAAAATTATATTTGGAAGCGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGCGTAGTT\n\
TTTAATATTATATATATGTATATTTTAGTTTTTTAAATTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTT\n\
AAGAATAGAAGATTTTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTT\n\
TTTAGTTTGTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACG\n\
CGTTGGATGCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTG\n\
AAATTGTTATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGA\n\
GCTAACTCACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATC\n\
GGCCAACGCGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGT\n\
TCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGATGTCCACAGAGTCAGGGGATAACGCAGGAAGAC\n\
ATGTGAGCAAATGCCAGCAAAGGCCAGGAACCGTAGAAAGGCCGCG\n\
>Gm9_16aabb_seq_11\n\
GAGTCGCATGCTCCGGCCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAG\n\
TTTTATGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTA\n\
GTGAGTTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTATAAGATATAGGTTTTTTTTT\n\
GAAAAATTATATTCGGAAGCGTGTTATTTAATTTTTATAATAGTGTGCGTGTTTTTTGTAATTTGCGTAGTTTTTAATAT\n\
TATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATCGATTCGATTTTTAAGAATAG\n\
AAGATTTTTAGATAATCGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTT\n\
GTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGAT\n\
GCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTT\n\
ATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTC\n\
ACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACG\n\
CGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGC\n\
GGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGA\n\
GCAAAAGGCCAGCAAAAGGCCA\n\
>Gm9_16aabb_seq_12\n\
ACTCGCATGCTCCGGCGCCATGGCGGCCGCGGGAATTCGATTTAAGAGAGTTGAGTTTGGAGAAATTTGATTTTTTAGTT\n\
TTATGTAGTTTGAGGTGGGAAGGTATTATATTATAAATGTGTATGTATATGTGTATTTTGAAGGTTGGGTTTTTTTTAGT\n\
GAGTTTAGAGGTTTTTGTGAGATTTTATTTTTAGTTTTGTTTTTTTGTTTTTTTTTTTATAAGATATAGGTTTTTTTTTC\n\
GAAAAATTATATTCGGAAGTGTGTTATTTAATTTTTATAATAGTGTGTGTGTTTTTTGTAATTTGTGTAGTTTTTAATAT\n\
TATATATATGTATATTTTAGTTTTTTAATTTTTAGGGTTGTGTGAATGTGTTTTTTTATTGATTCGATTTTTAAGAATAG\n\
AAGATTTTTAGATAATTGAAATTGTAGTATTAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTT\n\
GTTTAATTTTTTATTAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGAT\n\
GCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTT\n\
ATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTC\n\
ACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACG\n\
CGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGC\n\
GGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGA\n\
GCAAAAGGCCAGCAAAAGGCCAGGAACC\n\
>Gm9_16aabb_seq_13\n\
ACATTCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACG\n\
GTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGAACCGTAAAAAGG\n\
CCGCGTTGCTGGCGTTTTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCAGAGGTGGCGA\n\
AACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTCCTGTTCCGACCCTGCCGCT\n\
TACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGCTGTAGGTATCTCAGTTCGG\n\
TGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTGCGCCTTATCCGGTAACTAT\n\
CGTCTTGAGTCCAACCCGGTAAGACACGACTTATCGCCACTGGCAGCAGCCACTGGTAACAGGATTAGCAGAGCGAGGTA\n\
TGTAGGCGGTGCTACAGAGTTCTTGAAGTGGTGGCCTAACTACGGCTACACTAGAAGAACAGTATTTGGTATCTGCGCTC\n\
TGCTGAAGCCAGTTACCTTCGGAAAAAGAGTTGGTAGCTCTTGATCCGGCAAACAAACCACCGCTGGTAGCGGTGGTTTT\n\
TTTGTTTGCAAGCAGCAGATTACGCGCAGAAAAAAAGGATCTCAAGAAGATCCTTTGATCTTTTCTACGGGGTCTGACGC\n\
TCAGTGGAACGAAAACTCACGTTAAGGGATTTTGGTCATGAGATTATCAAAAAGGATCTTCACCTAGATCCTTTTAAATT\n\
AAAAATGAAGTTTTAAATCAATCTAAAGTATATATGAGTAAACTTGGTCTGACAGTTACCAATGCTTAATCAGTGAGGCA\n\
CCTATCTCAGCGATCTGTCTATTTCGTTCA\n\
>Gm9_16aabb_seq_14\n\
AAGTCGCATGCTCCGGCGCATGGCGGCCGCGGGAATTCGATTAAGAATAGAAGATTTTTAGATAATCGAAATTGTAGTAT\n\
TAAAAGTATTATAGTATATATAATTATAAATTTTATGTGTTTTTTAGTTTGTTTAATTTTTTATTAATCACTAGTGAATT\n\
CGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGATGCATAGCTTGAGTATTCTATAGTGTCACCT\n\
AAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAATTCCACACAACATACGAG\n\
CCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATTGCGTTGCGCTCACTGCCCGCT\n\
TTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAGGCGGTTTGCGTATTGGGCG\n\
CTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGG\n\
TAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGAACCGT\n\
AAAAAGGCCGCGTTGCTGGCGTTTTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCAGAG\n\
GTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTCCTGTTCCGACCC\n\
TGCCGCTTACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGCTGTAGGTATCTC\n\
AGTTCGGTGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTGCGCCTTATCCGG\n\
TAACTATCGTCTTGAGTCC\n\
>Gm9_16aabb_seq_15\n\
GCCCCGCCGACCGCGCTCGCCCGCGGGAATTCGATCTAAGGAATTCGGGGGCGCCTGCATGTCAACCATATGGGAGAGCT\n\
CCCAACCCGTTGGATGCATAGCTTGAATATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTC\n\
CTGTGTGAAATTGTTATCCGCTCACAATTCCACACAACATACGACCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAA\n\
TGAGTGAGCTAACTCACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTA\n\
ATGAATCGGCCAACGCGCGGGGAGAGGCGGTTTGCGGATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCT\n\
CGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCA\n\
TGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGAACCGTAAAAAGGTCGCATTACTGGCGTTTTTCCATAGGCT\n\
CCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCGGAGGTGGCGAAACCCGACAGGACTTGAAATATACCAGG\n\
CGTTTCCCCCTGGAAGCTCCCTCAAGCGCTCTCCTGTTCCGACGCTGCCGCATAGCGGATACCTGTCCGCCTGTCTGCCT\n\
TCTGGAAGCGTGGCGCTTACTCATAGCTCACGATGAAGGTATCTCAATTCGATGTAGGTCGTTCGCTCCAGGATGGGGTG\n\
TGTGCACGAACCCTCGTTCAGGCCGAGCGCTGCGCCTTATCCGGTAACTATCGTCGTGAGTCCAACCCGATCCGATAAAA\n\
CTAATCGGCACTGGTCAAACCCACTAGTAGCAGTATTAGTAGACCGGGGTCTGTAGGCGGCGCTCCATAAATCGTGAGGT\n\
GCCGACTTAA\n\
>Gm9_16aabb_seq_16\n\
TCACATGGCTCCCGGCGCCATGGCGGCCGCGGAATTCGATTAATAAAAAATTAAACAAACTAAAAAACACATAAAATTTA\n\
TAATTATATATACTATAATACTTTTAATACTACAATTTCGATTATCTAAAAATCTTCTATTCTTAAAAATCAAATCGATA\n\
AAAAAACACATTCACACAACCCTAAAAATTAAAAAACTAAAATATACATATATATAATATTAAAAACTACGCAAATTACA\n\
AAAAACACGCACACTATTATAAAAATTAAATAACACGCTTCCGAATATAATTTTTCGAAAAAAAAAACCTATATCTTATA\n\
AAAAAAAAAACAAAAAAACAAAACTAAAAATAAAATCTCACAAAAACCTCTAAACTCACTAAAAAAAACCCAACCTTCAA\n\
AATACACATATACATACACATTTATAATATAATACCTTCCCACCTCAAACTACATAAAACTGAAAAATCAAATCTCTCCA\n\
AACTCAACTCTCTTAAATCACTAGTGAATTCGCGGCCGCCTGCAGGTCGACCATATGGGAGAGCTCCCAACGCGTTGGAT\n\
GCATAGCTTGAGTATTCTATAGTGTCACCTAAATAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTT\n\
ATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTC\n\
ACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACG\n\
CGCGGGGAGAGGCGGTTTGCGTATTGGGCGCTCTTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGC\n\
GGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGA\n\
GCAAAAGGCCAGCAAAAGGCC\n\
";

function applyGen() {
  document.allform.genome.value = gen;
}

function applyBi1() {
  document.allform.multifasta.value = bi1;
}

function applyBi2() {
  document.allform.multifasta2.value = bi2;
}