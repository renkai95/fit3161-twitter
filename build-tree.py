import csv
import pprint
harvey_id={}
replied_to=[]
replied_to_id=[]
replied_inlist={}
tree= []
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
        except KeyError:
            pass
        
    f.close()
for row in range(len(replied_to)):
    x,y = replied_to[row]
    try:
        replied_inlist[y]
    except KeyError:
        replied_to.append((y,y))
'''
#print(harvey_id)
for k,v in replied_to.items():
    try: 
        harvey_id[v]
        repliesFound+=1
    except KeyError:
        pass
for k,v in replied_to.items():
    tree.append([])

    tree[-1].append(k)
    x= k
    try:
        while replied_to[x] is not None:
            x=replied_to[x]
            if len(x)>0:
                tree[-1].append(x)
    except KeyError:
        pass
    try:
        harvey_id[tree[-1][-1]]
        if len(harvey_id[tree[-1][-1]])>0:
            tree[-1].append(harvey_id[tree[-1][-1]])

    except KeyError:
        pass
    tree[-1].reverse()
'''
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
with open('../DATA/logfile.txt','w') as logFile:
    for row in forest:
        if len(row)>1:
            pprint.pprint(row, logFile)

'''
for row in tree:
    for test in tree:
        print(tree.index(row))
        if row!=test:
            if len(row)> len(test):
                if str(test) in str(row):
                    tree.remove(test)
            else:
                if str(row) in str(test):
                    tree.remove(row)
'''

