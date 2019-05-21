import csv
import re
import time
import datetime as dt
from ast import literal_eval
import matplotlib.pyplot as plt


def read_lexicon(lex_file_name):
    """

    :param lex_file_name: string of name for the file containing the emolex lexicon
    :return: list containing the processed data of the emolex lexicon. Each entry in the list takes the form of
    [word followed by 1st to 10th sentiment in this order] which is
    [word, anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust]
    which means each list entry shows the 'word' followed by its 10 sentiments.
    """
    # initialize array for lexicon
    lexicon_array = []

    # open lexicon text for reading and skip first line since its empty
    lexicon = open(lex_file_name, encoding='utf-8')
    next(lexicon)

    # for each 1st of 10 line read,
    #     for the 1st line: append the word and its sentiment value for the word for this line to lexicon_array
    #     otherwise: just append the respective sentiment value to its respective array in lexicon_array,
    lexicon_array_index = -1
    resetting_line = 10
    for line in lexicon:

        line_append = line.split()

        if resetting_line == 10:
            lexicon_array.append([line_append[0], line_append[2]])
            lexicon_array_index += 1

        else:
            lexicon_array[lexicon_array_index].append(line_append[2])

        resetting_line -= 1
        if resetting_line == 0:
            resetting_line = 10

    # return the lexicon_array
    return lexicon_array


def create_dictionary(lexicon_array):
    """

    :param lexicon_array: list containing processed data of the Emolex lexicon
    :return: dictionary created using lexicon_array, containing key-value pair of the form
    of {word:index number for the word in read lexicon_array}
    """

    hash_table_lex = {}

    current_index = 0
    for k in lexicon_array:
        hash_table_lex[k[0]] = current_index
        current_index += 1

    return hash_table_lex


def match_to_hash_table(full_word, lexicon_array, hash_table_lex):
    """

    :param full_word: string of the key to be searched in the dictionary hash_table_lex
    :param lexicon_array: list containing processed data of the Emolex lexicon
    :param hash_table_lex: dictionary created using lexicon_array, containing key-value pair of the form
    of {word:index number for the word in read lexicon_array}
    :return: if full_word is not found in hash_table_lex, return None, otherwise return the list of the full word
    appended by the 10 sentiment score for the matched full_word
    """

    word_lexicon_index = hash_table_lex.get(full_word)
    if word_lexicon_index is None:
        return None
    else:
        return lexicon_array[word_lexicon_index]


def word_sentiment_calculation(tweet_word_array, lexicon_array, hash_table_lex):
    """

    :param tweet_word_array: list of words in the tweet
    :param lexicon_array: list containing processed data of the Emolex lexicon
    :param hash_table_lex: dictionary created using lexicon_array, containing key-value pair of the form
    of {word:index number for the word in read lexicon_array}
    :return: list containing the the sum of sentiments scores for all words in tweet_word_array
    """
    # ensure full_text has been preprocessed, so its form should be an array of words
    # this functions does not analyse emoticons
    sentiment_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for word in tweet_word_array:
        result = match_to_hash_table(word, lexicon_array, hash_table_lex)
        if result is not None:
            sentiment_scores = update_scores(sentiment_scores, result)

    return sentiment_scores


def update_scores(sentiment_scores, result):
    """

    :param sentiment_scores: list containing the 10 sentiment scores
    :param result: list containing the word for the sentiment score and the 10 sentiment scores
    :return: list containing the sum of the 10 sentiment scores of sentiment_scores and result
    """

    # updates sentiment score using result from matching using hash table and word in tweet
    score_index = 0
    result_index = 0

    for k in result:
        # if statement used to skip first entry because result also contains the one word matched, not only sentiment
        # scores.
        if result_index != 0:
            sentiment_scores[score_index] += int(result[result_index])
            score_index += 1
        result_index += 1

    return sentiment_scores


def preprocess_tweet_text_for_analysis(tweet_text):
    """

    :param tweet_text: string of the tweet's fulltext
    :return: string of tweet_text's alphabets in lowercase. All non-alphabets are excluded.
    """
    # set all words in tweet text to lower case
    tweet_text = tweet_text.lower()

    # replace all non-lowercase-ASCII-letter from tweet text with space.
    tweet_text = re.sub("[^a-z]", " ", tweet_text)

    return tweet_text.split()


def process_and_write_to_file(tweet_score_output_file_name, reader_full_text, lexicon_array, hash_table_lex):
    """
    This function is called to process the sentiment score of all Tweet's in reader_full_text. The calculated sentiment
    score for each tweet is the written into the file named tweet_score_output_file_name with new lines one by one as the
    processing takes place. Note that any outout file with the same named will be replaced. Note that reader_full_text
    is closed once this functions ends.

    :param tweet_score_output_file_name: string for the name of the file for the processed data to be written into
    :param reader_full_text: opened file of the file for containing tweets' fulltext data, note that the first line is
    skipped in this function because it is assumed that the first line contains only field data for the opened file
    :param lexicon_array: list containing processed data of the Emolex lexicon
    :param hash_table_lex: dictionary created using lexicon_array, containing key-value pair of the form
    of {word:index number for the word in read lexicon_array}
    :return: None
    """
    tweet_word_array = []

    # open file to write sentiment score
    writing_file = open(tweet_score_output_file_name, "w+", encoding='utf-8')

    previous_line_data = []

    # skip the first line because it contains fields data, not the tweet data we want
    reader_full_text.readline()

    for lines in reader_full_text:
        fields = lines.split(',', 1)

        # for cases where a tweet's full text covers more than 1 line in the csv file, in this case, update score of
        # previous line, or when a tweet continues to a row with 2 fields that is not a new tweet

        if (len(fields) == 1) or (not fields[0].isdigit()):
            tweet_word_array = preprocess_tweet_text_for_analysis(fields[0])
            calculated_sentiment_score = word_sentiment_calculation(tweet_word_array, lexicon_array, hash_table_lex)

            previous_line_tweet_id = previous_line_data[0]
            previous_sentiment_score = previous_line_data[1]
            new_updated_score = sum_score(previous_sentiment_score,calculated_sentiment_score)

            writing_file = update_previous_line_sentiment_score(new_updated_score, previous_line_tweet_id, last_line_file_position, writing_file)

            previous_line_data[1] = new_updated_score
            continue

        # for handling rows with less than 2 fields, all rows should have 2 rows
        if len(fields) != 2:
            continue

        tweet_word_array = preprocess_tweet_text_for_analysis(fields[1])
        calculated_sentiment_score = word_sentiment_calculation(tweet_word_array, lexicon_array, hash_table_lex)
        tweet_sentiment_score_data = ([fields[0],calculated_sentiment_score])

        last_line_file_position = writing_file.tell()
        writing_file.write(str(tweet_sentiment_score_data) + "\n")

        previous_line_data = tweet_sentiment_score_data
    reader_full_text.close()
    return


def sum_score(previous_sentiment_score,calculated_sentiment_score):
    """
    
    :param previous_sentiment_score: first list of integer scores to be summed, of n length.
    :param calculated_sentiment_score: second list of integer scores to be summed, of n length.
    :return: list of summed score, of n length. The summing is the sum of k-th integer of booth list, where k-th starts
    from 0-th to n-th.
    """
    # sum scores in two arrays
    new_updated_score = []
    index = 0
    for score in previous_sentiment_score:
        new_updated_score += [score+calculated_sentiment_score[index]]
        index += 1
    return new_updated_score


def update_previous_line_sentiment_score(new_updated_score, previous_line_tweet_id, last_line_file_position, writing_file):
    """
    Update the tweet id sentiment score of the last tweet in writing_file by deleting the last line in writing_file and
    then adding a new line containing [previous_line_tweet_id, new_updated_score].

    :param new_updated_score: list containing the sentiment score to be added to the file
    :param previous_line_tweet_id: string of tweet id of tweet to be added into writing_file.
    :param last_line_file_position: the position of the beginning of the last line in writing_file. This can be usually
    obtained using writing_file.tell() before writing a new line into writing_file
    :param writing_file: the opened file for deletion of line and adding of new line of data
    :return: the opened file for deletion of line and adding of new line of data
    """

    # move pointer to beginning of previous line to delete the line by truncating at the pointer
    writing_file.seek(last_line_file_position)
    writing_file.truncate()

    # write the new updated sentiment score to the file
    writing_file.write(str([previous_line_tweet_id, new_updated_score]) + "\n")
    return writing_file


def load_timedata(time_data_file_name):
    """

    :param time_data_file_name: string of name for the file containing time data for the Tweets
    :return: list of size 2, containing [csvreader for the file containing time data for the Tweets, time stamp of
    the tweet in the file's first line
    """
    time_file = open(time_data_file_name, 'r',  encoding='utf-8')
    csv_reader_time_data = csv.reader(time_file)

    # skip first line its csv because the line contains only row header
    next(csv_reader_time_data, None)

    for row in csv_reader_time_data:
        first_row_time_data = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(row[1],'%a %b %d %H:%M:%S +0000 %Y'))
        first_tweet_time_stamp_data = dt.datetime.strptime(first_row_time_data, '%Y-%m-%d %H:%M:%S')
        break
    # move csvreader pointer to its first row
    time_file.seek(0)
    next(csv_reader_time_data, None)

    return [csv_reader_time_data, first_tweet_time_stamp_data]


def calculate_elapsed_time_and_write_to_file(tweet_time_output_data, csv_reader_time_data, first_tweet_time_data):
    """
    Process and prepare time data file for graphing tweet sentiment scores against time. The time data file is set
    to write into a file named tweet_time_output_data, so any file of the same name will be erased before writing.

    :param tweet_time_output_data: string for the name of the file for the processed data to be written into
    :param csv_reader_time_data: csvreader of the file containing time data for the Tweets
    :param first_tweet_time_data: time stamp of the tweet in the file's first line
    :return: None
    """
    # open file to write sentiment score
    writing_file = open(tweet_time_output_data, "w+",  encoding='utf-8')
    # empty file before writing
    writing_file.truncate()

    for row in csv_reader_time_data:

        # convert relevant row data into timestamp
        tweet_time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(row[1],'%a %b %d %H:%M:%S +0000 %Y'))
        tweet_time_stamp = dt.datetime.strptime(tweet_time_stamp, '%Y-%m-%d %H:%M:%S')

        if tweet_time_stamp < first_tweet_time_data:
            elapsed_time_in_hours = 0
        else:
            elapsed_time_in_hours = calculate_elapsed_time_in_hours(tweet_time_stamp, first_tweet_time_data)
        tweet_elapsed_timedata = [row[0], elapsed_time_in_hours]

        writing_file.write(str(tweet_elapsed_timedata) + "\n")

    writing_file.close()
    return


def calculate_elapsed_time_in_hours(tweet_time_stamp, first_tweet_time_data):
    """

    :param tweet_time_stamp: time stamp of tweet's creation time
    :param first_tweet_time_data: time stamp of first tweet's creation time
    :return: Elapsed hours in integer of tweet's creation time since the first tweet, the returned hour is rounded down.
    """
    time_difference = tweet_time_stamp - first_tweet_time_data
    return (time_difference.days * 24) + (time_difference.seconds // 3600 )


def generate_time_to_sentiment_score_dictionary(score_file, time_file):
    """

    :param score_file: string for the file name of the file containing the tweet's id_str and its respective array of 
    sentiment scores, with the same number of lines as time_file
    :param time_file: string for the file name of the file containing the tweet's id_str and its respective time elapse 
    from the first tweet, with the same number of lines as time_file
    :return: dictionary in the form of {integer hours elapsed since the first tweet: the list of sum of all tweet's 
    sentiment score for the integer hour appended by the number of tweeets for this hour}. Note that the value part
    of the dictionary's key value pair is an array of length 10 + 1, where each score, 10 scores in total,
    corresponds to the score in the order of ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative',
    'positive', 'sadness', 'surprise', 'trust'] + [number of tweets for this hour].
    """

    processed_sentiment_score_file = open(score_file, 'r',  encoding='utf-8')
    processed_time_file = open(time_file, 'r', encoding='utf-8')

    time_to_score_dictionary = {}

    for sentiment_score_line in processed_sentiment_score_file:
        # set the second field of the file, which is the time elapsed in hours, to corresponding_time
        corresponding_time = processed_time_file.readline().split(',', 1)
        corresponding_time = int((corresponding_time[1]).replace(']', '').strip())

        # set the second field of the file, which is the list of sentiment scores, to corresponding_score
        corresponding_score = sentiment_score_line.split(',', 1)
        corresponding_score = corresponding_score[1].replace(']]', ']').strip()
        corresponding_score = literal_eval(corresponding_score)

        score_for_this_hour_time = time_to_score_dictionary.get(corresponding_time) 

        # if the elapsd time is not recorded in the dictionary, record it along with its corresponding score
        if score_for_this_hour_time == None:
            time_to_score_dictionary[corresponding_time] = (corresponding_score + [1])
        # otherwise, update the matched time's corresponding_score
        else:
            time_to_score_dictionary[corresponding_time] = sum_score((corresponding_score + [1]), score_for_this_hour_time)

    return time_to_score_dictionary


def plot_graph_with_time_and_sentiment_dictionary(time_to_sentiment_dictionary):
    """
    Plot two graphs, first graph is a graph of      total Tweets' sentiment scores against time, the second is a graph
    of average Tweets' sentiment scores against time

    :param time_to_sentiment_dictionary: the dictionary with key-pair in the form of {time elapsed in hour: list, of
    size 11, containing the 10 sentiment appended by 1 value for the number of tweets in the hour}
    :return: None
    """
    plot_hours = []
    plot_scores = []
    list_of_number_of_tweets_for_the_hour = []

    # there are 10 type of sentiment sccore for each tweet
    for k in range(10):
        plot_scores.append([])

    for dkey, dvalue in time_to_sentiment_dictionary.items():
        plot_hours.append(dkey)
        list_of_number_of_tweets_for_the_hour.append(dvalue[len(dvalue) - 1])
        index = 0
        for dsentiment_value in dvalue[:-1]:
            plot_scores[index].append(dsentiment_value)
            index += 1

    # plot graph of total sentiment score against time
    graph_one = plt.figure(1)
    for k in range(10):
        plt.plot(plot_hours, plot_scores[k])
    plt.title("Total Tweets' sentiment scores over time")
    plt.xlabel('Hours elapsed since first Tweet')
    plt.ylabel('Sentiment score')
    plt.legend(['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise',
                'trust'], loc = 'upper left', prop={'size': 6})

    plt.show()

    # plot graph of average sentiment score per tweet against time
    graph_two = plt.figure(2)
    average_sentiment_score_per_tweet = []

    avg_index = -1
    for summed_score in plot_scores:
        average_sentiment_score_per_tweet.append([])
        avg_index += 1
        for k in summed_score:
            average_sentiment_score_per_tweet[avg_index].append(k/list_of_number_of_tweets_for_the_hour[avg_index])

    for k in range(10):
        plt.plot(plot_hours, average_sentiment_score_per_tweet[k])
    plt.title("Average Tweet sentiment scores over time")
    plt.xlabel('Hours elapsed since first Tweet')
    plt.ylabel('Sentiment score')
    plt.legend(['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise',
                'trust'], loc = 'upper left', prop={'size': 6})

    plt.show()

    return

def categorization_histogram(score_file):
    """
    Categorize each tweet based on their maximum sentiment score, if the max score is 0, it is categorized as neutral,
    otherwise if there are one or more sentiment values that matches the maximum score, the tweet is categorized
    based on the one or more categorized values. This means that a tweet will be categorized as neutral if its max
    score is 0 and can have 1 or more categorization otherwise because there can be more than 1 sentiment score
    type that matches the max score. The categorized data are then visualised onto a histogram.

    :param score_file: string for the file name of the file containing the tweet's id_str and its respective array of
    sentiment scores
    :return: None
    """

    tweet_scores = open(score_file, 'r',  encoding='utf-8')

    # sentiment type reference for list_for_categorization: [anger, anticipation, disgust, fear, joy, negative,
    # positive, sadness, surprise, trust, neutral]
    list_for_categorization = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for score_line in tweet_scores:

        # set the second field of the file, which is the list of sentiment scores, to corresponding_score
        corresponding_score = score_line.split(',', 1)
        corresponding_score = corresponding_score[1].replace(']]', ']').strip()
        corresponding_score = literal_eval(corresponding_score)

        highest_score = max(corresponding_score)

        # if max score is 0, categorize as neutral
        if highest_score == 0:
            list_for_categorization[10] += 1
            continue

        # if the max score is not 0, categorize the tweet based on the sentiment value type that matches the highest
        # score. Note that more than 1 score type can match so the tweet can have more than 1 categorization in
        # this case
        score_index = 0
        for sentiment_score in corresponding_score:
            if sentiment_score == highest_score:
                list_for_categorization[score_index] += 1
            score_index += 1

    # plot the histogram
    plt.bar(['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise',
             'trust', 'neutral'], height=list_for_categorization)
    plt.xticks(rotation=90)
    plt.xlabel('Sentiment Type')
    plt.ylabel('Number of tweets')
    plt.title('Categorized Tweets')
    plt.show()
    return


if __name__ == "__main__":

    print('_______________________START______________________________________________________    ')

    tweet_score_output_file_name = "writtenfile001.txt"
    tweet_time_output_file_name = 'timewrittenfile001.txt'
    full_text_data_file_name = "irma_fulltext.csv"
    tweet_id_created_at_file_name = "irma_idstr_createdat.csv"
    lexicon_file_name = 'lexicon.txt'

    lexicon_array = read_lexicon(lexicon_file_name)
    hash_table_lex = create_dictionary(lexicon_array)

    print('________________________FINISHED PROCESSING LEXICON_________________________________________________    ')

    reader_full_text = open(full_text_data_file_name, 'r', encoding='utf-8')

    print('||||||prrocessing and writing|||||||||')

    # create and initialise empty output for writing and reading, if it already exists, the file is emptied
    writing_file = open(tweet_score_output_file_name, "w",  encoding='utf-8')
    writing_file.close()
    process_and_write_to_file(tweet_score_output_file_name, reader_full_text, lexicon_array, hash_table_lex)

    print('|||||||||||||||||||FINISHED GENERATING AND WRITING TWEET SCORES|||||||||')

    csv_reader_time_data = load_timedata(tweet_id_created_at_file_name)
    csvreadertime = csv_reader_time_data[0]
    first_tweet_time_stamp_data = csv_reader_time_data[1]
    calculate_elapsed_time_and_write_to_file(tweet_time_output_file_name, csvreadertime, first_tweet_time_stamp_data)

    print('|||||||||||||||||||FINISHED PROCESSING TIME FILE|||||||||')

    time_to_sentiment_dictionary = generate_time_to_sentiment_score_dictionary(tweet_score_output_file_name, tweet_time_output_file_name)
    plot_graph_with_time_and_sentiment_dictionary(time_to_sentiment_dictionary)

    print('|||||||||||||||||||FINISHED GENERATING TIME TO SCORE GRAPH|||||||||')

    categorization_histogram(tweet_score_output_file_name)

    print('|||||||||||||||||||PROGRAM END|||||||||')



#NOTE:
# the id_created and fulltext csv files need to have its last line as empty or this program may throw an error.
# data in each array in lexicon_array is:
#  [word followed by 1st to 10th sentiment in this order]:
#  [word, anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust]
# the sentiment analysis only analyse rows with 2 fields, there are at least 1 row with less than 2 field in both csv
#  for Harvey and Irma, and some rows has 3 fields
# note that it may not be the same for data regarding tweet's created time, as the tweet time data may all have 2 fields
#  so all field for time data are processed, unlike fulltext data where some row have less than 2 fields and are skipped
# the first tweet in both fulltext.csv and id_str_created_at.csv will be used to graph tweets, any tweets later
#  with the file that is created before the tweet will has 0 scored for time elapsed in hours. (Example: first
#  tweet is created at 3pm, any tweet read after the first tweet rom the file that is created before 3pm on the
#  same day and year will have 0 scored as time elapsed in hours.) Because of this, we recommend sorting the tweets
#  by time before using this program to perform sentiment analysis on it.
# this program needs matplotlib installed in python for it to run and do graphing
# this program does not analyse emoticon for sentiments, but if desired, it can be added later by adding sentiment
#  scores into the emolex and modify the preprocess_tweet_text_for_analysis to tokenize emoticons too


#todo:
# do we need to add preconditions and postcondtions when we have already documented params, returns and function description?
# Everything works and are documented and tested. If theres something to do, its probably cleaning code for better
#  look since its messy. The coding can also be edited to be more efficient.






