#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,re,codecs
from collections import Counter


# specify the length of context for results before and after (in words)
results_before = 30
results_after = 30

# files
FOLDERPATH = 'speaker_files/tagged/'
FILES = sorted([file for file in os.listdir(FOLDERPATH) if file.endswith('tagged.txt')])

ARTICLES_DICT = { u'1erkata': [u'ćerka', u'Ncfsn-t'], u'1erkutu': [u'ćerka', u'Ncfsa-t'],
                 u'aljinete': [u'aljina', u'Ncfpn-t'], u'astalan': [u'astal', u'Ncmsn-n'],
                 u'avionat': [u'avion', u'Ncmsn-t'], u'avlijutu': [u'avlija', u'Ncfsa-t'],
                 u'babana': [u'baba', u'Ncfsn-n'], u'babata': [u'baba', u'Ncfsn-t'], u'babava': [u'baba', u'Ncfsn-v'],
                 u'babete': [u'baba', u'Ncfpn-t'], u'babinčevo': [u'babinče', u'Ncnsn-v'],
                 u'babutu': [u'baba', u'Ncfsa-t'], u'badnjakat': [u'badnjak', u'Ncmsn-t'],
                 u'badnjkat': [u'badnjk', u'Ncmsn-t'], u'banicutu': [u'banica', u'Ncfsa-t'],
                 u'barovat': [u'barov', u'Ncmsn-t'], u'baterijutu': [u'baterija', u'Ncfsa-t'],
                 u'baštata': [u'bašta' , u'Ncfsn-t'], u'baštunu': [u'bašta', u'Ncfsa-n'],
                 u'baštutu': [u'bašta', u'Ncfsa-t'], u'baščutu': [u'bašča', u'Ncfsa-t'],
                 u'biciklata': [u'bicikla', u'Ncfsn-t'], u'bobete': [u'boba', u'Ncfpn-t'],
                 u'bogata': [u'bog', u'Ncmsayt'], u'bogatiti': [u'bogat', u'Agpmsny-t'],
                 u'bogojavljenjeto': [u'bogojavljenje', u'Npnsn-t'], u'bogorodicata': [u'bogorodica', u'Ncfsn-t'],
                 u'bojat': [u'boj', u'Ncmsn-t'], u'boljeto': [u'dobro', u'Agcnsny-t'],
                 u'borakat': [u'borak', u'Ncmsn-t'], u'bosiljakav': [u'bosiljak', u'Ncmsn-v'],
                 u'brabinčevo': [u'brabinče', u'Ncnsn-v'], u'bracćiti': [u'braća', u'Ncmpn-t'],
                 u'bradeve': [u'brada', u'Ncfpn-v'], u'bratat': [u'brat', u'Ncmsn-t'],
                 u'bratata': [u'brat' , u'Ncmsayt'], u'bratatoga': [u'brat', u'Ncmsayt'],
                 u'bratav': [u'brat', u'Ncmsn-v'], u'brbinjevo': [u'brbinje', u'Ncnsn-v'],
                 u'brdilata': [u'brdila', u'Ncnpn-t'], u'brdljan': [u'brdlj', u'Ncmsn-n'],
                 u'brdono': [u'brdo', u'Ncnsn-n'], u'brdoto': [u'brdo', u'Ncnsn-t'],
                 u'bregat': [u'breg', u'Ncmsn-t'], u'brežakat': [u'brežak', u'Ncmsn-t'],
                 u'brvat': [u'brav', u'Ncmsn-t'], u'bubete': [u'buba', u'Ncfpn-t'],
                 u'bugariti': [u'Bugarin', u'Ncmpn-t'], u'bulkata': [u'bulka', u'Ncfsn-t'],
                 u'bučkutu': [u'bučka', u'Ncfsa-t'], u'bwlgariti': [u'bugarin', u'Ncmpn-t'],
                 u'bəlgariti': [u'bugarin', u'Ncmpn-t'], u'cenat': [u'cen', u'Ncmsn-t'],
                 u'cepotinutu': [u'cepotina', u'Ncfsa-t'], u'ceđat': [u'ceđ', u'Ncmsn-t'],
                 u'ciganjevi': [u'ciganin', u'Ncmpn-v'], u'cigankata': [u'ciganka', u'Ncfsn-t'],
                 u'cigankutu': [u'ciganka', u'Ncfsa-t'], u'ciglata': [u'cigla' , u'Ncfsn-t'],
                 u'crepnjete': [u'crepnja', u'Ncfpn-t'], u'crepnjutu': [u'crepnja', u'Ncfsa-t'],
                 u'crepuljete': [u'crepulja', u'Ncfpn-t'], u'crevistata': [u'crevista', u'Ncfsn-t'],
                 u'crkvata': [u'crkva', u'Ncfsn-t'], u'crkvunu': [u'crkva', u'Ncfsa-n'],
                 u'crkvutu': [u'crkva', u'Ncfsa-t'], u'crvenovo': [u'crven', u'Agpnsny-v'],
                 u'cvetakat': [u'cvetak', u'Ncmsn-t'], u'cveḱevo': [u'cveḱe', u'Ncnsn-v'],
                 u'danaskata': [u'danaska', u'Ncfsn-t'], u'danat': [u'dan', u'Ncmsn-t'],
                 u'datumat': [u'datum', u'Ncmsn-t'], u'de3icutu': [u'de3ica', u'Ncfsa-t'],
                 u'debeljat': [u'debeo', u'Agpmsny-t'], u'decana': [u'dete', u'Ncnpn-n'],
                 u'decata': [u'dete' , u'Ncnpn-t'], u'decava': [u'dete', u'Ncnpn-v'],
                 u'decutu': [u'deca', u'Ncfsa-t'], u'decuvu': [u'deca', u'Ncnpanv'],
                 u'dedata': [u'deda', u'Ncmsn-t'], u'dedava': [u'deda', u'Ncmsn-v'],
                 u'deduvu': [u'deda', u'Ncmsayt'], u'delat': [u'deo', u'Ncmsn-t'],
                 u'detenceto': [u'detence', u'Ncnsn-t'], u'deteno': [u'dete', u'Ncnsn-n'],
                 u'deteovo': [u'deteo', u'Ncnsn-v'], u'deveriti': [u'dever', u'Ncmpn-t'],
                 u'deverićićiti': [u'deverićić', u'Ncmpn-t'], u'devojkeve': [u'devojka', u'Ncfpn-v'],
                 u'devojqata': [u'devojka' , u'Ncfsn-t'], u'devojćete': [u'devojka', u'Ncfpn-t'],
                 u'devojčenceto': [u'devojčence', u'Ncnsn-t'], u'devojčeto': [u'devojče', u'Ncnsn-t'],
                 u'devojčevo': [u'devojče', u'Ncnsn-v'], u'devojčicata': [u'devojčica', u'Ncfsn-t'],
                 u'devoćete': [u'devoća', u'Ncfpn-t'], u'dečicata': [u'dečica', u'Ncnpn-t'],
                 u'dečicutu': [u'dečica', u'Ncfsa-t'], u'dečijava': [u'dečija', u'Ncfsn-v'],
                 u'dolat': [u'dol', u'Ncmsn-t'], u'domat': [u'dom', u'Ncmsn-t'], u'drešćete': [u'dreška', u'Ncfpn-t'],
                 u'dru2ijat': [u'drugi', u'Ncmsn-t'], u'drugaricutu': [u'drugarica', u'Ncfsa-t'],
                 u'drugata': [u'druga', u'Ncfsn-t'], u'drugete': [u'druge', u'Mlofpa-t'],
                 u'drugijat': [u'drugij', u'Mlomsn-t'], u'drugiti': [u'drugi', u'Mlompn-t'],
                 u'drugivi': [u'drugi', u'Ncmpn-v'], u'drugoto': [u'drugi', u'Mlonsn-t'],
                 u'drugutu': [u'druga', u'Ncfsa-t'], u'druguvu': [u'kuća', u'Mlofsayv'],
                 u'drumoto': [u'drumo', u'Ncnsn-t'], u'druǵijat': [u'druǵi', u'Mlomsn-t'],
                 u'drvičkata': [u'drvička', u'Ncfsn-t'], u'drvjata': [u'drvje', u'Ncnpn-t'],
                 u'drvoto': [u'drvo', u'Ncnsn-t'], u'drvovo': [u'drvo', u'Ncnsn-v'],
                 u'drwgoto': [u'drugi', u'Mlonsn-t'], u'držaljutu': [u'držalja', u'Ncfsa-t'],
                 u'drəgoto': [u'drugi', u'Mlonsn-t'], u'duhoviti': [u'duhovi', u'Ncmpn-t'],
                 u'dunjete': [u'dunja', u'Ncfpn-t'], u'duvanwt': [u'duvan', u'Ncmsn-t'],
                 u'duvanət': [u'duvan', u'Ncmsn-t'], u'dvanoto': [u'dvani', u'Mlonsn-t'],
                 u'dvorat': [u'dvor', u'Ncmsn-t'], u'džermanat': [u'Džerman', u'Ncmsn-t'],
                 u'džervinat': [u'džervin', u'Ncmsn-t'], u'emisijeve': [u'emisija', u'Ncfpn-v'],
                 u'fabrićete': [u'fabrika', u'Ncfpn-t'], u'fokloriti': [u'foklor', u'Ncmpn-t'],
                 u'frižiderat': [u'frižider', u'Ncmsn-t'], u'gazdata': [u'gazda', u'Ncmsn-t'],
                 u'generacijata': [u'generacija', u'Ncfsn-t'], u'germanat': [u'German', u'Ncmsn-t'],
                 u'gibanicuvu': [u'gibanica', u'Ncfsa-v'], u'gipsat': [u'gips', u'Ncmsn-t'],
                 u'glasat': [u'glas', u'Ncmsn-t'], u'glavata': [u'glava' , u'Ncfsn-t'],
                 u'glavnjutu': [u'glavnja', u'Ncfsa-t'], u'glavurinutu': [u'glavurina', u'Ncfsa-t'],
                 u'glavutu': [u'glava', u'Ncfsa-t'], u'glistete': [u'glista', u'Ncfpn-t'],
                 u'gljinete': [u'gljina', u'Ncfpn-t'], u'gluvata': [u'gluv', u'Agpfsny-t'],
                 u'gluvonemono': [u'gluvonem', u'Agpnsny-n'], u'gnjezdavoto': [u'gnjezdavo', u'Ncnsn-t'],
                 u'godžeto': [u'godže', u'Ncnsn-t'], u'golemutu': [u'golema', u'Ncfsa-t'],
                 u'gornjiti': [u'gornji', u'Agpmsny-t'], u'govedata': [u'govedo' , u'Ncnpn-t'],
                 u'gradat': [u'grad', u'Ncmsn-t'], u'gradinete': [u'gradina', u'Ncfpn-t'],
                 u'gradinunu': [u'gradina', u'Ncfsa-n'], u'gradinutu': [u'gradina', u'Ncfsa-t'],
                 u'gradoviti': [u'grad', u'Ncmpn-t'], u'gradžava': [u'gradža', u'Ncfsn-v'],
                 u'granicutu': [u'granica', u'Ncfsa-t'], u'greadinčevo': [u'greadinče', u'Ncnsn-v'],
                 u'grebeciti': [u'grebenac', u'Ncmpn-t'], u'grebenciti': [u'grebenc', u'Ncmpn-t'],
                 u'grmežat': [u'grmež', u'Ncmsn-t'], u'grnčariti': [u'grnčar', u'Ncmpn-t'],
                 u'grobat': [u'grob', u'Ncmsn-t'], u'grobljeno': [u'groblje', u'Ncnsn-n'],
                 u'grovinutu': [u'grovina', u'Ncfsa-t'], u'grsnicete': [u'grsnica', u'Ncfpn-t'],
                 u'grudnoto': [u'grudni', u'Agpnsny-t'], u'grznicete': [u'grznica', u'Ncfpn-t'],
                 u'gušata': [u'guša', u'Ncfsn-t'], u'gušava': [u'guša', u'Ncfsn-v'],
                 u'gušteriveve': [u'gušter', u'Ncmpn-v'], u'gvožđevo': [u'gvožđe', u'Ncnsn-v'],
                 u'igranćete': [u'igranća', u'Ncfpn-t'], u'imanjeto': [u'imanje', u'Ncnsn-t'],
                 u'ižutu': [u'iža', u'Ncfsa-t'], u'jabwl6ete': [u'jabuka', u'Ncfpn-t'],
                 u'jabəlḱete': [u'jabəlḱa', u'Ncfpn-t'], u'jaganjciti': [u'jaganjci', u'Ncmpn-t'],
                 u'jagnjeto': [u'jagnje', u'Ncnsn-t'], u'jedenjeto': [u'jedenje', u'Ncnsn-t'],
                 u'jedwnwt': [u'jedan', u'Mlcmsn-t'], u'jedənət': [u'jedən', u'Ncmsn-t'],
                 u'jutroto': [u'jutro', u'Ncnsn-t'], u'kWštata': [u'kuća' , u'Ncfsn-t'],
                 u'kafutu': [u'kafa', u'Ncfsa-t'], u'kaišat': [u'kaiš', u'Ncmsn-t'], u'kalupat': [u'kalup', u'Ncmsn-t'],
                 u'kamenat': [u'kamen', u'Ncmsn-t'], u'kamentat': [u'kamen', u'Ncmsn-t'],
                 u'kamionene': [u'kamion', u'Ncmpa-n'], u'kavaneto': [u'kavane', u'Ncnsn-t'],
                 u'kavuvu': [u'kava', u'Ncfsa-v'], u'kazančeto': [u'kazanče', u'Ncnsn-t'],
                 u'kerkutu': [u'kerka', u'Ncfsa-t'], u'kesunu': [u'kesa', u'Ncfsa-n'],
                 u'kladanat': [u'kladan', u'Ncmsn-t'], u'klepetarnikete': [u'klepetarnik', u'Ncmpa-t'],
                 u'klčinata': [u'klčina', u'Ncfsn-t'], u'knjaževwcav': [u'knjaževwc', u'Ncmsn-v'],
                 u'knjaževəcav': [u'Knjaževəc', u'Ncmsn-v'], u'knjigete': [u'knjiga', u'Ncfpn-t'],
                 u'knjigutu': [u'knjiga', u'Ncfsa-t'], u'knopljeto': [u'knoplje', u'Ncnsn-t'],
                 u'kobilunu': [u'kobila', u'Ncfsa-n'], u'kokete': [u'koka', u'Ncfpn-t'],
                 u'kokoxćeve': [u'kokoška', u'Ncfpn-v'], u'kokošćete': [u'kokošća', u'Ncfpn-t'],
                 u'kokošćetinene': [u'kokošćetina', u'Ncfpn-n'], u'kokošćeto': [u'kokošće', u'Ncnsn-t'],
                 u'kolata': [u'kola', u'Ncnpn-t'], u'kolatat': [u'kolat', u'Ncmsn-t'], u'kolačat': [u'kolač', u'Ncmsn-t'],
                 u'kolačiti': [u'kolač', u'Ncmpn-t'], u'kolibutu': [u'koliba', u'Ncfsa-t'],
                 u'koloto': [u'kolo', u'Ncnsn-t'], u'kompirat': [u'kompir', u'Ncmsn-t'],
                 u'kompirwt': [u'krompir', u'Ncmsn-t'], u'kompirət': [u'krompir', u'Ncmsn-t'],
                 u'komšikana': [u'komšika', u'Ncfsn-n'], u'komšikava': [u'komšika', u'Ncfsn-v'],
                 u'komšilakav': [u'komšiluk', u'Ncmsn-v'], u'komšilwkat': [u'komšiluk', u'Ncmsn-t'],
                 u'komšiləkat': [u'komšiluk', u'Ncmsn-t'], u'konacat': [u'konac', u'Ncmsn-t'],
                 u'konjat': [u'konj', u'Ncmsn-t'], u'konopljeto': [u'konoplje', u'Ncnsn-t'],
                 u'koprivete': [u'kopriva', u'Ncfpn-t'], u'korenat': [u'koren', u'Ncmsn-t'],
                 u'korenata': [u'koren' , u'Ncmsg-t'], u'kosačicata': [u'kosačica', u'Ncfsn-t'],
                 u'kosačicutu': [u'kosačica', u'Ncfsa-t'], u'kotalat': [u'kotao', u'Ncmsn-t'],
                 u'kotalwt': [u'kotao', u'Ncmsn-t'], u'kotalət': [u'kotao', u'Ncmsn-t'], u'kovutu': [u'kova', u'Ncfsa-t'],
                 u'kozata': [u'koza' , u'Ncfsn-t'], u'kozeve': [u'koza', u'Ncfpn-v'],
                 u'kočinete': [u'kočina', u'Ncfpn-t'], u'košat': [u'koš', u'Ncmsn-t'],
                 u'košuljata': [u'košulja', u'Ncfsn-t'], u'košuljkata': [u'košuljka', u'Ncfsn-t'],
                 u'košuljutu': [u'košulja', u'Ncfsa-t'], u'kožljaciti': [u'kožljak', u'Ncmpn-t'],
                 u'kravajciti': [u'kravaj', u'Ncmpn-t'], u'kravajot': [u'kravaj', u'Ncmsn-t'],
                 u'kravajčičiti': [u'kravajčič', u'Ncmpn-t'], u'kravata': [u'krava', u'Ncfsn-t'],
                 u'kravete': [u'krava', u'Ncfpn-t'], u'kravutu': [u'krava', u'Ncfsa-t'],
                 u'kreditat': [u'kredit', u'Ncmsn-t'], u'krevetat': [u'krevet', u'Ncmsn-t'],
                 u'krsat': [u'krst', u'Ncmsn-t'], u'krugat': [u'krug', u'Ncmsn-t'], u'krvat': [u'krv', u'Ncmsn-t'],
                 u'ku1ata': [u'kuća' , u'Ncfsn-t'], u'ku1utu': [u'kuća', u'Ncfsa-t'], u'ku1uvu': [u'kuća', u'Ncfsa-v'],
                 u'kujnutu': [u'kujna', u'Ncfsa-t'], u'kukuregat': [u'kukureg', u'Ncmsn-t'],
                 u'kumicata': [u'kumica', u'Ncfsn-t'], u'kupenovo': [u'kupiti', u'Agpnsny-v'],
                 u'kupinete': [u'kupina', u'Ncfpn-t'], u'kućata': [u'kuća', u'Ncfsn-t'],
                 u'kućava': [u'kuća', u'Ncfsn-v'], u'kućete': [u'kuća', u'Ncfpn-t'],
                 u'kućeve': [u'kuća', u'Ncfpn-v'], u'kućicutu': [u'kućica', u'Ncfsa-t'],
                 u'kućovo': [u'kućo', u'Ncnsn-v'], u'kućutu': [u'kuća', u'Ncfsa-t'],
                 u'kučeno': [u'kuče', u'Ncnsn-n'], u'kučutu': [u'kuča', u'Ncfsa-t'],
                 u'kuḱata': [u'kuća' , u'Ncfsn-t'], u'kuḱava': [u'kuḱa', u'Ncfsn-v'], u'kuḱutu': [u'kuḱa', u'Ncfsa-t'],
                 u'kuḱuvu': [u'kuća', u'Ncfsa-v'], u'kƏštata': [u'kuća' , u'Ncfsn-t'],
                 u'lampata': [u'lampa', u'Ncfsn-t'], u'lavorat': [u'lavor', u'Ncmsn-t'],
                 u'lebacat': [u'lebac', u'Ncmsn-t'], u'lebat': [u'hleb', u'Ncmsn-t'],
                 u'lekarat': [u'lekar', u'Ncmsn-t'], u'lekat': [u'lek', u'Ncmsn-t'],
                 u'lepenacwt': [u'lepenac', u'Npmsn-t'], u'lepenacət': [u'Lepenac', u'Npmsn-t'],
                 u'letvene': [u'letva', u'Ncfpn-n'], u'lisat': [u'list', u'Ncmsn-t'],
                 u'lisicata': [u'lisica', u'Ncfsn-t'], u'litijata': [u'litija', u'Ncfsn-t'],
                 u'livadutu': [u'livada', u'Ncfsa-t'], u'ličnutu': [u'lična', u'Agpfsay-t'],
                 u'lju2evi': [u'čovek', u'Ncmpn-v'], u'ljubata': [u'ljuba', u'Ncfsn-t'],
                 u'ljubinkata': [u'ljubinka', u'Ncfsn-t'], u'ljuditi': [u'čovek', u'Ncmpn-t'],
                 u'ljulj1ete': [u'ljuljka', u'Ncfpn-t'], u'ljuljaljćete': [u'ljuljaljka', u'Ncfpn-t'],
                 u'ljuljkutu': [u'ljuljka', u'Ncfsa-t'], u'ljuljḱete': [u'ljuljka', u'Ncfpn-t'],
                 u'ljuđevi': [u'čovek', u'Ncmpn-v'], u'ljuǵevi': [u'čovek', u'Ncmpn-v'],
                 u'lonacat': [u'lonac', u'Ncmsn-t'], u'lugat': [u'lug', u'Ncmsn-t'], u'lugjiti': [u'čovek', u'Ncmpn-t'],
                 u'lukovinjeto': [u'lukovinje', u'Ncnsn-t'], u'ma1i1iti': [u'mače', u'Ncmpn-t'],
                 u'mackava': [u'macka', u'Ncfsn-v'], u'macutu': [u'maca', u'Ncfsa-t'],
                 u'magareto': [u'magare', u'Ncnsn-t'], u'magatistrurutu': [u'magatistura', u'Ncfsa-t'],
                 u'malijat': [u'mali', u'Agpmsny-t'], u'maliti': [u'mali', u'Agpmpn-y'],
                 u'maloto': [u'mali', u'Agpnsny-t'], u'malovo': [u'mali', u'Agpnsny-v'],
                 u'masnoto': [u'mastan', u'Agpnsny-t'], u'materjata': [u'materija' , u'Ncfsn-t'],
                 u'materjete': [u'materja', u'Ncfpn-t'], u'maznono': [u'mazno', u'Agpnsny-n'],
                 u'mač6ete': [u'mačka', u'Ncfpn-t'], u'mačeto': [u'mače', u'Ncnsn-t'], u'mačevo': [u'mače', u'Ncnsn-v'],
                 u'mačkata': [u'mačka', u'Ncfsn-t'], u'mačkete': [u'mačka', u'Ncfpn-t'],
                 u'mačkutu': [u'mačka', u'Ncfsa-t'], u'mačḱete': [u'mačka', u'Ncfpn-t'],
                 u'mašinuvu': [u'mašina', u'Ncfsa-v'], u'maḱiḱiti': [u'mače', u'Ncmpn-t'],
                 u'medat': [u'med', u'Ncmsn-t'], u'mengrantivi': [u'mengrant', u'Ncmpn-v'],
                 u'mesoto': [u'meso', u'Ncnsn-t'], u'mezrejutu': [u'mezreja', u'Ncfsa-t'],
                 u'mečkata': [u'mečka', u'Ncfsn-t'], u'mešenoto': [u'mešen', u'Agpnsny-t'],
                 u'miderat': [u'mider', u'Ncmsn-t'], u'mirisat': [u'miris', u'Ncmsn-t'],
                 u'mladijat': [u'mlad', u'Agpmsnn-t'], u'mladiti': [u'mlad', u'Ncmpn-t'],
                 u'mlekoto': [u'mlekoto', u'Ncnsn-t'], u'mlekovo': [u'mleko', u'Ncnsn-v'],
                 u'mlinat': [u'mlin', u'Ncmsn-t'], u'moav': [u'moj', u'Ps1msn-v'], u'moete': [u'moj', u'Ncfpn-t'],
                 u'moeto': [u'moj', u'Ps1nsn-t'], u'moevo': [u'moj', u'Ps1nsn-v'], u'moiti': [u'moj', u'Ps1mpn-t'],
                 u'mojana': [u'moj', u'Ps1fsn-n'], u'mojat': [u'moj', u'Ps1msn-t'], u'mojata': [u'moj', u'Ps1fsn-t'],
                 u'mojav': [u'moj', u'Ps1msn-v'], u'mojava': [u'moj', u'Ps1fsn-v'], u'mojete': [u'moj', u'Ps1fpn-t'],
                 u'mojeto': [u'moj', u'Ps1nsn-t'], u'mojeve': [u'moj', u'Ps1fsn-v'], u'mojevo': [u'moj', u'Ps1nsn-v'],
                 u'mojiti': [u'moj', u'Ps1mpn-t'], u'mojivi': [u'moj', u'Ps1mpn-v'], u'mojutu': [u'moj', u'Ps1fsa-t'],
                 u'momakat': [u'momak', u'Ncmsn-t'], u'momciti': [u'momak', u'Ncmpn-t'],
                 u'moruzutu': [u'moruza', u'Ncfsa-t'], u'mostat': [u'most', u'Ncmsn-t'],
                 u'motkutu': [u'motka', u'Ncfsa-t'], u'mozakat': [u'mozak', u'Ncmsn-t'],
                 u'mozakata': [u'mozak', u'Ncmsayt'], u'mumuruzinutu': [u'mumuruzina', u'Ncfsa-t'],
                 u'mušiceve': [u'mušica', u'Ncfpn-v'], u'muškaracat': [u'muškarac', u'Ncmsn-t'],
                 u'mušćiti': [u'muški', u'Agpmsny-t'], u'mužat': [u'muž', u'Ncmsn-t'],
                 u'mužatoga': [u'muž', u'Ncmsayt'], u'mužava': [u'muž', u'Ncmsayv'],
                 u'mužjete': [u'muž', u'Ncfpn-t'], u'mužjetinata': [u'mužjetina', u'Ncfsn-t'],
                 u'naprezutu': [u'napreza', u'Ncfsa-t'], u'našata': [u'naš', u'Ps3nsn-t'],
                 u'našava': [u'naš', u'Ps3nsn-t'], u'našeto': [u'naš', u'Ps3nsn-t'], u'naševo': [u'naš', u'Ps3nsn-t'],
                 u'našiat': [u'naš', u'Ps3nsn-t'], u'našiti': [u'naš', u'Ps3nsn-t'], u'našutu': [u'naš', u'Ps3nsn-t'],
                 u'neboto': [u'nebo', u'Ncnsn-t'], u'nekakovo': [u'nekakav', u'Agpnsny-v'],
                 u'nekcijete': [u'nekcija', u'Ncfpn-t'], u'nekolkoto': [u'nekolko', u'Ncnsn-t'],
                 u'nemačkete': [u'nemačka', u'Ncfpn-t'], u'nemciti': [u'Nemac', u'Npmpn-t'],
                 u'nepovijenoto': [u'nepovijen', u'Agpnsny-t'], u'neḱivi': [u'neḱi', u'Ncmpn-v'],
                 u'nišata': [u'niša' , u'Ncfsn-t'], u'njegovoto': [u'njegov', u'Ps3nsn-t'],
                 u'njinata': [u'njihov', u'Ps3nsn-t'], u'njinoto': [u'njihov', u'Ps3nsn-t'],
                 u'njivete': [u'njiva', u'Ncfpn-t'], u'njivutu': [u'njiva', u'Ncfsa-t'],
                 u'njojnjata': [u'njenojnja', u'Ps3fsn-t'], u'njojnoto': [u'moj', u'Ps3nsn-t'], u'no2eve': [u'noga', u'Ncfpn-v'], u'nogata': [u'noga' , u'Ncfsn-t'], u'nosat': [u'nos', u'Ncmsn-t'], u'nosav': [u'nos', u'Ncmsn-v'], u'novovo': [u'nov', u'Agpnsny-v'], u'novčeničeto': [u'novčeniče', u'Ncnsn-t'], u'noǵeve': [u'noga', u'Ncfpn-v'], u'noǵićkana': [u'noǵićka', u'Ncfsn-n'], u'obete': [u'oba', u'Mlcfpa-t'], u'obeve': [u'obe', u'Mlofsn-v'], u'oblakat': [u'oblak', u'Ncmsn-t'], u'obojicata': [u'obojica' , u'Mlomsn-t'], u'odeloto': [u'odelo', u'Ncnsn-t'], u'oganjat': [u'oganj', u'Ncmsn-t'], u'oganjatat': [u'oganjat', u'Ncmsn-t'], u'ognjišteto': [u'ognjište', u'Ncnsn-t'], u'okoto': [u'oko', u'Ncnsn-t'], u'okrugloto': [u'okrugao', u'Agpnsny-t'], u'olalijete': [u'olalija', u'Ncfpn-t'], u'om1ete': [u'omča', u'Ncfpn-t'], u'omladijat': [u'omladij', u'Ncmsn-t'], u'omḱete': [u'omča', u'Ncfpn-t'], u'opančat': [u'opanč', u'Ncmsn-t'], u'opančićiti': [u'opančići', u'Ncmpn-t'], u'opwnciti': [u'opanak', u'Ncmpn-t'], u'opštinutu': [u'opština', u'Ncfsa-t'], u'opənciti': [u'opənak', u'Ncmpn-t'], u'oteklata': [u'otekla' , u'Agpfsny-t'], u'otroviti': [u'otrov', u'Ncmpn-t'], u'ovcete': [u'ovca', u'Ncfpn-t'], u'ovceve': [u'ovca', u'Ncfpn-v'], u'ovcincete': [u'ovcinca', u'Agpfpny-t'], u'ovcutu': [u'ovca', u'Ncfsa-t'], u'ovijav': [u'ovaj', u'Ps3nsn-t'], u'ovčicete': [u'ovčica', u'Ncfpn-t'], u'ovčinete': [u'ovčina', u'Ncfpn-t'], u'padinata': [u'padina', u'Ncfsn-t'], u'padinutu': [u'padina', u'Ncfsa-t'], u'papričkata': [u'paprička', u'Ncfsn-t'], u'papričkutu': [u'paprička', u'Ncfsa-t'], u'paradajsat': [u'paradajs', u'Ncmsn-t'], u'parana': [u'para', u'Ncfsn-n'], u'parata': [u'para' , u'Ncfsn-t'], u'paraunučeto': [u'paraunuče', u'Ncnsn-t'], u'parete': [u'para', u'Ncfpn-t'], u'paricata': [u'parica', u'Ncfsn-t'], u'paricete': [u'parica', u'Ncfpn-t'], u'paričkata': [u'parička', u'Ncfsn-t'], u'parutu': [u'para', u'Ncfsa-t'], u'pasuljat': [u'pasulj', u'Ncmsn-t'], u'pelenete': [u'pelena', u'Ncfpn-t'], u'penzijiceve': [u'penzijica', u'Ncfpn-v'], u'penzijicutu': [u'penzijica', u'Ncfsa-t'], u'penzijutu': [u'penzija', u'Ncfsa-t'], u'penzićutu': [u'penzića', u'Ncfsa-t'], u'pepelat': [u'pepel', u'Ncmsn-t'], u'peraškata': [u'peraška', u'Ncfsn-t'], u'peraškutu': [u'peraška', u'Ncfsa-t'], u'perašćete': [u'perašća', u'Ncfpn-t'], u'pesmicutu': [u'pesmica', u'Ncfsa-t'], u'pesmutu': [u'pesma', u'Ncfsa-t'], u'petljete': [u'petlja', u'Ncfpn-t'], u'pečiljkete': [u'pečiljka', u'Ncfpn-t'], u'pisarat': [u'pisar', u'Ncmsn-t'], u'piteve': [u'pita', u'Ncfpn-v'], u'planinutu': [u'planina', u'Ncfsa-t'], u'plastenikat': [u'plastenik', u'Ncmsn-t'], u'plinčićivi': [u'plinče', u'Ncmpn-v'], u'plotat': [u'plot', u'Ncmsn-t'], u'podrumat': [u'podrum', u'Ncmsn-t'], u'podubičkata': [u'podubička', u'Ncfsn-t'], u'pogačkata': [u'pogačka', u'Ncfsn-t'], u'pogačutu': [u'pogača', u'Ncfsa-t'], u'pojatutu': [u'pojata', u'Ncfsa-t'], u'pokladete': [u'poklada', u'Ncfpn-t'], u'poklopenovo': [u'poklopiti', u'Appnsny-v'], u'pomijete': [u'pomija', u'Ncfpn-t'], u'ponedelnikat': [u'ponedelnik', u'Ncmsn-t'], u'ponjavete': [u'ponjava', u'Ncfpn-t'], u'popadijava': [u'popadija', u'Ncfsn-v'], u'popat': [u'pop', u'Ncmsn-t'], u'posediti': [u'posed', u'Ncmpn-t'], u'potokat': [u'potok', u'Ncmsn-t'], u'povatutu': [u'povata', u'Ncfsa-t'], u'povijenoto': [u'povijen', u'Agpnsny-t'], u'povolenšćiti': [u'povolen', u'Ncmpn-t'], u'pragat': [u'prag', u'Ncmsn-t'], u'prazniciti': [u'praznik', u'Ncmpn-t'], u'prašakat': [u'prašak', u'Ncmsn-t'], u'preobraženjeto': [u'preobraženje', u'Npnsn-t'], u'prinovljenijat': [u'prinovljenij', u'Ncmsn-t'], u'pritisakat': [u'pritisak', u'Ncmsn-t'], u'privat': [u'priv', u'Ncmsn-t'], u'pričanjeto': [u'pričanje', u'Ncnsn-t'], u'pričićiti': [u'pričić', u'Ncmpn-t'], u'prodavnicunu': [u'prodavnica', u'Ncfsa-n'], u'prodavnicutu': [u'prodavnica', u'Ncfsa-t'], u'prokletijete': [u'prokletija', u'Ncfpn-t'], u'prstiti': [u'prst', u'Ncmpn-t'], u'prtenicete': [u'prtenica', u'Ncfpn-t'], u'prutat': [u'prut', u'Ncmsn-t'], u'prutičiti': [u'prutić', u'Ncmpn-t'], u'prvutu': [u'prvi', u'Mlofsa-t'], u'przdelat': [u'przdel', u'Ncmsn-t'], u'punat': [u'pun', u'Agpmsny-t'], u'pustinjata': [u'pustinja' , u'Ncfsn-t'], u'putat': [u'put', u'Ncmsn-t'], u'putav': [u'put', u'Ncmsn-v'], u'putničkoto': [u'putnički', u'Agpnsny-t'], u'pušnicutu': [u'pušnica', u'Ncfsa-t'], u'radojčutu': [u'radojča', u'Ncnsayt'], u'rakijutu': [u'rakija', u'Ncfsa-t'], u'ratat': [u'rat', u'Ncmsn-t'], u'razmiricava': [u'razmirica', u'Ncfsn-v'], u'rekata': [u'reka', u'Ncfsn-t'], u'rekunu': [u'reka', u'Ncfsa-n'], u'rekutu': [u'reka', u'Ncfsa-t'], u'rezat': [u'rez', u'Ncmsn-t'], u'ribicata': [u'ribica' , u'Ncfsn-t'], u'rimskete': [u'rimska', u'Agpfpny-t'], u'rmat': [u'rm', u'Ncmsn-t'], u'robata': [u'roba', u'Ncfsn-t'], u'roditeljiti': [u'roditelj', u'Ncmpn-t'], u'rodivi': [u'rod', u'Ncmpn-v'], u'rogat': [u'rog', u'Ncmsn-t'], u'rovinete': [u'rovina', u'Ncfpn-t'], u'rtat': [u'rt', u'Ncmsn-t'], u'rudnikat': [u'rudnik', u'Ncmsn-t'], u'rukata': [u'ruka' , u'Ncfsn-t'], u'rukete': [u'ruka', u'Ncfpn-t'], u'rukutu': [u'ruka', u'Ncfsa-t'], u'ruputu': [u'rupa', u'Ncfsa-t'], u'rusiti': [u'Rus', u'Npmpn-t'], u'ručiḱkene': [u'ručiḱka', u'Ncfpn-n'], u'saloto': [u'salo', u'Ncnsn-t'], u'salovo': [u'selo', u'Ncnsn-v'], u'sandalete': [u'sandala', u'Ncfpn-t'], u'sedenjkete': [u'sedenjka', u'Ncfpn-t'], u'sedinjkete': [u'sedenjka', u'Ncfpn-t'], u'selono': [u'selo', u'Ncnsn-n'], u'seloto': [u'selo', u'Ncnsn-t'], u'selovo': [u'selo', u'Ncnsn-v'], u'selskutu': [u'selska', u'Ncfsa-t'], u'semaforivi': [u'semafor', u'Ncmpn-v'], u'sestrata': [u'sestra' , u'Ncfsn-t'], u'sećirutu': [u'sećira', u'Ncfsa-t'], u'sinat': [u'sin', u'Ncmsn-t'], u'sinatoga': [u'sin', u'Ncmsayt'], u'sinav': [u'sin', u'Ncmsn-v'], u'sirinjeto': [u'sirinje', u'Ncnsn-t'], u'sirinjiceto': [u'sirinjice', u'Ncnsn-t'], u'sirutkutu': [u'sirutka', u'Ncfsa-t'], u'sičkoto': [u'sičko', u'Ncnsn-t'], u'skijanjeto': [u'skijanje', u'Ncnsn-t'], u'sklopkata': [u'sklopka', u'Ncfsn-t'], u'sklopkutu': [u'sklopka', u'Ncfsa-t'], u'slamata': [u'slama' , u'Ncfsn-t'], u'slamutu': [u'slama', u'Ncfsa-t'], u'slavutu': [u'slava', u'Ncfsa-t'], u'slikata': [u'slika', u'Ncfsn-t'], u'slikava': [u'slika', u'Ncfsn-v'], u'slivete': [u'sliva', u'Ncfpn-t'], u'sličkete': [u'slička', u'Ncfpn-t'], u'sljivete': [u'šljiva', u'Ncfpn-t'], u'službete': [u'služba', u'Ncfpn-t'], u'snajkata': [u'snajka', u'Ncfsn-t'], u'snata': [u'snaha' , u'Ncfsn-t'], u'snautu': [u'snaha', u'Ncfsa-t'], u'snauvu': [u'snaja', u'Ncfsa-v'], u'snegat': [u'sneg', u'Ncmsn-t'], u'snegav': [u'sneg', u'Ncmsn-v'], u'snimakat': [u'snimak', u'Ncmsn-t'], u'snopoviti': [u'snop', u'Ncmpn-t'], u'sobutu': [u'soba', u'Ncfsa-t'], u'socijalutu': [u'socijala', u'Ncfsa-t'], u'sodata': [u'soda', u'Ncfsn-t'], u'sprjmutu': [u'sprjma', u'Ncfsa-t'], u'srednjiti': [u'srednji', u'Ncmpn-t'], u'srednjoto': [u'srednji', u'Agpnsny-t'], u'sstrujata': [u'struja' , u'Ncfsn-t'], u'staracat': [u'starac', u'Ncmsn-t'], u'starata': [u'star', u'Agpfsny-t'], u'starcat': [u'starac', u'Ncmsn-t'], u'starcatoga': [u'starac', u'Ncmsayt'], u'starcav': [u'starac', u'Ncmsn-v'], u'starcavoga': [u'starac', u'Ncmsayv'], u'starciti': [u'starac', u'Ncmpn-t'], u'starejutu': [u'stareja', u'Ncfsa-t'], u'starinskiti': [u'starinski', u'Agpmsny-t'], u'stariti': [u'star', u'Ncmpn-t'], u'stativat': [u'stativ', u'Ncmsn-t'], u'stepeniceve': [u'stepenica', u'Ncfpn-v'], u'stipsata': [u'stipsa' , u'Ncfsn-t'], u'stipsutu': [u'stipsa', u'Ncfsa-t'], u'stogovene': [u'stog', u'Ncmpa-n'], u'stokata': [u'stoka', u'Ncfsn-t'], u'stokutu': [u'stoka', u'Ncfsa-t'], u'stolicutu': [u'stolica', u'Ncfsa-t'], u'stoparceto': [u'stoparce', u'Ncnsn-t'], u'strahat': [u'strah', u'Ncmsn-t'], u'strejutu': [u'streja', u'Ncfsa-t'], u'strinata': [u'strina', u'Ncfsn-t'], u'strujata': [u'struja' , u'Ncfsn-t'], u'strujutu': [u'struja', u'Ncfsa-t'], u'subotutu': [u'subota', u'Ncfsa-t'], u'sudive': [u'sud', u'Ncmpn-v'], u'suknata': [u'sukna', u'Ncnpn-t'], u'suknoto': [u'sukno', u'Ncnsn-t'], u'sunceto': [u'sunce', u'Ncnsn-t'], u'suprašicutu': [u'suprašica', u'Ncfsa-t'], u'svadbeve': [u'svadba', u'Ncfpn-v'], u'svadbutu': [u'svadba', u'Ncfsa-t'], u'svekarat': [u'svekar', u'Ncmsn-t'], u'svekrvata': [u'svekrva', u'Ncfsn-t'], u'svekrvava': [u'svekrva', u'Ncfsn-v'], u'svekrvutu': [u'svekrva', u'Ncfsa-t'], u'svetat': [u'svet', u'Ncmsn-t'], u'svetlata': [u'svetlo' , u'Ncnpn-t'], u'svečata': [u'sveća' , u'Ncfsn-t'], u'svinjata': [u'svinja' , u'Ncfsn-t'], u'svinjutu': [u'svinja', u'Ncfsa-t'], u'taksistivi': [u'taksist', u'Ncmpn-v'], u'tamniti': [u'taman', u'Agpmsny-t'], u'tanjirčevo': [u'tanjirče', u'Ncnsn-v'], u'taštata': [u'tašta', u'Ncfsn-t'], u'taštutu': [u'tašta', u'Ncfsa-t'], u'teglete': [u'tegla', u'Ncfpn-t'], u'telefonat': [u'telefon', u'Ncmsn-t'], u'telefoniti': [u'telefon', u'Ncmpn-t'], u'televizorat': [u'televizor', u'Ncmsn-t'], u'telfonat': [u'telfon', u'Ncmsn-t'], u'terasutu': [u'terasa', u'Ncfsa-t'], u'testoto': [u'testo', u'Ncnsn-t'], u'tetkata': [u'tetka', u'Ncfsn-t'], u'tevelevizorav': [u'tevelevizor', u'Ncmsn-v'], u'tevsićeto': [u'tevsiće', u'Ncnsn-t'], u'tikvete': [u'tikva', u'Ncfpn-t'], u'tikvicete': [u'tikvica', u'Ncfpn-t'], u'topoviti': [u'top', u'Ncmpn-t'], u'torbeve': [u'torba', u'Ncfpn-v'], u'torbičkata': [u'torbička', u'Ncfsn-t'], u'torbutu': [u'torba', u'Ncfsa-t'], u'trakoviti': [u'trak', u'Ncmpn-t'], u'traktorav': [u'traktor', u'Ncmsn-v'], u'tramizat': [u'tramiz', u'Ncmsn-t'], u'trapat': [u'trap', u'Ncmsn-t'], u'travaljat': [u'travalj', u'Ncmsn-t'], u'travata': [u'trava' , u'Ncfsn-t'], u'travete': [u'trava', u'Ncfpn-t'], u'travicata': [u'travica', u'Ncfsn-t'], u'traviceve': [u'trava', u'Ncfpn-v'], u'travicutu': [u'travica', u'Ncfsa-t'], u'travutu': [u'trava', u'Ncfsa-t'], u'trećoto': [u'trećo', u'Mlonsn-t'], u'trljakat': [u'trljak', u'Ncmsn-t'], u'trojicata': [u'trojica', u'Ncmsn-t'], u'troškoviti': [u'trošak', u'Ncmpn-t'], u'tujete': [u'tuja', u'Ncfpn-t'], u'tunelat': [u'tunel', u'Ncmsn-t'], u'turciti': [u'Turčin', u'Ncmpn-t'], u'turenoto': [u'tureno', u'Agpnsny-t'], u'tuđutu': [u'tuđa', u'Agpfsay-t'], u'tvoata': [u'tvoj' , u'Ps2fsn-t'], u'tvojana': [u'tvoj', u'Ps2fsn-n'], u'tvojevo': [u'tvoj', u'Ps2nsn-v'], u'tvojutu': [u'tvoja', u'Ps2fsa-t'], u'ubavoto': [u'ubav', u'Agpnsny-t'], u'uglenčičiti': [u'uglenčić', u'Ncmpn-t'], u'unuciti': [u'unuk', u'Ncmpn-t'], u'unucivi': [u'unuk', u'Ncmpn-v'], u'unukat': [u'unuk', u'Ncmsn-t'], u'unukata': [u'unuka', u'Ncfsn-t'], u'unukutu': [u'unuka', u'Ncfsa-t'], u'unučeto': [u'unuče', u'Ncnsn-t'], u'uranat': [u'uran', u'Ncmsn-t'], u'utrono': [u'jutro', u'Ncnsn-n'], u'uvečevo': [u'uveče', u'Ncnsn-v'], u'učiteljanoga': [u'učitelj', u'Ncmsayn'], u'učiteljite': [u'učitelj', u'Ncmpn-t'], u'učiteljiti': [u'učitelj', u'Ncmpn-t'], u'vadutu': [u'vada', u'Ncfsa-t'], u'vagava': [u'vaga', u'Ncfsn-v'], u'vagutu': [u'vaga', u'Ncfsa-t'], u'vasuljakat': [u'vasuljak', u'Ncmsn-t'], u'vašariti': [u'vašar', u'Ncmpn-t'], u'vašarwt': [u'vašar', u'Ncmsn-t'], u'vašarət': [u'vašar', u'Ncmsn-t'], u'vašata': [u'vaša', u'Ncfsn-t'], u'vašćete': [u'vašća', u'Ncfpn-t'], u'vedroto': [u'vedro', u'Ncnsn-t'], u'vejnikat': [u'vejnik', u'Ncmsn-t'], u'velikete': [u'velik', u'Agpfpny-t'], u'venacwt': [u'venacwt', u'Ncmsn-t'], u'venacət': [u'venacwt', u'Ncmsn-t'], u'venciti': [u'venac', u'Ncmpn-t'], u'venwcat': [u'venac', u'Ncmsn-t'], u'venčakat': [u'venčak', u'Ncmsn-t'], u'venčekat': [u'venček', u'Ncmsn-t'], u'venəcat': [u'venəc', u'Ncmsn-t'], u'veri2ete': [u'veriga', u'Ncfpn-t'], u'veridbutu': [u'veridba', u'Ncfsa-t'], u'veriǵete': [u'veriga', u'Ncfpn-t'], u'videloto': [u'videlo', u'Ncnsn-t'], u'vimeto': [u'vime', u'Ncnsn-t'], u'vimoto': [u'vimo', u'Ncnsn-t'], u'virat': [u'vir', u'Ncmsn-t'], u'višnjete': [u'višnja', u'Ncfpn-t'], u'vlaškata': [u'vlaški', u'Agpfsny-t'], u'vo1kete': [u'voćka', u'Ncfpn-t'], u'vodata': [u'voda', u'Ncfsn-t'], u'vodenicutu': [u'vodenica', u'Ncfsa-t'], u'vodicata': [u'vodica', u'Ncfsn-t'], u'vodicutu': [u'vodica', u'Ncfsa-t'], u'vodičkoto': [u'vodičko', u'Ncnsn-t'], u'vodutu': [u'voda', u'Ncfsa-t'], u'voduvu': [u'voda', u'Ncfsa-v'], u'vojniciti': [u'vojnik', u'Ncmpn-t'], u'volat': [u'vo', u'Ncmsn-t'], u'voloviti': [u'vol', u'Ncmpn-t'], u'volovoloviti': [u'vo', u'Ncmpn-t'], u'voḱkete': [u'voḱka', u'Ncfpn-t'], u'vragat': [u'vrag', u'Ncmsn-t'], u'vratana': [u'vrata', u'Ncfsn-n'], u'vratata': [u'vrata' , u'Ncfsn-t'], u'vratava': [u'vrata', u'Ncfsn-v'], u'vračkata': [u'vračka', u'Ncfsn-t'], u'vražalacat': [u'vražalac', u'Ncmsn-t'], u'vrbakat': [u'vrbak', u'Ncmsn-t'], u'vremevo': [u'vreme', u'Ncnsn-v'], u'vretenoto': [u'vreteno', u'Ncnsn-t'], u'vrezutu': [u'vreza', u'Ncfsa-t'], u'vrećutu': [u'vreća', u'Ncfsa-t'], u'vrtolomata': [u'vrtoloma' , u'Ncmsn-t'], u'vrućinutu': [u'vrućina', u'Ncfsa-t'], u'vršnjakat': [u'vršnjak', u'Ncmsn-t'], u'vršnjekat': [u'vršnjek', u'Ncmsn-t'], u'vukovete': [u'vuk', u'Ncmpa-t'], u'vurnjutu': [u'vurnja', u'Ncfsa-t'], u'vutnjutu': [u'vutnja', u'Ncfsa-t'], u'zadnjata': [u'zadnji', u'Agpfsny-t'], u'zadnjete': [u'zadnji', u'Agpfpny-t'], u'zamrzivačat': [u'zamrzivač', u'Ncmsn-t'], u'zapisiti': [u'zapis', u'Ncmpn-t'], u'zatvoreniciti': [u'zatvorenik', u'Ncmpn-t'], u'zavetinata': [u'zavetina', u'Ncfsn-t'], u'zdravjeto': [u'zdravje', u'Ncnsn-t'], u'zejtinat': [u'zejtin', u'Ncmsn-t'], u'zemljata': [u'zemlja', u'Ncfsn-t'], u'zemljutu': [u'zemlja', u'Ncfsa-t'], u'zetat': [u'zet', u'Ncmsn-t'], u'zgradata': [u'zgrada', u'Ncfsn-t'], u'zmejat': [u'zmej', u'Ncmsn-t'], u'zmijata': [u'zmija' , u'Ncfsn-t'], u'zmijeve': [u'zmija', u'Ncfpn-v'], u'zmijurineve': [u'zmijurina', u'Ncfpn-v'], u'zmijutu': [u'zmija', u'Ncfsa-t'], u'zorata': [u'zora' , u'Ncfsn-t'], u'zubiti': [u'zub', u'Ncmpn-t'], u'zvonata': [u'zvona', u'Ncfsn-t'], u'ćebeto': [u'ćebe', u'Ncnsn-t'], u'ćerkata': [u'ćerka', u'Ncfsn-t'], u'ćerkutu': [u'ćerka', u'Ncfsa-t'], u'ćerćete': [u'ćerka', u'Ncfpn-t'], u'ćesutu': [u'ćesa', u'Ncfsa-t'], u'ćoravata': [u'ćorav', u'Agpfsny-t'], u'čajat': [u'čaj', u'Ncmsn-t'], u'čarapete': [u'čarapa', u'Ncfpn-t'], u'čaškete': [u'čaška', u'Ncfpn-t'], u'čedinoto': [u'čedin', u'Appnsny-t'], u'četvrtoto': [u'četvrto', u'Mlonsn-t'], u'češmutu': [u'češma', u'Ncfsa-t'], u'češmuvu': [u'česma', u'Ncfsa-v'], u'čitaonicutu': [u'čitaonica', u'Ncfsa-t'], u'čičeve': [u'čiča', u'Ncmpn-v'], u'čičutu': [u'čiča', u'Ncfsa-t'], u'čovekat': [u'čovek', u'Ncmsn-t'], u'čovekata': [u'čovek', u'Ncmsayt'], u'čovekatoga': [u'čovek', u'Ncmsayt'], u'čovekwt': [u'čovek', u'Ncmsn-t'], u'čovekət': [u'čovek', u'Ncmsn-t'], u'čuvaškutu': [u'čuvaška', u'Ncfsa-t'], u'čvatata': [u'čvata', u'Ncfsn-t'], u'đaciti': [u'đak', u'Ncmpn-t'], u'đemperiti': [u'đemper', u'Ncmpn-t'], u'đuvečat': [u'đuveč', u'Ncmsn-t'], u'šakalivi': [u'šakal', u'Ncmpn-v'], u'šakutu': [u'šaka', u'Ncfsa-t'], u'šargarepata': [u'šargarepa', u'Ncfsn-t'], u'šerputu': [u'šerpa', u'Ncfsa-t'], u'šerpuvu': [u'šerpa', u'Ncfsa-v'], u'šećerat': [u'šećer', u'Ncmsn-t'], u'šibicutu': [u'šibica', u'Ncfsa-t'], u'školava': [u'škola', u'Ncfsn-v'], u'školutu': [u'škola', u'Ncfsa-t'], u'šljivete': [u'šljiva', u'Ncfpn-t'], u'šoljicete': [u'šoljica', u'Ncfpn-t'], u'šporetiti': [u'šporeti', u'Ncmpn-t'], u'štalutu': [u'štala', u'Ncfsa-t'], u'šumutu': [u'šuma', u'Ncfsa-t'], u'šuputu': [u'šupa', u'Ncfsa-t'], u'šušćete': [u'šušća', u'Ncfpn-t'], u'žarat': [u'žar', u'Ncmsn-t'], u'ždrloto': [u'ždrlo', u'Ncnsn-t'], u'ženata': [u'žena' , u'Ncfsn-t'], u'ženete': [u'žena', u'Ncfpn-t'], u'ženeve': [u'žena', u'Ncfpn-v'], u'ženicana': [u'ženica', u'Ncfsn-n'], u'ženicata': [u'ženica', u'Ncfsn-t'], u'ženicutu': [u'ženica', u'Ncfsa-t'], u'ženskite': [u'ženski', u'Agpfpny-t'], u'ženskoto': [u'ženski', u'Agpnsny-t'], u'ženutu': [u'žena', u'Ncfsa-t'], u'ženšćinata': [u'ženšćina', u'Ncfsn-t'], u'žetvutu': [u'žetva', u'Ncfsa-t'], u'žitencevo': [u'žitence', u'Ncnsn-v'], u'žitoto': [u'žito', u'Ncnsn-t'], u'ǵubreto': [u'ǵubre', u'Ncnsn-t'], u'ḱerkata': [u'ḱerka', u'Ncfsn-t'], u'ḱerkutu': [u'ḱerka', u'Ncfsa-t']}

outfile = codecs.open('00_search_atricles_out.txt','w','utf8')

# Functions
def file_to_str(infile):
    non_verbal_list = [u'((?))', u'.', u'#', u'•', u'••', u'•••']
    filestring = str()
    for line in infile:
        line = line.strip()
        if len(line.split('\t')) < 3:
            if line.split('\t')[0] in non_verbal_list:
                line = line
                # pass
            else:
                line = ".\tZ\t.\n\t\t"  # adding a fullstop as an utterance boundary, for the visual output

        filestring += " " + line
    return filestring


# create a string out of words in a list of tokens
def token_list_to_str_words(token_list):
    str_words = str()
    for item in token_list:
        word = item.split('\t')[0]
        str_words += word + ' '

    return str_words


def token_list_to_str_lemmas(token_list):
    str_lemmas = str()
    for item in token_list:
        lemma = item.split('\t')[2]
        str_lemmas += lemma + ' '

    return str_lemmas


def token_list_to_word_list(token_list):
    word_list = []
    for item in token_list:
        word = item.split('\t')[0]
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

def file_to_list(infile):

    non_verbal_list = [u'((?))', u'.', u'#', u'•', u'••', u'•••', ' ']
    file_str = str()
    for line in infile:
        if '\t' in line:
            line = line.strip()

        if len(line.split('\t')) == 3:
            line = line+' '
            file_str += (line)
        elif line.split('\t')[0] in non_verbal_list:
            line = line.strip()
            file_str += (line)
            # pass
        else:
            # print(line.split())
            # print(line.encode('utf8'))
            pass
    filelist = file_str.split(" ")
    filelist = [i for i in filelist if i]

    return filelist
# -------------------------------------

# main
art_list = []

for transcript in FILES:

    filename = FOLDERPATH + transcript

    with codecs.open(filename, 'r', 'UTF-8') as input_file:

        # putting file into a list of lines
        filelist = file_to_list(input_file)

        if len(filelist) < 6:
            pass

        else:

            for i in range(0, len(filelist) - 1):

                # creating tokens: each token has the structure "word\tpos\tlemma", \t tab is a separator
                token = filelist[i]


                i += 1

                word = token.split('\t')[0]
                pos = token.split('\t')[1]
                lemma = token.split('\t')[2]

                if word.lower() in ARTICLES_DICT:
                    art_list.append(transcript)

                    # resultspre = filelist[(i - results_before): i - 1]
                    # resultspre_text = token_list_to_str_words(resultspre)
                    # resultspost = filelist[i + 1: (i + results_after)]
                    # resultspost_text = token_list_to_str_words(resultspost)
                    # outfile.write(transcript + '\t' + resultspre_text + '\t' + word + '\t' + resultspost_text + '\n')

art_per_spk = Counter(art_list)

for item in art_per_spk:
    outfile.write(item + '\t' + str(art_per_spk[item]) + '\n')

outfile.close()