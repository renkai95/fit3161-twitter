import nlp_analysis_v1
import time
import datetime as dt


def test_readLexicon():

    try:
        lexiconArray = nlp_analysis_v1.readLexicon('testlexicon.txt')
        if lexiconArray != [['abbot', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], ['abbreviate', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['abbreviation', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['purify', '0', '0', '0', '1', '0', '1', '0', '0', '1']]:
            raise()
        print('readLexicon() works as intended.')
    except:
        print('Error occurred in testing readLexicon().')
    return


def test_createdictionary():

    try:
        lexiconArray = nlp_analysis_v1.readLexicon('testlexicon.txt')
        hashtablelex = nlp_analysis_v1.createdictionary(lexiconArray)

        if hashtablelex != {'abbot': 0, 'abbreviate': 1, 'abbreviation': 2, 'purify': 3}:
            raise()
        print('createdictionary() works as intended.')
    except:
        print('Error occurred in testing createdictionary().')
    return


def test_matchtohashtable():
    try:

        lexiconArray = nlp_analysis_v1.readLexicon('testlexicon.txt')
        hashtablelex = nlp_analysis_v1.createdictionary(lexiconArray)
        if nlp_analysis_v1.matchtohashtable('abbot', lexiconArray, hashtablelex) != ['abbot', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0']:
            raise()
        if nlp_analysis_v1.matchtohashtable('abbreviate', lexiconArray, hashtablelex) != ['abbreviate', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']:
            raise()
        if nlp_analysis_v1.matchtohashtable('thiswordisnotinthelexicon', lexiconArray, hashtablelex) != None:
            raise()
        print('matchtohashtable() works as intended.')
    except:
        print('Error occurred in testing matchtohashtable().')
    return


def test_wordsentimentcalculation():
    try:

        lexiconArray = nlp_analysis_v1.readLexicon('testlexicon.txt')
        hashtablelex = nlp_analysis_v1.createdictionary(lexiconArray)
        if nlp_analysis_v1.wordsentimentcalculation(['a','abbot','abbreviate','abbot','ok', 'purify'], lexiconArray, hashtablelex) != [0, 0, 0, 1, 0, 1, 0, 0, 3, 0]:
            raise()
        print('wordsentimentcalculation() works as intended.')
    except:
        print('Error occurred in testing wordsentimentcalculation().')
    return



def test_updatescores():
    try:

        if nlp_analysis_v1.updatescores([1, 0, 23, 0, 0, 0, 0, 0, 2, 0], ['abbot', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0']) != [1, 0, 23, 0, 0, 0, 0, 0, 3, 0]:
            raise()
        print('updatescores() works as intended.')
    except:
        print('Error occurred in testing updatescores().')
    return




def test_preprocesstweettextforanalysis():
    try:
        if nlp_analysis_v1.preprocesstweettextforanalysis('@testt, Tweet: Hurricane Irma looks like fun <3 XD ') !=  ['testt', 'tweet', 'hurricane', 'irma', 'looks', 'like', 'fun','xd']:
            raise()
        print('preprocesstweettextforanalysis() works as intended.')
    except:
        print('Error occurred in testing preprocesstweettextforanalysis().')
    return


def test_processandwritetofile():
    try:

        lexiconArray = nlp_analysis_v1.readLexicon('testlexicon.txt')
        hashtablelex = nlp_analysis_v1.createdictionary(lexiconArray)
        readerfulltext = open('testtweets.csv')
        testwritefile = 'testwrittenfile.txt'
        nlp_analysis_v1.processandwritetofile(testwritefile,readerfulltext,lexiconArray,hashtablelex)
        sstring = ''
        openedreadfile = open(testwritefile)
        for k in openedreadfile:
            sstring += k.strip()

        if sstring !=  "['901102323925176321', [0, 0, 0, 2, 0, 2, 0, 0, 3, 0]]['901102307902967808', [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]['901102320708145153', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]['901102328828354560', [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]['901102310453108736', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]":
            raise()
        print('processandwritetofile() works as intended.')
    except:
        print('Error occurred in testing processandwritetofile().')
    return

def test_sumscore():
    try:
        if nlp_analysis_v1.sumscore([0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 2, 0, 2, 0, 0, 3, 0]) !=  [0, 0, 0, 2, 0, 2, 0, 0, 4, 0]:
            raise()
        print('sumscore() works as intended.')
    except:
        print('Error occurred in testing sumscore().')
    return


def test_updatepreviouslinesentimentscore():
    try:


        lexiconArray = nlp_analysis_v1.readLexicon('testlexicon.txt')
        hashtablelex = nlp_analysis_v1.createdictionary(lexiconArray)
        readerfulltext = open('testtweets.csv')
        testwritefile = 'testwrittenfile.txt'
        writingfile = open(testwritefile, 'w')
        nlp_analysis_v1.processandwritetofile(testwritefile,readerfulltext,lexiconArray,hashtablelex)
        nlp_analysis_v1.updatepreviouslinesentimentscore([0, 0, 0, 99, 0, 108, 0, 77, 0, 0], 901102310453108736, 224, writingfile)
        writingfile.close()
        openedreadfile = open(testwritefile)
        sstring = ''
        for k in openedreadfile:
            sstring += k.strip()

        if sstring != "['901102323925176321', [0, 0, 0, 2, 0, 2, 0, 0, 3, 0]]['901102307902967808', [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]['901102320708145153', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]['901102328828354560', [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]][901102310453108736, [0, 0, 0, 99, 0, 108, 0, 77, 0, 0]]":
            raise()
        print('updatepreviouslinesentimentscore() works as intended.')
    except:
        print('Error occurred in testing updatepreviouslinesentimentscore().')
    return

def test_load_timedata():
    try:

        testtimefile = 'testtime.csv'
        result = nlp_analysis_v1.load_timedata(testtimefile)
        if str(result[1]) != '2017-08-25 15:21:50':
            raise()
        if str(result[0].__next__()) != "['901102323925176321', 'Fri Aug 25 15:21:50 +0000 2017']":
            raise()
        print('load_timedata() works as intended.')
    except:
        print('Error occurred in testing load_timedata().')
    return



def test_calculateelapsedtimeandwritetofile():
    try:
        testtimefile = 'testtime.csv'
        result = nlp_analysis_v1.load_timedata(testtimefile)
        tweettimeoutputdata = 'testtimewrittenfile.txt'
        nlp_analysis_v1.calculateelapsedtimeandwritetofile(tweettimeoutputdata, result[0], result[1])
        opentimefile = open(tweettimeoutputdata)
        sstring = ''
        for k in opentimefile:
            sstring += k.strip()

        if sstring !=  "['901102323925176321', 0]['901102307902967808', 3]['901102320708145153', 3]['901102328828354560', 6]['901102310453108736', 7]":
            raise()
        print('calculateelapsedtimeandwritetofile() works as intended.')
    except:
        print('Error occurred in testing calculateelapsedtimeandwritetofile().')
    return


def test_calculateelapsedtimeinhours():
    try:

        earliertime = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Fri Aug 25 19:21:46 +0000 2017", '%a %b %d %H:%M:%S +0000 %Y'))
        earliertime = dt.datetime.strptime(earliertime, '%Y-%m-%d %H:%M:%S')
        latertime = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Fri Aug 25 23:21:47 +0000 2017", '%a %b %d %H:%M:%S +0000 %Y'))
        latertime = dt.datetime.strptime(latertime, '%Y-%m-%d %H:%M:%S')
        if nlp_analysis_v1.calculateelapsedtimeinhours(latertime, earliertime) != 4:
            raise()
        print('calculateelapsedtimeinhours() works as intended.')
    except:
        print('Error occurred in testing calculateelapsedtimeinhours().')
    return



def test_generatetimetosentimentscoredictionary():
    try:
        lexiconArray = nlp_analysis_v1.readLexicon('testlexicon.txt')
        hashtablelex = nlp_analysis_v1.createdictionary(lexiconArray)
        readerfulltext = open('testtweets.csv')
        testwritefile = 'testwrittenfile.txt'
        nlp_analysis_v1.processandwritetofile(testwritefile, readerfulltext, lexiconArray, hashtablelex)

        testtimefile = 'testtime.csv'
        result = nlp_analysis_v1.load_timedata(testtimefile)
        tweettimeoutputdata = 'testtimewrittenfile.txt'
        nlp_analysis_v1.calculateelapsedtimeandwritetofile(tweettimeoutputdata, result[0], result[1])

        if nlp_analysis_v1.generatetimetosentimentscoredictionary(testwritefile, tweettimeoutputdata) !=  {0: [0, 0, 0, 2, 0, 2, 0, 0, 3, 0, 1], 3: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2], 6: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}:
            raise()
        print('generatetimetosentimentscoredictionary() works as intended.')
    except:
        print('Error occurred in testing generatetimetosentimentscoredictionary().')
    return



if __name__ == '__main__':


    print('this python file tests all functions in nlp_analysis_v1')
    print('__________________test starting')
    test_readLexicon()
    test_createdictionary()
    test_matchtohashtable()
    test_wordsentimentcalculation()
    test_updatescores()
    test_preprocesstweettextforanalysis()
    test_processandwritetofile()
    test_sumscore()
    test_updatepreviouslinesentimentscore()
    test_load_timedata()
    test_calculateelapsedtimeandwritetofile()
    test_calculateelapsedtimeinhours()
    test_generatetimetosentimentscoredictionary()
    print('__________________test ending')