import csv
import re
import time
import datetime as dt
from ast import literal_eval
import matplotlib.pyplot as plt





def readLexicon(lexfilename):
    """

    :param lexfilename: string of name for the file containing the emolex lexicon
    :return: list containing the processed data of the emolex lexicon. Each entry in the list takes the form of
    [word followed by 1st to 10th sentiment in this order] which is
    [word, anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust]
    which means each list entry shows the 'word' followed by its 10 sentiments.
    """
    #initialize array for lexicon
    lexiconArray = []

    # open lexicon text for reading and skip first line since its empty
    lexicon = open(lexfilename)
    next(lexicon)

    # for each 1st of 10 line read,
    #     for the 1st line: append the word and its sentiment value for the word for this line to lexiconArray
    #     otherwise: just append the respective sentiment value to its respective array in lexiconArray,
    lexiconArrayIndex = -1
    resettingline = 10
    for line in lexicon:

        lineappend = line.split()

        if resettingline == 10:
            lexiconArray.append([lineappend[0], lineappend[2]])
            lexiconArrayIndex += 1

        else:
            lexiconArray[lexiconArrayIndex].append(lineappend[2])

        resettingline -= 1
        if resettingline == 0:
            resettingline = 10


    #return the lexiconArray
    return (lexiconArray)


def createdictionary(lexiconArray):
    """

    :param lexiconArray: list contataining processed data of the Emolex lexicon
    :return: dictionary created using lexiconArray, containing key-value pair of the form
    of {word:index number for the word in read lexiconArray}
    """

    hashtablelex = {}


    currentindex = 0
    for k in lexiconArray:
        hashtablelex[k[0]] = currentindex
        currentindex += 1


    return hashtablelex


def matchtohashtable(fullword,lexiconArray,hashtablelex):
    """

    :param fullword: string of the key to be searched in the dictionary hashtablelex
    :param lexiconArray: list containing processed data of the Emolex lexicon
    :param hashtablelex: dictionary created using lexiconArray, containing key-value pair of the form
    of {word:index number for the word in read lexiconArray}
    :return: if fullword is not found in hashtablelex, return None, otherwise return the list of the full word appended
     by the 10 sentiment score for the matched fullword
    """
    #Function description: matches fullword to its respective word in lexiconArray, returns:
    #                      the array in lexiconArray for the matched word withs its sentiments in lexiconArray if found,
    #                      None value if not found

    wordlexiconindex = hashtablelex.get(fullword)
    if wordlexiconindex == None:
        return None
    else:
        return lexiconArray[wordlexiconindex]


def wordsentimentcalculation(tweetwordarray, lexiconArray, hashtablelex):
    """

    :param tweetwordarray: list of words in the tweet
    :param lexiconArray: list containing processed data of the Emolex lexicon
    :param hashtablelex: dictionary created using lexiconArray, containing key-value pair of the form
    of {word:index number for the word in read lexiconArray}
    :return: list containing the the sum of sentiments scores for all words in tweetwordarray
    """
    #ensure full_text has been preprocessed, so its form should be an array of words
    #this functions does not analyse emoticons
    sentimentscores = [0,0,0,0,0,0,0,0,0,0]
    for word in tweetwordarray:
        resultt = matchtohashtable(word, lexiconArray, hashtablelex)
        if resultt != None:
            sentimentscores = updatescores(sentimentscores,resultt);

    return sentimentscores


def updatescores(sentimentscores,resultt):
    """

    :param sentimentscores: list containing the 10 sentiment scores
    :param resultt: list containing the word for the sentiment score and the 10 sentiment scores
    :return: list containing the sum of the 10 sentiment scores of sentimentscores and resultt
    """

    #updates sentiment score using result from matching using hash table and word in tweet
    scoreindex = 0
    resultindexx = 0

    for k in resultt:
        #if statement used to skip first entry because resultt also contains the one word matched, not only sentiment
        # scores.
        if resultindexx != 0:
            sentimentscores[scoreindex] += int(resultt[resultindexx])
            scoreindex += 1
        resultindexx += 1

    return sentimentscores


def preprocesstweettextforanalysis(tweettext):
    """

    :param tweettext: string of the tweet's fulltext
    :return: string of tweettext's alphabets in lowercase. All non-alphabets are excluded.
    """
    #Function description: Takes the tweet fulltext as inoput and returns an array of words in the fulltext, where
    #                      any non-lowercase-ASCII-letter are not included.

    #set all words in tweet text to lower case
    tweettext = tweettext.lower()

    #replace all non-lowercase-ASCII-letter from tweet text with space.
    tweettext = re.sub("[^a-z]", " ", tweettext)


    return tweettext.split()


def processandwritetofile(tweetscoreoutputfilename, readerfulltext,lexiconArray,hashtablelex):
    """
    This function is called to process the sentiment score of all Tweet's in readerfulltext. The calculated sentiment
    score for each tweet is the written into the file named tweetscoreoutputfilename with new lines one by one as the
    processing takes place. Note that any outout file with the same named will be replaced. Note that readerfulltext
    is closed once this functions ends.

    :param tweetscoreoutputfilename: string for the name of the file for the processed data to be written into
    :param readerfulltext: opened file of the file for containing tweets' fulltext data, note that the first line is
    skipped in this function because it is assumed that the first line contains only field data for the opened file
    :param lexiconArray: list containing processed data of the Emolex lexicon
    :param hashtablelex: dictionary created using lexiconArray, containing key-value pair of the form
    of {word:index number for the word in read lexiconArray}
    :return: None
    """
    tweetwordarray = []

    #open file to write sentiment score
    writingfile = open(tweetscoreoutputfilename, "w+")

    previouslinedata = []

    #skip the first line because it contains fields data, not the tweet data we want
    readerfulltext.readline()

    for lines in readerfulltext:
        fields = lines.split(',', 1)

        #for cases where a tweet's full text covers more than 1 line in the csv file, in this case, update score of
        #previous line, or when a tweet continues to a row with 2 fields that is not a new tweet

        if (len(fields) == 1) or (not fields[0].isdigit()):
            tweetwordarray = preprocesstweettextforanalysis(fields[0])
            calculatedsentimentscore = wordsentimentcalculation(tweetwordarray, lexiconArray, hashtablelex)

            previouslinetweetid = previouslinedata[0]
            previoussentimentscore = previouslinedata[1]
            newupdatedscore = sumscore(previoussentimentscore,calculatedsentimentscore)

            writingfile = updatepreviouslinesentimentscore(newupdatedscore, previouslinetweetid, lastlinefileposition, writingfile)

            previouslinedata[1] = newupdatedscore
            continue

        #for handling rows with less than 2 fields, all rows should have 2 rows
        if len(fields) != 2:
            continue

        tweetwordarray = preprocesstweettextforanalysis(fields[1])
        calculatedsentimentscore = wordsentimentcalculation(tweetwordarray,lexiconArray,hashtablelex)
        tweetsentimentscoredata = ([fields[0],calculatedsentimentscore])

        lastlinefileposition = writingfile.tell()
        writingfile.write(str(tweetsentimentscoredata) + "\n")

        previouslinedata = tweetsentimentscoredata
    readerfulltext.close()
    return


def sumscore(previoussentimentscore,calculatedsentimentscore):
    """
    
    :param previoussentimentscore: first list of integer scores to be summed, of n length.
    :param calculatedsentimentscore: second list of integer scores to be summed, of n length.
    :return: list of summed score, of n length. The summing is the sum of k-th integer of booth list, where k-th starts
    from 0-th to n-th.
    """
    #sum scores in two arrays
    newupdatedscore = []
    index = 0
    for score in previoussentimentscore:
        newupdatedscore += [score+calculatedsentimentscore[index]]
        index += 1
    return newupdatedscore


def updatepreviouslinesentimentscore(newupdatedscore, previouslinetweetid, lastlinefileposition, writingfile):
    """
    Update the tweet id sentiment score of the last tweet in writingfile by deleting the last line in writingfile and
    then adding a new line containing [previouslinetweetid, newupdatedscore].

    :param newupdatedscore: list containing the sentiment score to be added to the file
    :param previouslinetweetid: string of tweet id of tweet to be added into writingfile.
    :param lastlinefileposition: the position of the beginning of the last line in writingfile. This can be usually
    obtained using writingfile.tell() before writing a new line into writingfile
    :param writingfile: the opened file for deletion of line and adding of new line of data
    :return: the opened file for deletion of line and adding of new line of data
    """

    #move pointer to beginning of previous line to delete the line by truncating at the pointer
    writingfile.seek(lastlinefileposition)
    writingfile.truncate()

    #write the new uupdate sentiment score to the file
    writingfile.write(str([previouslinetweetid, newupdatedscore]) + "\n")
    return writingfile


def load_timedata(timedatafilename):
    """

    :param timedatafilename: string of name for the file containing time data for the Tweets
    :return: list of size 2, containing [csvreader for the file containing time data for the Tweets, time stamp of
    the tweet in the file's first line
    """
    timefile = open(timedatafilename, 'r')
    csvreadertimedata = csv.reader(timefile)

    #skip first line its csv because the line contains only row header
    next(csvreadertimedata, None)

    for row in csvreadertimedata:
        firstrowtimedata = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(row[1],'%a %b %d %H:%M:%S +0000 %Y'))
        firsttweettimestampdata = dt.datetime.strptime(firstrowtimedata, '%Y-%m-%d %H:%M:%S')
        break
    #move csvreader pointer to its first row
    timefile.seek(0)
    next(csvreadertimedata, None)



    return [csvreadertimedata, firsttweettimestampdata]


def calculateelapsedtimeandwritetofile(tweettimeoutputdata, csvreadertimedata, firsttweettimedata):
    """
    Process and prepare time data file for graphing tweet sentiment scores against time. The time data file is set
    to write into a file named tweettimeoutputdata, so any file of the same name will be erased before writing.

    :param tweettimeoutputdata: string for the name of the file for the processed data to be written into
    :param csvreadertimedata: csvreader of the file containing time data for the Tweets
    :param firsttweettimedata: time stamp of the tweet in the file's first line
    :return: None
    """
    # open file to write sentiment score
    writingfile = open(tweettimeoutputdata, "w+")
    # empty file before writing
    writingfile.truncate()

    for row in csvreadertimedata:

        #convert relevant row data into timestamp
        tweettimestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(row[1],'%a %b %d %H:%M:%S +0000 %Y'))
        tweettimestamp = dt.datetime.strptime(tweettimestamp, '%Y-%m-%d %H:%M:%S')

        if tweettimestamp < firsttweettimedata:
            elapsedtimeinhours = 0
        else:
            elapsedtimeinhours = calculateelapsedtimeinhours(tweettimestamp, firsttweettimedata)
        tweetelapsedtimedata = [row[0], elapsedtimeinhours]

        writingfile.write(str(tweetelapsedtimedata) + "\n")

    writingfile.close()
    return


def calculateelapsedtimeinhours(tweettimestamp, firsttweettimedata):
    """

    :param tweettimestamp: time stamp of tweet's creation time
    :param firsttweettimedata: time stamp of first tweet's creation time
    :return: Elapsed hours in integer of tweet's creation time since the first tweet, the returned hour is rounded down.
    """
    timedifference = tweettimestamp - firsttweettimedata
    return ((timedifference.days * 24) + (timedifference.seconds // 3600 ))#PUT FORMULA FOR COUNTING THE ELAPSED HOUR HERE


def generatetimetosentimentscoredictionary(scorefile, timefile):
    """

    :param scorefile: string for the file name of the file containing the tweet's id_str and its respective array of 
    sentiment scores, with the same number of lines as timefile
    :param timefile: string for the file name of the file containing the tweet's id_str and its respective time elapse 
    from the first tweet, with the same number of lines as timefile
    :return: dictionary in the form of {integer hours elapsed since the first tweet: the list of sum of all tweet's 
    sentiment score for the integer hour appended by the number of tweeets for this hour}. Note that the value part
    of the dictionary's key value pair is an array of length 10 + 1, where each score, 10 scores in total,
    corresponds to the score in the order of ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative',
    'positive', 'sadness', 'surprise', 'trust'] + [number of tweets for this hour].
    """

    processedsentimentscorefile = open(scorefile, 'r')
    processedtimefile = open(timefile, 'r')

    timetoscoredictionary = {}

    for sentimentscoreline in processedsentimentscorefile:
        #set the second field of the file, which is the time elapsed in hours, to correspondingtime
        correspondingtime = processedtimefile.readline().split(',', 1)
        correspondingtime = int((correspondingtime[1]).replace(']', '').strip())

        #set the second field of the file, which is the list of sentiment scores, to correspondingscore
        correspondingscore = sentimentscoreline.split(',', 1)
        correspondingscore = correspondingscore[1].replace(']]', ']').strip()
        correspondingscore = literal_eval(correspondingscore)

        scoreforthishourtime = timetoscoredictionary.get(correspondingtime) 

        #if the elapsd time is not recorded in the dictionary, record it along with its corresponding score
        if scoreforthishourtime == None:
            timetoscoredictionary[correspondingtime] = (correspondingscore + [1])
        #otherwise, update the matched time's correspondingscore
        else:
            timetoscoredictionary[correspondingtime] = sumscore((correspondingscore + [1]), scoreforthishourtime)


    return timetoscoredictionary

def plotgraphwithtimeandsentimentdictionary(timetosentimentdictionary):
    """
    Plot two graphs, first graph is a graph of      total Tweets' sentiment scores against time, the second is a graph
    of average Tweets' sentiment scores against time

    :param timetosentimentdictionary: the dictionary with key-pair in the form of {time elapsed in hour: list, of
    size 11, containing the 10 sentiment appended by 1 value for the number of tweets in the hour}
    :return: None
    """
    plothours = []
    plotscores = []
    listofnumberoftweetsforthehour = []

    #there are 10 type of sentiment sccore for each tweet
    for k in range(10):
        plotscores.append([])

    for dkey,dvalue in timetosentimentdictionary.items():
        plothours.append(dkey)
        listofnumberoftweetsforthehour.append(dvalue[len(dvalue) - 1])
        index = 0
        for dsentimentvalue in dvalue[:-1]:
            plotscores[index].append(dsentimentvalue)
            index += 1

    #plot graph of total sentiment score against time
    graphone = plt.figure(1)
    for k in range(10):
        plt.plot(plothours, plotscores[k])
    plt.title("Total Tweets' sentiment scores over time")
    plt.xlabel('Hours elapsed since first Tweet')
    plt.ylabel('Sentiment score')
    plt.legend(['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise',
                'trust'], loc = 'upper left', prop={'size': 6})

    plt.show()

    #plot graph of average sentiment score per tweet against time
    graphtwo = plt.figure(2)
    averagesentimentscorepertweet = []

    avgindex = -1
    for summedscore in plotscores:
        averagesentimentscorepertweet.append([])
        avgindex += 1
        for k in summedscore:
            averagesentimentscorepertweet[avgindex].append(k/listofnumberoftweetsforthehour[avgindex])

    for k in range(10):
        plt.plot(plothours, averagesentimentscorepertweet[k])
    plt.title("Average Tweet sentiment scores over time")
    plt.xlabel('Hours elapsed since first Tweet')
    plt.ylabel('Sentiment score')
    plt.legend(['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise',
                'trust'], loc = 'upper left', prop={'size': 6})

    plt.show()

    return

def categorizationhistogram(scorefile):
    """
    Categorize each tweet based on their maximum sentiment score, if the max score is 0, it is categorized as neutral,
    otherwise if there are one or more sentiment values that matches the maximum score, the tweet is categorized
    based on the one or more categorized values. This means that a tweet will be categorized as neutral if its max
    score is 0 and can have 1 or more categorization otherwise because there can be more than 1 sentiment score
    type that matches the max score. The categorized data are then visualised onto a histogram.

    :param scorefile: string for the file name of the file containing the tweet's id_str and its respective array of
    sentiment scores
    :return: None
    """


    tweetscores = open(scorefile, 'r')

    # sentiment type reference for listforcategorization: [anger, anticipation, disgust, fear, joy, negative,
    # positive, sadness, surprise, trust, neutral]
    listforcategorization = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for scoreline in tweetscores:

        # set the second field of the file, which is the list of sentiment scores, to correspondingscore
        correspondingscore = scoreline.split(',', 1)
        correspondingscore = correspondingscore[1].replace(']]', ']').strip()
        correspondingscore = literal_eval(correspondingscore)


        highestscore = max(correspondingscore)

        #if max score is 0, categorize as neutral
        if highestscore == 0:
            listforcategorization[10] += 1
            continue

        #if the max score is not 0, categorize the tweet based on the sentiment value type that matches the highest
        # score. Note that more than 1 score type can match so the tweet can have more than 1 categorization in
        # this case
        scoreindex = 0
        for sentimentscore in correspondingscore:
            if sentimentscore == highestscore:
                listforcategorization[scoreindex] += 1
            scoreindex += 1

    #plot the histogram
    plt.bar(['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise',
             'trust', 'neutral'], height=listforcategorization)
    plt.xticks(rotation=90)
    plt.xlabel('Sentiment Type')
    plt.ylabel('Number of tweets')
    plt.title('Categorized Tweets')
    plt.show()
    return

if __name__ == "__main__":

    print('_______________________START______________________________________________________    ')

    tweetscoreoutputfilename = "writtenfile001.txt"
    tweettimeoutputfilename = 'timewrittenfile001.txt'
    fulltextdatafilename = "harvey_fulltext.csv"
    tweetidcreatedatfilename = "harvey_idstr_createdat.csv"
    lexiconfilename = 'lexicon.txt'

    lexiconArray = readLexicon(lexiconfilename)
    hashtablelex = createdictionary(lexiconArray)

    print('________________________FINISHED PROCESSING LEXICON_________________________________________________    ')

    readerfulltext = open(fulltextdatafilename, 'r')

    print('||||||prrocessing and writing|||||||||')

    #create and initialise empty output for writing and reading, if it already exists, the file is emptied
    writingfile = open(tweetscoreoutputfilename, "w")
    writingfile.close()
    processandwritetofile(tweetscoreoutputfilename, readerfulltext, lexiconArray, hashtablelex)

    print('|||||||||||||||||||FINISHED GENERATING AND WRITING TWEET SCORES|||||||||')

    csvreadertimedata = load_timedata(tweetidcreatedatfilename)
    csvreadertime = csvreadertimedata[0]
    firsttweettimestampdata = csvreadertimedata[1]
    calculateelapsedtimeandwritetofile(tweettimeoutputfilename, csvreadertime, firsttweettimestampdata)


    print('|||||||||||||||||||FINISHED PROCESSING TIME FILE|||||||||')

    timetosentimentdictionary = generatetimetosentimentscoredictionary(tweetscoreoutputfilename, tweettimeoutputfilename)
    plotgraphwithtimeandsentimentdictionary(timetosentimentdictionary)

    print('|||||||||||||||||||FINISHED GENERATING TIME TO SCORE GRAPH|||||||||')

    categorizationhistogram(tweetscoreoutputfilename)

    print('|||||||||||||||||||PROGRAM END|||||||||')



#NOTE:
#the id_created and fulltext csv files need to have its last line as empty or this program may throw an error.
#data in each array in lexiconArray is:
# [word followed by 1st to 10th sentiment in this order]:
# [word, anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust]
#the sentiment analysis only analyse rows with 2 fields, there are at least 1 row with less than 2 field in both csv
# for Harvey and Irma, and some rows has 3 fields
#note that it may not be the same for data regarding tweet's created time, as the tweet time data may all have 2 fields
# so all field for time data are processed, unlike fulltext data where some row have less than 2 fields and are skipped
#the first tweet in both fulltext.csv and id_str_created_at.csv will be used to graph tweets, any tweets later
# with the file that is created before the tweet will has 0 scored for time elapsed in hours. (Example: first
# tweet is created at 3pm, any tweet read after the first tweet rom the file that is created before 3pm on the
# same day and year will have 0 scored as time elapsed in hours.) Because of this, we recommend sorting the tweets
# by time before using this program to perform sentiment analysis on it.
#this program needs matplotlib installed in python for it to run and do graphing
#this program does not analyse emoticon for sentiments, but if desired, it can be added later by adding sentiment
# scores into the emolex and modify the preprocesstweettextforanalysis to tokenize emoticons too


#todo:
#add pre conditions and post conditions
#understand what to do for ML task
#Everything works and are documented and tested. If theres something to do, its probably cleaning code for better
# look since its messy. The codings can also be edited to be more efficient.






