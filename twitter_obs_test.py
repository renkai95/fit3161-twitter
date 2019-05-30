import build_tree as bt
import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys

def testTraverse():
    #Empty list returns empty graph
    n = nx.Graph()
    bt.traverse(n,{},{})
    assert n.number_of_edges()==0, "Traversed empty graph should return empty graph"
    n.clear()
    #Empty 
    bt.traverse(n,{'id':'2','id_children':[{'id':'3'}]},{'2':'2','3':'3'})
    assert n.number_of_edges()==1, "One nested element results in 1 edge"
    n.clear()
    bt.traverse(n,{'id':'2','id_children':[{'id':'3'}]},{})
    assert n.number_of_edges()==0, "No input id data will not result in any return value"
    n.clear()
    bt.traverse(n,{'id':'2'},{'id':'2'})
    assert n.number_of_edges()==0, "Terminal node will not add an edge"
    n.clear()
    bt.traverse(n,{'id':'2','id_children':[{'id':'3'},{'id':'4'}]},{'2':'2','3':'3','4':'4'})
    assert n.number_of_edges()==2, "2 child nodes results in 2 edges"
    n.clear()
    bt.traverse(n,{},{'2':'2','3':'3','4':'4'})
    assert n.number_of_edges()==0, "Empty node results in empty graph"

def testTrimTerminators():
    replied_to = [('1','2'),('2','3')]
    replied_inlist = {'1':'1','2':'2'}
    bt.trimTerminators(replied_to,replied_inlist)
    #print(replied_to)
    assert replied_to[2]==('3','3') ,"Terminal node should be 3,3"
    replied_to = [('1','2'),('2','3')]
    replied_inlist = {}
    bt.trimTerminators(replied_to,replied_inlist)
    #print(replied_to)
    assert replied_to[2]==('2','2') and replied_to[3] == ('3','3'), "no input data still adds terminators"
    replied_to = []
    replied_inlist = {'1':'1','2':'2'}
    bt.trimTerminators(replied_to,replied_inlist)
    #print(replied_to)
    assert len(replied_to)==0, "no input replied to data does not add terminators"


    
    
def testAll():
    testTraverse()
    #testBuildReplyTree()

    testTrimTerminators()


if __name__ == "__main__":
    testAll()

