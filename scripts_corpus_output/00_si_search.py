#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, codecs, re
from collections import Counter

# provide the path to the folder with transcripts
INPUT_DIRECTORY = "speaker_files/tagged/"
INPUT_FILES = sorted([file for file in os.listdir(INPUT_DIRECTORY) if re.match(r'TIM.+tagged\.txt$',file)])


# specify the length of context for search before and after (in words)
context_before = 3
context_after = 3

# specify the length of context for results before and after (in words)
results_before = 15
results_after = 15


# ================================================================================
# Imports

import sys
import codecs
import re
import os


# ================================================================================
# functions

#function that creats a string out of the whole file, with . as the utterance boundary
def file_to_str(infile):
    non_verbal_list = [u'((?))', u'.', u'#', u'•', u'••', u'•••']
    filestring = str()
    for line in infile:
        line = line.strip()
        if len(line.split('\t')) < 3:
            if line.split('\t')[0] in non_verbal_list:
                pass
            else:
                line = ".\tZ\t.\n\t\t"  # adding a fullstop as an utterance boundary, for the visual output

        filestring += " " + line
    return filestring

# create a string out of words in a list of tokens
def token_list_to_str_words(token_list):
    str_words = str()
    for item in token_list:
        word=item.split('\t')[0]
        str_words+=word+' '

    return str_words

def token_list_to_str_lemmas(token_list):
    str_lemmas = str()
    for item in token_list:
        lemma=item.split('\t')[2]
        str_lemmas+=lemma+' '

    return str_lemmas

def token_list_to_word_list(token_list):
    word_list = []
    for item in token_list:
        word=item.split('\t')[0]
        word_list.append(word)
        
    return word_list


def token_list_to_pos_list(token_list):
    pos_list = []
    for item in token_list:
        pos = item.split('\t')[1]
        pos_list.append(pos)

    return pos_list


def token_list_to_lemma_list(token_list):
    lemma_list = []
    for item in token_list:
        lemma = item.split('\t')[2]
        lemma_list.append(lemma)

    return lemma_list


# ================================================================================


# ================================================================================
# create output file
OUTFILE = codecs.open('00_si_out.txt', 'w', 'utf-8')

not_2pers = [u'sam', u'nesam', u'nisam', u'ja', u'on', u'smo', u'one', u'da', u'on', u'nešto']

si_occurences = []

for transcript in INPUT_FILES:

    filename = INPUT_DIRECTORY + transcript

    with codecs.open(filename, 'r', 'utf8') as input_file:

        # creating a list of tokens with '.' between utterances
        filestring = file_to_str(input_file)
        # putting the tokens into a list
        filelist = filestring.split(' ') # reading the whole file in a list . utterance boundary

        for i in range(0,len(filelist)-1):

            # creating tokens: each token has the structure "word\tpos\tlemma", \t tab is a separator
            token = filelist[i]
            try:
                word = token.split('\t')[0]
                pos = token.split('\t')[1]
                lemma = token.split('\t')[2]
                word_pre1 = filelist[i-1].split('\t')[0]
                pos_pre1 = filelist[i-1].split('\t')[1]
                lemma_pre1 = filelist[i-1].split('\t')[2]
                word_pre2 = filelist[i - 2].split('\t')[0]
                pos_pre2 = filelist[i - 2].split('\t')[1]
                lemma_pre2 = filelist[i - 2].split('\t')[2]
                word_post1 = filelist[i + 1].split('\t')[0]
                pos_post1 = filelist[i + 1].split('\t')[1]
                lemma_post1 = filelist[i + 1].split('\t')[2]
                word_post2 = filelist[i + 2].split('\t')[0]
                pos_post2 = filelist[i + 2].split('\t')[1]
                lemma_post2 = filelist[i + 2].split('\t')[2]
                word_post3 = filelist[i + 3].split('\t')[0]
                pos_post3 = filelist[i + 3].split('\t')[1]
                lemma_post3 = filelist[i + 3].split('\t')[2]


                if word.lower() == "si":


                    if not word_pre1.lower() in [u"e", u"jel",  u"el", u"odakle", u'odokle']:

                        contextpre = filelist[(i - context_before): i]  # context length in words
                        contextpost = filelist[i: (i + context_after)]  # context length in words
                        context = contextpre+contextpost
                        words_in_context = token_list_to_word_list(context)
                        pos_in_context = token_list_to_pos_list(context)
                        lemmas_in_context = token_list_to_lemma_list(context)

                        if not "ti" in [word.lower() for word in words_in_context]:

                            si_occurences.append(transcript)


                        else:
                            pass



            except IndexError:
                pass


si_per_spk = Counter(si_occurences)

for item in si_per_spk:
    OUTFILE.write(item + '\t' + str(si_per_spk[item]) + '\n')

OUTFILE.close()


