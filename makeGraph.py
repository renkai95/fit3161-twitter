import csv
import pprint
#import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt
harvey_id = []
test = {}
left={}
right={}
leftlist=[]
rightlist=[]
with open('../DATA/harvey_ids.csv') as inputFile:
    for row in inputFile:
        harvey_id.append(row.rstrip())
        test[row.rstrip()]=row.rstrip()
    f = open('../DATA/harvey_replies.csv')
    next(f)
    for row in f:
        temp=row.split(',')
        try:
            test[temp[1].rstrip()]
            left[temp[0].rstrip()]=temp[0].rstrip()
            right[temp[1].rstrip()]=temp[1].rstrip()
            leftlist.append(temp[0].rstrip())
            rightlist.append(temp[0].rstrip())

        except KeyError:
            pass
    
    f.close()
print("graph starting")
g = nx.Graph()
for row in harvey_id:
    try:
        left[row]
        right[row]
    except KeyError:
        g.add_node(row)
print("rows added")
for x in range(len(left)):
    g.add_edge(leftlist[x],rightlist[x])
print("edges added")
nx.draw_networkx(g, pos = nx.shell_layout(g))
nx.draw_networkx_edge_labels(g, pos = nx.shell_layout(g))
plt.show()
