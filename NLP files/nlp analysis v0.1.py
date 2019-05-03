import csv
import re

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


def createhashtable(lexiconArray):
    #Function description: takes the array from readLexicon and create and return a hash table. The each entry in the
    #                      hash table array is in the form of [word, index_number_for_the_word_in_readLexicon_array]



    #create hash table, the first hashing function is python's hash() function
    #in case of collisions, double probing is used where the same python's hash function is used but the input for the hash function has "jump appended to it
    #the hash table is of size 20261, to be at approximately a load factor of 70% and 20261 us chosen because it is a prime numbeer
    hashtablelex = []
    hashtSize = 20261
    for k in range(hashtSize):
        hashtablelex.append([])

    currentindex = 0
    for k in lexiconArray:
        addhashindex = hash(k[0]) % hashtSize
        if hashtablelex[addhashindex] == []:
            hashtablelex[addhashindex] = [k[0],currentindex]
        else:
            probingjump = hash(k[0] + "jump") % hashtSize
            while True:
                addhashindex = (addhashindex + probingjump) % hashtSize

                if hashtablelex[addhashindex] == []:
                    hashtablelex[addhashindex] = [k[0], currentindex]
                    break

        currentindex += 1

    return hashtablelex


def matchtohashtable(fullword,lexiconArray,hashtablelex):
    #Function description: matches fullword to its resective word in lexiconArray, returns:
    #                      index for the matched word withs its sentiments in lexiconArray if found,
    #                      None value if not found

    hashtSize = len(hashtablelex)
    checkinghashindex = hash(fullword)% hashtSize
    probingjump = hash(fullword + "jump") % hashtSize


    #if the data at the index is not [], check if it is in the table and return it if it is, None if it is not,
    # if it is [], it means the word is not in the hash table so return None
    if hashtablelex[checkinghashindex] != []:
        if hashtablelex[checkinghashindex][0] == fullword:
            return lexiconArray[hashtablelex[checkinghashindex][1]]
        else:
            while True:
                checkinghashindex = (checkinghashindex + probingjump) % hashtSize

                if hashtablelex[checkinghashindex] == []:
                    return None;
                else:
                    if hashtablelex[checkinghashindex][0] == fullword:
                        return lexiconArray[hashtablelex[checkinghashindex][1]]
    else:
        return None


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


def load_fulltext(fulltextfile):


    textfile = open(fulltextfile, 'r')

    csvreaderfulltext = csv.reader(textfile)

    #skip first line its csv because the line contains only row header
    next(csvreaderfulltext, None)

    #calculate number of rows in the csv and return pointer back to the top of the file
    row_count = sum(1 for row in csvreaderfulltext)
    textfile.seek(0)
    next(csvreaderfulltext, None)



    return [csvreaderfulltext, row_count]


def preprocesstweettextforanalysis(tweettext):
    #Function description: Takes the tweet fulltext as inoput and returns an array of words in the fulltext, where
    #                      any non-lowercase-ASCII-letter are not included.

    #set all words in tweet text to lower case
    tweettext = tweettext.lower()

    #replace all non-lowercase-ASCII-letter from tweet text with space.
    tweettext = re.sub("[^a-z]", " ", tweettext)


    return tweettext.split()







if __name__ == "__main__":
    #extra documentation:
    #lexiconArray should be of size 14182 unless a different lexicon is used
    #the size of hash table at approximately 70% load factor created based on lexiconArray is 20261, and 20261 is chosen because it is a prime nuber
    #this program does not analyse emoticon for sentiments, but if desired, it can be added later by adding sentiment
    # scores into the emolex and modify the preprocesstweettextforanalysis to tokenize emoticons too

    # import pandas as pd
    # df = pd.read_csv("irma_cleaned.csv")
    # # saved_column = df.column_name
    #
    # print("a")
    # print(df["full_text"])
    # print("a")
    #


    print('_______________________START______________________________________________________    ')

    lexiconArray = readLexicon('lexicon.txt')

    # print(lexiconArray)
    # print(len(lexiconArray))



    hashtablelex = createhashtable(lexiconArray)



    print(hashtablelex)
    print(len(hashtablelex))

    print(matchtohashtable('praiseworthy',lexiconArray,hashtablelex))
    print(wordsentimentcalculation(['praiseworthy'], lexiconArray, hashtablelex))




    print('_____________________________________________________________________________    ')



    #todo:
    #use calculatesentimentscorefortweet() on preprocessed full_text
    #testing of all untested functions
    #_____________________________________________________________________________________


    csvreaderfulltextdata = load_fulltext("irma_fulltext.csv")
    #
    csvreaderfulltext = csvreaderfulltextdata[0]

    row_count = csvreaderfulltextdata[1]

    print(row_count)

    listoftweetsentimentscore = []
    tweetwordarray = []
    for row in csvreaderfulltext:
        print(row[1])
        tweetwordarray = preprocesstweettextforanalysis(row[1])
        # print(tweetwordarray)
        listoftweetsentimentscore.append([row[0],wordsentimentcalculation(tweetwordarray,lexiconArray,hashtablelex)])
        # print(listoftweetsentimentscore)
        # break   #uncomment this break line to only analyse 1 row of csvreaderfulltext


    #open file to write sentiment score
    writingfile = open("writtenfile001.txt", "w+")

    #empty file before writing
    writingfile.truncate()

    #write tweet ids along with sentiment score
    for k in listoftweetsentimentscore:
        writingfile.write(str(k) + "\n")

    print('|||||||||||||||||||HHH||||||')



