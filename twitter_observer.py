import sys
import readFilecsv as rf 
import build_tree as bt 
import wordEmbeddings as we 
import mysql.connector
import os
import ntpath

if __name__=="__main__":
    cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='twitter')
    cursor = cnx.cursor()
    if sys.argv[1] == "parse-json":
        if os.path.isfile(sys.argv[2]):
            rf.readFileCsv(sys.argv[2],sys.argv[3])
        else:
            print("Cannot find",sys.argv[2],"\n Usage: parse-json infile outfile")
    
    elif sys.argv[1] == "insert-db":
        if os.path.isfile(sys.argv[2]):
            rf.insertDb(cursor,sys.argv[2])
        else:
            print("Cannot find",sys.argv[2],"\n Usage: insert-db infile ")

    elif sys.argv[1] == "build-tree":
        if sys.argv[2]!="":
            bt.buildTree(cursor,sys.argv[2])
        else:
            print("ERROR: Usage: python build-tree tablename")