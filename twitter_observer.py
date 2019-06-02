import sys
import readFilecsv as rf 
import build_tree as bt 
import wordEmbeddings as we 
import mysql.connector
import os
import ntpath
import twitter_obs_test as obsTest

if __name__=="__main__":
    
    cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='twitter')
    cursor = cnx.cursor()
    if len(sys.argv)<2:
        print("""
        Unknown command
        commands: 
        ----parse-json infile outfile
        ----insert-db infile
        ----build-tree tablename or build-tree tablename noOfGraphs
        ----wordEmbed tablename
        """)
    elif sys.argv[1] == "parse-json":
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
        #print(int(sys.argv[3]))
        if len(sys.argv)==4:
            
            bt.buildTree(cursor,sys.argv[2],int(sys.argv[3]))
        elif len(sys.argv)==3:
            bt.buildTree(cursor,sys.argv[2])
        else:
            print("ERROR: Usage: build-tree tablename or build-tree tablename noOfGraphs")
    elif sys.argv[1] == "wordEmbed":
        x = input("\nEnter a comma separated list of words: ")
        if len(sys.argv)== 3 and x!="":
            we.wordEmbed(cursor,x.split(','),sys.argv[2])
        else:
            if x=="":
                print("Error: input cannot be empty")
            print("Error: usage: wordEmbed tablename")
    else:
        print("""
        Unknown command
        commands: 
        ----parse-json infile outfile
        ----insert-db infile
        ----build-tree tablename or build-tree tablename noOfGraphs
        ----wordEmbed tablename
        """)