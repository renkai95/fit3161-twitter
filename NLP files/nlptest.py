import nlp_analysis_v1
import time
import datetime as dt


def test_read_lexicon():

    try:
        lexicon_array = nlp_analysis_v1.read_lexicon('testlexicon.txt')
        if lexicon_array != [['abbot', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], ['abbreviate', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['abbreviation', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['purify', '0', '0', '0', '1', '0', '1', '0', '0', '1']]:
            raise()
        print('read_lexicon() works as intended.')
    except:
        print('Error occurred in testing read_lexicon().')
    return


def test_create_dictionary():

    try:
        lexicon_array = nlp_analysis_v1.read_lexicon('testlexicon.txt')
        hash_table_lex = nlp_analysis_v1.create_dictionary(lexicon_array)

        if hash_table_lex != {'abbot': 0, 'abbreviate': 1, 'abbreviation': 2, 'purify': 3}:
            raise()
        print('create_dictionary() works as intended.')
    except:
        print('Error occurred in testing create_dictionary().')
    return


def test_match_to_hash_table():
    try:

        lexicon_array = nlp_analysis_v1.read_lexicon('testlexicon.txt')
        hash_table_lex = nlp_analysis_v1.create_dictionary(lexicon_array)
        if nlp_analysis_v1.match_to_hash_table('abbot', lexicon_array, hash_table_lex) != ['abbot', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0']:
            raise()
        if nlp_analysis_v1.match_to_hash_table('abbreviate', lexicon_array, hash_table_lex) != ['abbreviate', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']:
            raise()
        if nlp_analysis_v1.match_to_hash_table('thiswordisnotinthelexicon', lexicon_array, hash_table_lex) != None:
            raise()
        print('match_to_hash_table() works as intended.')
    except:
        print('Error occurred in testing match_to_hash_table().')
    return


def test_word_sentiment_calculation():
    try:

        lexicon_array = nlp_analysis_v1.read_lexicon('testlexicon.txt')
        hash_table_lex = nlp_analysis_v1.create_dictionary(lexicon_array)
        if nlp_analysis_v1.word_sentiment_calculation(['a','abbot','abbreviate','abbot','ok', 'purify'], lexicon_array, hash_table_lex) != [0, 0, 0, 1, 0, 1, 0, 0, 3, 0]:
            raise()
        print('word_sentiment_calculation() works as intended.')
    except:
        print('Error occurred in testing word_sentiment_calculation().')
    return



def test_update_scores():
    try:

        if nlp_analysis_v1.update_scores([1, 0, 23, 0, 0, 0, 0, 0, 2, 0], ['abbot', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0']) != [1, 0, 23, 0, 0, 0, 0, 0, 3, 0]:
            raise()
        print('update_scores() works as intended.')
    except:
        print('Error occurred in testing update_scores().')
    return




def test_preprocess_tweet_text_for_analysis():
    try:
        if nlp_analysis_v1.preprocess_tweet_text_for_analysis('@testt, Tweet: Hurricane Irma looks like fun <3 XD ') !=  ['testt', 'tweet', 'hurricane', 'irma', 'looks', 'like', 'fun','xd']:
            raise()
        print('preprocess_tweet_text_for_analysis() works as intended.')
    except:
        print('Error occurred in testing preprocess_tweet_text_for_analysis().')
    return


def test_process_and_write_to_file():
    try:

        lexicon_array = nlp_analysis_v1.read_lexicon('testlexicon.txt')
        hash_table_lex = nlp_analysis_v1.create_dictionary(lexicon_array)
        reader_full_text = open('testtweets.csv')
        test_write_file = 'testwrittenfile.txt'
        nlp_analysis_v1.process_and_write_to_file(test_write_file,reader_full_text,lexicon_array,hash_table_lex)
        sstring = ''
        opened_read_file = open(test_write_file)
        for k in opened_read_file:
            sstring += k.strip()

        if sstring !=  "['901102323925176321', [0, 0, 0, 2, 0, 2, 0, 0, 3, 0]]['901102307902967808', [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]['901102320708145153', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]['901102328828354560', [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]['901102310453108736', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]":
            raise()
        print('process_and_write_to_file() works as intended.')
    except:
        print('Error occurred in testing process_and_write_to_file().')
    return

def test_sum_score():
    try:
        if nlp_analysis_v1.sum_score([0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 2, 0, 2, 0, 0, 3, 0]) !=  [0, 0, 0, 2, 0, 2, 0, 0, 4, 0]:
            raise()
        print('sum_score() works as intended.')
    except:
        print('Error occurred in testing sum_score().')
    return


def test_update_previous_line_sentiment_score():
    try:


        lexicon_array = nlp_analysis_v1.read_lexicon('testlexicon.txt')
        hash_table_lex = nlp_analysis_v1.create_dictionary(lexicon_array)
        reader_full_text = open('testtweets.csv')
        test_write_file = 'testwrittenfile.txt'
        writing_file = open(test_write_file, 'w')
        nlp_analysis_v1.process_and_write_to_file(test_write_file,reader_full_text,lexicon_array,hash_table_lex)
        nlp_analysis_v1.update_previous_line_sentiment_score([0, 0, 0, 99, 0, 108, 0, 77, 0, 0], 901102310453108736, 224, writing_file)
        writing_file.close()
        opened_read_file = open(test_write_file)
        sstring = ''
        for k in opened_read_file:
            sstring += k.strip()

        if sstring != "['901102323925176321', [0, 0, 0, 2, 0, 2, 0, 0, 3, 0]]['901102307902967808', [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]['901102320708145153', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]['901102328828354560', [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]][901102310453108736, [0, 0, 0, 99, 0, 108, 0, 77, 0, 0]]":
            raise()
        print('update_previous_line_sentiment_score() works as intended.')
    except:
        print('Error occurred in testing update_previous_line_sentiment_score().')
    return

def test_load_timedata():
    try:

        test_time_file = 'testtime.csv'
        result = nlp_analysis_v1.load_timedata(test_time_file)
        if str(result[1]) != '2017-08-25 15:21:50':
            raise()
        if str(result[0].__next__()) != "['901102323925176321', 'Fri Aug 25 15:21:50 +0000 2017']":
            raise()
        print('load_timedata() works as intended.')
    except:
        print('Error occurred in testing load_timedata().')
    return



def test_calculate_elapsed_time_and_write_to_file():
    try:
        test_time_file = 'testtime.csv'
        result = nlp_analysis_v1.load_timedata(test_time_file)
        tweet_time_output_data = 'testtimewrittenfile.txt'
        nlp_analysis_v1.calculate_elapsed_time_and_write_to_file(tweet_time_output_data, result[0], result[1])
        open_time_file = open(tweet_time_output_data)
        sstring = ''
        for k in open_time_file:
            sstring += k.strip()

        if sstring !=  "['901102323925176321', 0]['901102307902967808', 3]['901102320708145153', 3]['901102328828354560', 6]['901102310453108736', 7]":
            raise()
        print('calculate_elapsed_time_and_write_to_file() works as intended.')
    except:
        print('Error occurred in testing calculate_elapsed_time_and_write_to_file().')
    return


def test_calculate_elapsed_time_in_hours():
    try:

        earlier_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Fri Aug 25 19:21:46 +0000 2017", '%a %b %d %H:%M:%S +0000 %Y'))
        earlier_time = dt.datetime.strptime(earlier_time, '%Y-%m-%d %H:%M:%S')
        latertime = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("Fri Aug 25 23:21:47 +0000 2017", '%a %b %d %H:%M:%S +0000 %Y'))
        latertime = dt.datetime.strptime(latertime, '%Y-%m-%d %H:%M:%S')
        if nlp_analysis_v1.calculate_elapsed_time_in_hours(latertime, earlier_time) != 4:
            raise()
        print('calculate_elapsed_time_in_hours() works as intended.')
    except:
        print('Error occurred in testing calculate_elapsed_time_in_hours().')
    return



def test_generate_time_to_sentiment_score_dictionary():
    lexicon_array = nlp_analysis_v1.read_lexicon('testlexicon.txt')
    hash_table_lex = nlp_analysis_v1.create_dictionary(lexicon_array)
    reader_full_text = open('testtweets.csv')
    test_write_file = 'testwrittenfile.txt'
    nlp_analysis_v1.process_and_write_to_file(test_write_file, reader_full_text, lexicon_array, hash_table_lex)

    test_time_file = 'testtime.csv'
    result = nlp_analysis_v1.load_timedata(test_time_file)
    tweet_time_output_data = 'testtimewrittenfile.txt'
    nlp_analysis_v1.calculate_elapsed_time_and_write_to_file(tweet_time_output_data, result[0], result[1])

    if nlp_analysis_v1.generate_time_to_sentiment_score_dictionary(test_write_file, tweet_time_output_data) != {
        0: [0, 0, 0, 2, 0, 2, 0, 0, 3, 0, 1], 3: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2],
        6: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}:
        raise ()
    try:
        lexicon_array = nlp_analysis_v1.read_lexicon('testlexicon.txt')
        hash_table_lex = nlp_analysis_v1.create_dictionary(lexicon_array)
        reader_full_text = open('testtweets.csv')
        test_write_file = 'testwrittenfile.txt'
        nlp_analysis_v1.process_and_write_to_file(test_write_file, reader_full_text, lexicon_array, hash_table_lex)

        test_time_file = 'testtime.csv'
        result = nlp_analysis_v1.load_timedata(test_time_file)
        tweet_time_output_data = 'testtimewrittenfile.txt'
        nlp_analysis_v1.calculate_elapsed_time_and_write_to_file(tweet_time_output_data, result[0], result[1])

        if nlp_analysis_v1.generate_time_to_sentiment_score_dictionary(test_write_file, tweet_time_output_data) !=  {0: [0, 0, 0, 2, 0, 2, 0, 0, 3, 0, 1], 3: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2], 6: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}:
            raise()
        print('generate_time_to_sentiment_score_dictionary() works as intended.')
    except:
        print('Error occurred in testing generate_time_to_sentiment_score_dictionary().')
    return



if __name__ == '__main__':


    print('this python file tests all functions in nlp_analysis_v1')
    print('__________________test starting')
    test_read_lexicon()
    test_create_dictionary()
    test_match_to_hash_table()
    test_word_sentiment_calculation()
    test_update_scores()
    test_preprocess_tweet_text_for_analysis()
    test_process_and_write_to_file()
    test_sum_score()
    test_update_previous_line_sentiment_score()
    test_load_timedata()
    test_calculate_elapsed_time_and_write_to_file()
    test_calculate_elapsed_time_in_hours()
    test_generate_time_to_sentiment_score_dictionary()
    print('__________________test ending')