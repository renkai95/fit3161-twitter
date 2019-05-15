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


def makeQuery(cursor):
    cursor.execute("SELECT full_text FROM harvey_cleaned")
    myresult = cursor.fetchone()
    print(myresult)
if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='twitter')

    cursor = cnx.cursor()
    makeQuery(cursor)




    cnx.close()