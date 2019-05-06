import csv
import pprint
import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def traverse(g,node,harvey_id):
    #g.add_node(node['id'])
    try:
        node['id_children']
    except KeyError:
        return
    for child in node['id_children']:
        g.add_node(harvey_id[child['id']])
        g.add_node(harvey_id[node['id']])
        g.add_edge(harvey_id[child['id']],harvey_id[node['id']])
        traverse(g,child,harvey_id)
#def nodeCount(node):
#    try:
        
cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='twitter')
cursor = cnx.cursor()
harvey_id={}
replied_to=[]
replied_to_id=[]
replied_inlist={}
tree= []

font = {'family' : 'normal',
        'size'   : 1}

plt.rc('font', **font)
with open('../DATA/harvey_ids.csv') as inputFile:
    for row in inputFile:
        harvey_id[row.rstrip()]=row.rstrip()
    f = open('../DATA/harvey_replies.csv')
    next(f)
    for row in f:
        temp=row.split(',')
        try:
            harvey_id[temp[1].rstrip()]
            replied_to.append((temp[0].rstrip(),temp[1].rstrip()))
            replied_inlist[temp[0].rstrip()]=temp[1].rstrip()
            harvey_id[temp[0].rstrip()]=temp[2].rstrip()
            harvey_id[temp[1].rstrip()]=temp[3].rstrip()
        except KeyError:
            pass
        
    f.close()
for row in range(len(replied_to)):
    x,y = replied_to[row]
    try:
        replied_inlist[y]
    except KeyError:
        replied_to.append((y,y))
    
#print(replied_to)
nodes = {}
for i in harvey_id:
    #print(i)
    nodes[i] = { 'id': i }
#print(nodes)
# pass 2: create trees and parent-child relations
forest = []
for i in replied_to:
    #print(forest)
    id, parent_id = i
    node = nodes[id]
    #print(node)
    # either make the node a new tree or link it to its parent
    if id == parent_id:
        # start a new tree in the forest
        forest.append(node)
    else:
        # add new_node as child to parent
        parent = nodes[parent_id]
        if not 'id_children' in parent:
            # ensure parent has a 'children' field
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
'''
with open('../DATA/logfile.txt','w') as logFile:
    for row in forest:
        if len(row)>1:
            pprint.pprint(row, logFile)
            

'''
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 6
fig_size[1] = 6
plt.rcParams["figure.figsize"] = fig_size

for row in range(len(forest)) :
    test = 1
    #print(row)
    g = nx.Graph()
    traverse(g,forest[row],harvey_id)
    #print(g)
    '''
    while test == 1:
        try:
            forest[row]['id_children']
        except KeyError:
            test = 0
        g.add_node(harvey_id[forest[row]['id']])
        for child in forest[row]['id_children']:
            g.add_node(harvey_id[child['id']])
            g.add_edge(harvey_id[forest[row]['id']],harvey_id[child['id']])
        test=0
    '''
    d=dict(g.degree)
    nx.draw_networkx(g, pos = nx.fruchterman_reingold_layout(g),node_size=[v * 6 for v in d.values()],font_size=1,width =0.08)
    plt.savefig('../DATA/graph'+str(row)+'.png' ,dpi = 1200)
    print(row)
    g.clear()
    plt.clf()

cnx.close()

