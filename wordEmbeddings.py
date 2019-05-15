import csv
import pprint
import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import os
import sys
import re
import gensim
import string

def makeQuery(cursor,sentences):
    cursor.execute("SELECT full_text FROM harvey_cleaned")
    myresult = cursor.fetchall()
    for k in myresult:
        x,y = k
        x = re.sub('['+string.punctuation+']', '', x).split() 
        sentences.append(x)
if __name__ == "__main__":
    sentences = []
    cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='twitter')

    cursor = cnx.cursor()
    makeQuery(cursor,sentences)
    



    cnx.close()