import csv
import re
import time
import datetime as dt

# #ways to categorize
#
#
#
# f = open("irma_cleaned.csv", encoding="utf8");
#
# reader = csv.reader(f)
#
#
#
# if __name__ == "__main__":
#
#     for row in reader:
#         print(row);
#
#
#
#
# f.close();







def readLexicon(lexfilename):
    #Function description: Takes the lexicon text file as input and return an array. Note that the array follow the form of:
    #                      [word followed by 1st to 10th sentiment in this order]:
    #                      [word, anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust]
    #                      which means each array entry shows the 'word' followed by its 10 sentiments



    #initialize array for lexicon
    lexiconArray = []

    # open lexicon text for reading and skip first line since its empty
    lexicon = open(lexfilename)
    next(lexicon)

    # for each 1st of 10 line read,
    #     for the 1st line: append the word and its sentiment value for the word for this line to lexiconArray
    #     otherwise: just append the respective sentiment value to its respective array in lexiconArray,
    #NOTE: data in each array in lexiconArray is:
    # [word followed by 1st to 10th sentiment in this order]:
    # [word, anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust]
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
    #Function description: takes the array from readLexicon and create and return a dictionary. The each entry in the
    #                      dictionary is in the form of (word: index_number_for_the_word_in_readLexicon_array)

    hashtablelex = {}


    currentindex = 0
    for k in lexiconArray:
        hashtablelex[k[0]] = currentindex
        currentindex += 1


    return hashtablelex


def matchtohashtable(fullword,lexiconArray,hashtablelex):
    #Function description: matches fullword to its respective word in lexiconArray, returns:
    #                      the array in lexiconArray for the matched word withs its sentiments in lexiconArray if found,
    #                      None value if not found

    wordlexiconindex = hashtablelex.get(fullword)
    if wordlexiconindex == None:
        return None
    else:
        return lexiconArray[wordlexiconindex]



def wordsentimentcalculation(tweetwordarray, lexiconArray, hashtablelex):
    #ensure full_text has been preprocessed, so its form should be an array of words
    #this functions does not analyse emoticons

    sentimentscores = [0,0,0,0,0,0,0,0,0,0]
    for word in tweetwordarray:
        resultt = matchtohashtable(word, lexiconArray, hashtablelex)
        if resultt != None:
            sentimentscores = updatescores(sentimentscores,resultt);

    return sentimentscores


def updatescores(sentimentscores,resultt):
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
    #Function description: Takes the tweet fulltext as inoput and returns an array of words in the fulltext, where
    #                      any non-lowercase-ASCII-letter are not included.

    #set all words in tweet text to lower case
    tweettext = tweettext.lower()

    #replace all non-lowercase-ASCII-letter from tweet text with space.
    tweettext = re.sub("[^a-z]", " ", tweettext)


    return tweettext.split()



def processandwritetofile(readerfulltext,lexiconArray,hashtablelex):
    tweetwordarray = []

###########################################################################
    lessthantwocounter = 0
    morethantwocounter = 0
    counter = 0
###########################################################################


    #open file to write sentiment score
    writingfile = open("writtenfile001.txt", "r+")

    previouslinedata = []

    for lines in readerfulltext:
        fields = lines.split(',', 1)
###########################################################################
        if len(fields) > 2:
            morethantwocounter += 1
            print('333333number of fields: ', len(fields), 'row data: ', fields, 'counter', counter)
        else:
            if len(fields) < 2:
                lessthantwocounter += 1

                print('number of fields: ', len(fields), 'row data: ', fields, 'counter', counter)
###########################################################################

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

##############################################################################
        counter += 1

##############################################################################

##############################################################################
    print("lessthantwocounter: ", lessthantwocounter)
    print("morethantwocounter: ", morethantwocounter)
    print('counter: ,', counter)
##############################################################################

    return


def sumscore(previoussentimentscore,calculatedsentimentscore):
    #sum scores in two arrays
    newupdatedscore = []
    index = 0
    for score in previoussentimentscore:
        newupdatedscore += [score+calculatedsentimentscore[index]]
        index += 1
    return newupdatedscore


def updatepreviouslinesentimentscore(newupdatedscore, previouslinetweetid, lastlinefileposition, writingfile):

    print(writingfile.tell(), newupdatedscore, lastlinefileposition)
    #move pointer to beginning of previous line to delete the line by truncating at the pointer
    writingfile.seek(lastlinefileposition) #instead of writingfile.seek((writingfile.tell() - lastlinefileposition), 2)
    writingfile.truncate()

    #write the new uupdate sentiment score to the file
    writingfile.write(str([previouslinetweetid, newupdatedscore]) + "\n")
    return writingfile


def load_timedata(timedatafilename):
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

def calculateelapsedtimeandwritetofile(csvreadertimedata, firsttweettimedata):
    # open file to write sentiment score
    writingfile = open("timewrittenfile001.txt", "w+")
    # empty file before writing
    writingfile.truncate()

    for row in csvreadertimedata:


        tweettimestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(row[1],'%a %b %d %H:%M:%S +0000 %Y'))
        tweettimestamp = dt.datetime.strptime(tweettimestamp, '%Y-%m-%d %H:%M:%S')

        if tweettimestamp < firsttweettimedata:
            elapsedtimeinhours = 0
        else:
            elapsedtime = tweettimestamp-firsttweettimedata
            elapsedtimeinhours = calculateelapsedtimeinhours(tweettimestamp, firsttweettimedata)
        tweetelapsedtimedata = [row[0], elapsedtimeinhours]

        writingfile.write(str(tweetelapsedtimedata) + "\n")


    return

def calculateelapsedtimeinhours(tweettimestamp, firsttweettimedata):
    #Function description: calculate time difference between tweettimestamp and firsttweettimedata, output is rounded
    #                      down to integer in hours
    timedifference = tweettimestamp - firsttweettimedata
    return ((timedifference.days * 24) + (timedifference.seconds // 3600 ))#PUT FORMULA FOR COUNTING THE ELAPSED HOUR HERE



if __name__ == "__main__":
    #extra documentation:
    #lexiconArray should be of size 14182 unless a different lexicon is used
    #this program does not analyse emoticon for sentiments, but if desired, it can be added later by adding sentiment
    # scores into the emolex and modify the preprocesstweettextforanalysis to tokenize emoticons too

    print('_______________________START______________________________________________________    ')

    lexiconArray = readLexicon('lexicon.txt')

    # print('kkkkkk:   ', lexiconArray)
    # print(len(lexiconArray))

    hashtablelex = createdictionary(lexiconArray)


    #
    # print(hashtablelex)
    # print(len(hashtablelex))
    #
    # print(matchtohashtable('praiseworthy',lexiconArray,hashtablelex))
    # print(wordsentimentcalculation(['praiseworthy'], lexiconArray, hashtablelex))
    #
    # print('_____________________________________________________________________________    ')
    #
    #


    readerfulltext = open("irma_fulltext.csv", 'r')
    readerfulltext.readline()

    print('||||||prcoessing and writing|||||||||')

    #create and initialise empty output for writing and reading, if it already exists, the file is emptied
    writingfile = open("writtenfile001.txt", "w")
    writingfile.close()

    processandwritetofile(readerfulltext, lexiconArray, hashtablelex)

    print('|||||||||||||||||||PROGRAM END|||||||||')
#
# #todo:
# #testing
# #graphing
# #may want to remove computing "row_count", since its used only for printing
#
# #NOTE:
# #the sentiment analysis only analyse rows with 2 fields, there are at least 1 row with less than 2 field in both csv
# # for Harvey and Irma, and some rows has 3 fields
# #note that it may not be the same for data regarding tweet's created time, as the tweet time data may all have 2 fields
# # so all field for time data are processed, unlike fulltext data where some row have less than 2 fields and are skipped
# #the proram assumes the dataset is sorted chronologically, it msut be be sorted chronologically, by year, month, day,
# # and hours. The program will still work even if it is not sorted by minutes and seconds, as long as it is sorted by
# # year, month, day and hours.





#_____________________________________________________________________________________

    #
    #
    # csvreadertimedata = load_timedata("irma_idstr_createdat.csv")
    # csvreadertime = csvreadertimedata[0]
    # firsttweettimestampdata = csvreadertimedata[1]
    #
    # calculateelapsedtimeandwritetofile(csvreadertime, firsttweettimestampdata)
    #




    #
    #
    #
    #
    # tweettime = 'Fri Sep 01 14:03:58 +0000 2022'
    #
    #
    # tweettimestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweettime,'%a %b %d %H:%M:%S +0000 %Y'))
    #
    # tweettimestamp = dt.datetime.strptime(tweettimestamp, '%Y-%m-%d %H:%M:%S')
    #
    #
    # secondtweettime = 'Fri Sep 01 11:03:57 +0000 2017'
    #
    # secondtweettimestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(secondtweettime,'%a %b %d %H:%M:%S +0000 %Y'))
    #
    # secondtweettimestamp = dt.datetime.strptime(secondtweettimestamp, '%Y-%m-%d %H:%M:%S')
    #
    #
    # print(tweettimestamp)
    # print(secondtweettimestamp)
    #
    # print(type(tweettimestamp), '.........',tweettimestamp.second,'....',max(tweettimestamp,secondtweettimestamp))
    #
    # print('difference: ', (tweettimestamp - secondtweettimestamp).days)
    #
    # print('difference: ', (secondtweettimestamp - secondtweettimestamp).days)
    # print('difference: ', (secondtweettimestamp - tweettimestamp).days)
    #
    # print('check: ', secondtweettimestamp == tweettimestamp)
    # print('check: ', secondtweettimestamp < tweettimestamp)
    # print('check: ', secondtweettimestamp > tweettimestamp)
    #
    # print(dt.datetime.now())
    #
    # print(type(dt.datetime.now()))





