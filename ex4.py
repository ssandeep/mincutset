from pygraph import graph
from pygraph.mixins.labeling import labeling
from pygraphviz import *
from pygraph.readwrite.dot import write

#Graph:
ns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
G = graph()
G.add_nodes(ns)
G.add_edge('a', 'b',  wt=2)
G.add_edge('a', 'h',  wt=3)
G.add_edge('c', 'b',  wt=3)
G.add_edge('h', 'b',  wt=2)
G.add_edge('c', 'd',  wt=4)
G.add_edge('h', 'g',  wt=3)
G.add_edge('e', 'd',  wt=2)
G.add_edge('g', 'b',  wt=2)
G.add_edge('f', 'g',  wt=1)
G.add_edge('e', 'f',  wt=3)
G.add_edge('f', 'c',  wt=2)
G.add_edge('f', 'd',  wt=2)

#Algorithm:
nodeSet = ns
globalS = []
globalV = []
globalMinCutWt = 1000000

for node in nodeSet:
	print node
	S = []
	V = list(nodeSet)
	S.append(node)
	V.remove(node)
	currentMinWt = 0
	for neighbor in G.neighbors(node):
        	currentMinWt = currentMinWt + G.edge_weight(node, neighbor)
	if currentMinWt < globalMinCutWt:
		globalS = list(S)
		globalV = list(V)
		globalMinCutWt = currentMinWt

	loopIndex = 0
	while len(S)<(len(nodeSet) - 1):
		eachSelected = S[loopIndex]
		neighborNodes = []
		neighborNodeWts = []
		for neighbor in G.neighbors(eachSelected):
			tempWt = 0
			if neighbor not in S:
				for nbrofnbr in G.neighbors(neighbor):
					if nbrofnbr not in S:
						tempWt = tempWt + G.edge_weight(nbrofnbr, neighbor)
					elif nbrofnbr in S:
						tempWt = tempWt - G.edge_weight(nbrofnbr, neighbor)
				neighborNodes.append(neighbor)
				neighborNodeWts.append(tempWt)
		try:
			nextNode = neighborNodes[neighborNodeWts.index(min(neighborNodeWts))]
		except ValueError:
			print "continuing"
			break
		S.append(nextNode)
		V.remove(nextNode)
		#Calculate Cut Weight:
		currentMinWt = currentMinWt + min(neighborNodeWts)
		if currentMinWt < globalMinCutWt:
			globalS = list(S)
			globalV = list(V)
			globalMinCutWt = currentMinWt
		loopIndex = loopIndex + 1
	print globalS
	print globalV
	print globalMinCutWt
	
print globalS
print globalV
print globalMinCutWt

# Draw as PNG:
dot = write(G)
graphImage = AGraph(string = dot)
graphImage.graph_attr['label']='Graph of example4'
eset = graphImage.edges()
for edge in eset:
    (graphImage.get_edge(edge[0], edge[1])).attr['label'] = str(G.edge_weight(edge[0], edge[1]))
graphImage.layout(prog='fdp')
graphImage.draw('example4.png')

