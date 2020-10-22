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
OUTPUT_FILE = codecs.open('00_perf_no_aux_out.txt', 'w', 'utf8')

perf_aux_list = [u'sam', u'nesam', u'nisam', u'nEsam', u'nIsam', u'nesAm', u'nisAm',
                 u'si', u'nesi', u'nisi', u'nEsi', u'nIsi', u'nesI', u'nisI',
                 u'smo', u'nesmo', u'nismo', u'nEsmo', u'nIsmo', u'nesmO', u'nismO',
                 u'ste', u'niste', u'neste', u'nIste', u'nEste', u'nistE', u'nestE',
                 u'smo', u'si.']
perf_aux_3_list = [u'je', u'e', u'neje', u'nE', u'nEe', u'ne'
                   u'su', u'nesu', u'nisu', u'nesU', u'nEsu', u'nIsu', u'nisU', u'su']

potenc_list = [u'bi',u'bih', u'bismo', u'biste', u'bIsmo', u'bIste', u'bismO', u'bistE']

not_list = [u'selO', u'cElo', u'al', u'[al', u'sElo', u'automobIli', u'ali',
            u'mAlo', u'[mAlo', u'kOlA', u'kOla', u'el', u'[el', u'il', u'ili',
            u'zavErgla', u'škOla', u'bEla', u'kao', u'mAli', u'nIkola', u'škOla',
            u'škOla', u'mAla', u'jel', u'pOsle', u'pOsla', u'prEdjelo', u'dOle',
            u'sEelo', u'Ili', u'đAvola', u'šakAli', u'Ali', u'vEli', u'li', u'vEli',
            u'Aali', u'jAao', u'okrUgal', u'okrUgla', u'ogrUglo', u'Ali', u'šAkali',
            u'ili', u'kAd/Ali', u'[Ali', u'li', u'al', u'nikOla', u'ali', u'ao',
            u'pOmali', u'razbOli', u'uzOkol', u'zaUrla', u'velI', u'sEla']

OUTPUT_FILE.write('trancript' + ',' + 'tokens' + ',' + 'perf_count' + ',' + 'perf_aux_count' + ',' + 'perf_aux_3_count' + ',' + 'perf_total_aux_count' + ',' + 'perf_no_aux_count' + ',' + "perf_no_aux_norm" + '\n')

for transcript in INPUT_FILES:

    filename = INPUT_DIRECTORY + transcript

    tokens_count = 0
    perf_count = 0
    perf_aux_count = 0
    perf_aux_3_count = 0
    potenc_count = 0
    perf_no_aux_count = 0

    with codecs.open(filename, 'r', 'utf8') as input_file:

        for line in input_file:

            line = line.strip()
            line = line.split(': ')[1]
            line_list = line.split(' ')

            # count tokens
            len_line = len(line_list)
            tokens_count+=len_line

            for i in range(0,len(line_list)):
                item = line_list[i]
                if re.match(r'.*([aeiou]l|la|lo|li|[aeiu]o)$', item) \
                        and not item in not_list:
                    # print line

                    perf_count += 1 # total participles

                    try:
                        if line_list[i-1] in perf_aux_list \
                            or line_list[i-2] in perf_aux_list \
                            or line_list[i-3]in perf_aux_list \
                            or line_list[i+1]in perf_aux_list:

                            # print line

                            perf_aux_count += 1 # first second person sg pl positive negative

                        elif line_list[i - 1] in perf_aux_3_list \
                                or line_list[i - 2] in perf_aux_3_list \
                                or line_list[i - 3] in perf_aux_3_list \
                                or line_list[i - 4] in perf_aux_3_list \
                                or line_list[i + 1] in perf_aux_3_list:

                            # print line

                            perf_aux_3_count += 1 # third person sg pl positive negative
                                #print line

                        elif line_list[i - 1] in potenc_list \
                             or line_list[i - 2] in potenc_list \
                             or line_list[i - 3] in potenc_list \
                             or line_list[i - 4] in potenc_list \
                             or line_list[i + 1] in potenc_list:

                            # print line

                            potenc_count+=1

                        else:
                            continue
                            # print line
                    except IndexError:
                        pass
        # print 'trancript' + ',' + 'perf_count' + ',' + 'perf_aux_count' + ',' + 'perf_aux_3_count' + ',' + 'perf_total_aux_count' + ',' + 'perf_no_aux_count'
        perf_total_aux_count = perf_aux_count+perf_aux_3_count
        perf_no_aux_count = perf_count - (perf_aux_count + perf_aux_3_count + potenc_count)

        try:
            perf_no_aux_norm = perf_no_aux_count * 1000 / perf_count
        except:
            perf_no_aux_norm = 0

        OUTPUT_FILE.write(transcript + ',' + str(tokens_count) + ',' + str(perf_count) + ',' + str(perf_aux_count) + ',' + str(perf_aux_3_count) + ',' + str(perf_total_aux_count) + ',' + str(perf_no_aux_count) +
                          ',' + str(perf_no_aux_norm) +
                          '\n')




OUTPUT_FILE.close()

# '''