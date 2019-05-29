import csv
import pprint

import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import os
import sys
import re
import string
import gensim
import gensim.test.utils
import gensim.models
import mysql.connector
def makeQuery(cursor,sentences,table="harvey_cleaned"):
    cursor.execute("SELECT full_text FROM "+table)
    myresult = cursor.fetchall()
    for k in myresult:
        x= k
        x = re.sub('['+string.punctuation+']', '', str(x)).lower().split() 
        sentences.append(x)
        #print(x)
def wordEmbed(cursor,words,tableName):
	sentences = []
	makeQuery(cursor,sentences,tableName)
	print("Query Done")
	model = gensim.models.Word2Vec(sentences, size=100, window=3, min_count=2, workers=8)
	#print(model)
	#model.save('model.bin')
    #load model
	#new_model = gensim.models.Word2Vec.load('model.bin')
	#print(new_model)
	print(model.wv.most_similar(positive=words))
	for k in range(10):
		print(model.wv.index2word[k])
    #print(new_model.wv.most_similar(positive=['no']))
if __name__ == "__main__":
	
	cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='twitter')

	cursor = cnx.cursor()
	sentences = []
	makeQuery(cursor,sentences)
	print("Done")
	model = gensim.models.Word2Vec(sentences, size=100, window=3, min_count=2, workers=8)
	print(model)
	model.save('model.bin')
    #load model
	new_model = gensim.models.Word2Vec.load('model.bin')
	print(new_model)
	print(new_model.wv.most_similar(positive=['afraid','fear','scared','scare']))
	for k in range(10):
		print(new_model.wv.index2word[k])
    #print(new_model.wv.most_similar(positive=['no']))
	cnx.close()