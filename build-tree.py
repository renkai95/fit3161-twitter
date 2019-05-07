import csv
import pprint
import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys


def traverse(g,node,harvey_id):
    '''
    Recursive traversal of a python reply tree dict
    :param g: networkx graph object
    :param node: Current node name
    :param harvey_id: dict of twitter id_str
    Returns: Nothing
    Side effects: Adds node to graph if there exists a reply, calls itself recursively if there is a child node
    
    '''
    try:
        node['id_children']
    except KeyError:
        return
    for child in node['id_children']:
        g.add_node(harvey_id[child['id']])
        g.add_node(harvey_id[node['id']])
        g.add_edge(harvey_id[child['id']],harvey_id[node['id']])
        traverse(g,child,harvey_id)

        
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
nodes = {}
for i in harvey_id:
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

    d=dict(g.degree)
    nx.draw_networkx(g, pos = nx.fruchterman_reingold_layout(g),node_size=[v * 2 for v in d.values()],font_size=1,width =0.08)
    plt.savefig('../DATA/graph'+str(row)+'.png' ,dpi = 1200)
    print(row)
    g.clear()
    plt.clf()

cnx.close()

if __name__ == "__main__":
    '''
    Usage: python build-tree.py <path to file of ids> <path to file of replies>

    '''
    idfile = sys.argv[1]
    replyfile = sys.argv[2]
    
