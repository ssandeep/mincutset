from pygraph import graph
from pygraph.mixins.labeling import labeling
from pygraphviz import *
from pygraph.readwrite.dot import write

#Graph:
ns = ['a', 'b','c', 'd', 'e']
G = graph()
G.add_nodes(ns)
G.add_edge('a', 'b',  wt=5)
G.add_edge('b', 'c',  wt=1)
G.add_edge('c', 'd',  wt=7)
G.add_edge('d', 'e',  wt=6)
G.add_edge('e', 'a',  wt=4)

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
graphImage.graph_attr['label']='Graph of example9'
eset = graphImage.edges()
for edge in eset:
    (graphImage.get_edge(edge[0], edge[1])).attr['label'] = str(G.edge_weight(edge[0], edge[1]))
graphImage.layout()
graphImage.draw('example9.png')

