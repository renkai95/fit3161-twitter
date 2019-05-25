import csv
import pprint
import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys


def traverse(g,node,tweet_ids):
    '''
    Recursive traversal of a python reply tree dict
    :param g: networkx graph object
    :param node: Current node name
    :param tweet_ids: dict of twitter id_str
    Returns: Nothing
    Side effects: Adds node to graph if there exists a reply, calls itself recursively if there is a child node
    
    '''
    try:
        node['id_children']
    except KeyError:
        return
    for child in node['id_children']:
        g.add_node(tweet_ids[child['id']])
        g.add_node(tweet_ids[node['id']])
        g.add_edge(tweet_ids[child['id']],tweet_ids[node['id']])
        traverse(g,child,tweet_ids)


def readFile(idFile,replyFile):
    '''
    Reads file, splits results into dicts
    returns: dict of tweet ids, dict of all reply ids, list of tuples of reply ids
    '''
    tweet_ids={}
    replied_inlist={}
    replied_to=[]
    with open(idFile,encoding='utf-8') as inputFile:
        for row in inputFile:
            tweet_ids[row.rstrip()]=row.rstrip()
        f = open(replyFile,encoding='utf-8')
        next(f)
        for row in f:
            temp=row.split(',')
            try:
                tweet_ids[temp[1].rstrip()]
                replied_to.append((temp[0].rstrip(),temp[1].rstrip()))
                replied_inlist[temp[0].rstrip()]=temp[1].rstrip()
                tweet_ids[temp[0].rstrip()]=temp[2].rstrip()
                tweet_ids[temp[1].rstrip()]=temp[3].rstrip()
            except KeyError:
                pass    
        f.close()
    return tweet_ids,replied_inlist,replied_to
def makeQuery(cursor):
    tweet_ids={}
    replied_inlist={}
    replied_to=[]
    cursor.execute("select id_str from twitter.harvey_cleaned;")
    myresult = cursor.fetchall()
    for k in myresult:
        tweet_ids[str(k[0])]=str(k[0])
    cursor.execute("select id_str,in_reply_to_status_id_str,user_name,in_reply_to_screen_name,user_followers_count from twitter.harvey_cleaned where in_reply_to_status_id_str != '';")
    myresult = cursor.fetchall()
    for row in myresult:
        try:
            
            tweet_ids[row[1]]
            replied_to.append((str(row[0]),row[1]))
            replied_inlist[str(row[0])]=row[1]
            tweet_ids[str(row[0])]=row[2]
            tweet_ids[row[1]]=row[3]
        except KeyError:
            pass
    return tweet_ids,replied_inlist,replied_to
def trimTerminators(replied_to,replied_inlist):
    '''
    If replied to tweet exists outside of the dataset, we terminate them by having the edge to the same node
    :param replied_to: List of edges between 2 users
    :param replied_inlist: Dict of all ids of users that replied
    :return replied_to: List of tuples representing edges.
    '''
    for row in range(len(replied_to)):
        x,y = replied_to[row]
        try:
            replied_inlist[y]
        except KeyError:
            replied_to.append((y,y))    
    #return replied_to

def buildReplyTree(replied_to,tweet_ids):
    '''
    Builds a list of dicts which represents reply trees
    :param replied_to: list of tuples representing edges in the reply tree
    :param tweet_ids: List of all tweet ids
    :return forest: List of all reply trees
    '''

    nodes = {}
    for i in tweet_ids:
        nodes[i] = { 'id': i }
    forest = []
    for i in replied_to:
        id, parent_id = i
        
        node = nodes[id]
        if id == parent_id:
            forest.append(node)
        else:
            parent = nodes[parent_id]
            if not 'id_children' in parent:
                parent['id_children'] = []
            children = parent['id_children']
            children.append(node)
    for row in forest:
        try:
            row["id_children"]
        except KeyError:
            forest.remove(row)
    forest.sort(key=lambda x:len(x["id_children"]),reverse=1)
    forest = list({v['id']:v for v in forest}.values())
    print(len(forest))
    print(forest.count(forest[0]))
    return forest

def createLog(forest):
    '''
    Prints the forest as a log file
    :param forest: List of dicts of reply trees
    '''
    with open('../DATA/logfile.txt','w') as logFile:
        for row in forest:
            if len(row)>1:
                pprint.pprint(row, logFile)
                


def plotGraphs(forest,tweet_ids):
    '''
    Plots all graphs in the forest.
    :param forest: List of reply trees
    :param tweet_ids: Dict of all tweet ids
    '''
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 6
    fig_size[1] = 6
    plt.rcParams["figure.figsize"] = fig_size
    font = {'family' : 'normal',
            'size'   : 1}

    plt.rc('font', **font)
    for row in range(len(forest)) :
        test = 1
        #print(row)
        g = nx.Graph()
        traverse(g,forest[row],tweet_ids)

        d=dict(g.degree)
        nx.draw_networkx(g, pos = nx.fruchterman_reingold_layout(g),node_size=[v * 2 for v in d.values()],font_size=1,width =0.08)
        plt.savefig('../DATA/graph'+str(row)+'.png' ,dpi = 1200)
        print(row)
        g.clear()
        plt.clf()



if __name__ == "__main__":
    '''
    Usage: python build-tree.py <path to file of ids> <path to file of replies>
    Original location: '../DATA/harvey_ids.csv'  '../DATA/harvey_replies.csv'


    '''
    try:
        idFile = sys.argv[1]
        replyFile = sys.argv[2]
        tweet_ids,replied_inlist,replied_to=readFile(idFile,replyFile)
    except IndexError:
        cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='twitter')

        cursor = cnx.cursor()
        tweet_ids,replied_inlist,replied_to=makeQuery(cursor)
    #cursor.execute("SELECT * FROM harvey_cleaned")
    #myresult = cursor.fetchone()
    #print(myresult)
    
    trimTerminators(replied_to,replied_inlist)
    forest = buildReplyTree(replied_to,tweet_ids)
    plotGraphs(forest,tweet_ids)
    cnx.close()