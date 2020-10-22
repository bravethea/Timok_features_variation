#!/usr/bin/python
# -*- coding: utf-8 -*-



# ================================================================================
# Imports

import sys
import codecs
import re
import os



# --------------------------------------------------------
# input files
# --------------------------------------------------------
INPUT_DIRECTORY = "speaker_files/text/"
INPUT_FILES = sorted([file for file in os.listdir(INPUT_DIRECTORY) if file.endswith('.txt')])

# ================================================================================
# create output file
OUTPUT_FILE = codecs.open('00_accent_match_out.txt', 'w', 'utf8')


# ================================================================================
# list of words

nonst_words = [u'brazdA', u'brazdU', u'vodA', u'vodU', u'glavA', u'glavU', u'gredA', u'gredU',
               u'zvezdA', u'zvezdU', u'zemljA', u'zemljU', u'zimA', u'zimU', u'zorA', u'zorU',
               u'ženA', u'ženU', u'iglA', u'iglU', u'kozA', u'kozU', u'kosA', u'kosU',
               u'maglA', u'maglU', u'metlA', u'metlU', u'nogA', u'nogU', u'ovcA', u'ovcU',
               u'rekA', u'rekU', u'rukA', u'rukU', u'svinjA', u'svinjU', u'svećA', u'svEću',
               u'svečA', u'svečU', u'sestrA', u'sestrU', u'snajA', u'snajU', u'torbA', u'torbU',
               u'međA', u'medžA', u'međU', u'medžU', u'plAnina', u'plAninu', u'decA', u'decU', u'dEte',
               u'mlekO', u'čovEk', u'ručA', u'krstOvi', u'kakvO',
               u'takO', u'bilA', u'bilO', u'bilI', u'bilE', u'jedAn', u'jedWn', u'edAn', u'jednA', u'jednU',
               u'išlA', u'išAl', u'išlI', u'išlO', u'išlE', u'unUk', u'kakO', u'kojI', u'mojA',
               u'tvojA', u'tvA', u'timOk' ]

st_words = [u'brAzda', u'brAzdu', u'vOda', u'vOdu', u'glAva', u'glAvu', u'grEda', u'grEdu',
            u'zvEzda', u'zvEzdu', u'zEmlja', u'zEmlju', u'zIma', u'zImu', u'zOra', u'zOru',
            u'žEna', u'žEnu', u'Igla', u'Iglu', u'kOza', u'kOzu', u'kOsa', u'kOsu',
            u'mAgla', u'mAglu', u'mEtla', u'mEtlu', u'nOga', u'nOgu', u'Ovca', u'Ovcu',
            u'rEka', u'rEku', u'rUka', u'rUku', u'svInja', u'svInju', u'svEća', u'svEću',
            u'svEča', u'svEču', u'sEstra', u'sEstru', u'snAja', u'snAju', u'tOrba', u'tOrbu',
            u'mEđa', u'mEdža', u'mEđu', u'mEdžu' u'planIna', u'planInu', u'dEca', u'dEcu', u'dEte',
            u'mlEko', u'čOvek', u'rUčak', u'kRstovi', u'kAkvo',
            u'tAko', u'bIla', u'bIlo', u'bIli', u'bIle', u'jEdan', u'Edan', u'jEdwn', u'jEdna', u'jEdnu',
            u'nEsi', u'nEsu', u'nIsi', u'nIsu', u'nEsam', u'nEswm', u'nEsam', u'nEswm',
            u'Išla', u'Išal', u'Išli', u'Išlo', u'Išle', u'Unuk', u'kAko', u'kOji', u'mOja',
            u'tvOja', u'Tva', u'tImok']


OUTPUT_FILE.write("transcript" + "," + "st_words_count" + "," + "nonst_words_count" + '\n')

for transcript in INPUT_FILES:

    filename = INPUT_DIRECTORY+transcript

    token_count = 0
    st_words_count = 0
    nonst_words_count = 0


    with codecs.open(filename, 'r', 'utf8') as input_file:

        # going through file
        for line in input_file:


            line = line.strip()
            utterance = line.split(': ')[1]
            utterance_list = utterance.split(" ")

            word = utterance_list[0]

            if word in st_words:
                st_words_count+=1

            if word in nonst_words:
                nonst_words_count+=1

        OUTPUT_FILE.write(transcript + "," +
                          str(st_words_count) + "," + str(nonst_words_count) + '\n')


OUTPUT_FILE.close()