import csv
import matplotlib.pyplot as plt
import networkx as nx
import math

from igraph import *
from networkx import pagerank
from networkx import clustering, hits
from networkx import connected_components, subgraph
from networkx import average_degree_connectivity
from networkx.algorithms.approximation import average_clustering,clustering_coefficient
from networkx.algorithms.assortativity.correlation import degree_pearson_correlation_coefficient, \
    attribute_assortativity_coefficient, numeric_assortativity_coefficient, degree_assortativity_coefficient
from networkx.algorithms.clique import enumerate_all_cliques,node_clique_number,find_cliques

'''

This is the correct version of 1/06/2022

Comments about this code:

The CSV  needs to have an extra column with some values in it.
For example a .  in the most right column.
If this extra column does not exist, all values in the last column will be read
as '<value> \n'   instead of '<value>'   which messes up
the rest of the code.

Make sure the CSV is in the exact same directory as your python module.


# pip install pycairo
# pip install igraph
# pip install networkx
# pip install scipy
# pip install matplotlib


'''

# Mother=source page, that recommends the corresponding index in recommendation1 list, recommendation 2 list, etc
Motherlist = []
Rec1list = []
Rec2list = []
Rec3list = []
Rec4list = []
Rec5list = []

# Slegte.csv  or Bol.csv
# if using slegte, delete empty columns in line 184

# Seperates individual lists from the csv
with open('sleg.csv', encoding='utf-8-sig') as file:  # encoding in right form deletes the unneccesary characters
    csv_reader = csv.reader(file, delimiter=',')
    line_count = 0
    for row in file:

        row = row.split(',')
        index = 0
        for e in row:
            if index == 0:
                Motherlist.append(e)
                index += 1
            elif index == 1:
                Rec1list.append(e)
                index += 1
            elif index == 2:
                Rec2list.append(e)
                index += 1
            elif index == 3:
                Rec3list.append(e)
                index += 1
            elif index == 4:
                Rec4list.append(e)
                index += 1
            elif index == 5:
                Rec5list.append(e)
                index += 1
            elif index > 6:
                print(
                    "something went wrong. Please check the booklist and the length of the recommendations. All books should have exactly five recommendations.")

        line_count += 1
    print(f'Processed {line_count} books.')

# tests if the lists are compiled correctly
'''
print(Motherlist)
print(Rec1list)
print(Rec2list)
print(Rec3list)
print(Rec4list)
print(Rec5list)
'''

# creates a list of recommendation lists
Recommendationlist = []
Recommendationlist.append(Rec1list)
Recommendationlist.append(Rec2list)
Recommendationlist.append(Rec3list)
Recommendationlist.append(Rec4list)
Recommendationlist.append(Rec5list)

# List with all recommendation values in it, but not as as a list of lists
Totallist = []
for i in Rec1list:
    Totallist.append(i)
for i in Rec2list:
    Totallist.append(i)
for i in Rec3list:
    Totallist.append(i)
for i in Rec4list:
    Totallist.append(i)
for i in Rec5list:
    Totallist.append(i)

# create empty graphs
bookgraph = Graph(directed=True)
bookgraph2 = Graph(directed=False)
Gnx = nx.Graph()

# adds mother vertices to empty graphs
for mother in Motherlist:
    bookgraph.add_vertex(mother)
    bookgraph2.add_vertex(mother)
    Gnx.add_node(mother)

# keeps track of existing nodes as to not create double nodes
vertexlist = []
for i in Motherlist:
    vertexlist.append(i)

# creates the recommendation vertices and checks if they already exist or not
count = 0
for i in Totallist:
    # if i in vertexlist:
    # print(i, 'exists')
    # print(count)
    count += 1
    if i not in vertexlist:
        # print(i, 'didnt exist yet  in', vertexlist)
        vertexlist.append(i)
        bookgraph.add_vertex(i)
        bookgraph2.add_vertex(i)
        Gnx.add_node(i)

# add edges between mothers and recommendations
for i in range(len(Motherlist)):
    mother = Motherlist[i]
    for r in range(5):
        rec = Recommendationlist[r][i]
        bookgraph.add_edges([(mother, rec)])  # creates edges
        bookgraph2.add_edges([(mother, rec)])
        Gnx.add_edge(mother, rec)


# functions to help calculate stuff
def getMean(listname):
    total = 0
    count = 0
    for i in listname:
        total += i
        count += 1
    return total / count


def getSum(listname):
    total = 0
    for i in listname:
        total += i
    return total


# delete  NULL values , only use for deSlegte.nl
Gnx.remove_node('')
bookgraph.delete_vertices('')
bookgraph2.delete_vertices('')

# analysis

print(" start analysis for Bol.com:  ")

layout = bookgraph.layout("drl")
connected = max(connected_components(Gnx), key=len)  # largest connected components
bookgraph.vs["label"] = bookgraph.vs["name"]  # shows the node names in the graph
# plot(bookgraph, layout=layout)
clust = VertexClustering(bookgraph, membership=range(bookgraph.vcount()))

print("vertex count: ", bookgraph.vcount(), ' edge count: ', bookgraph.ecount())
print('indegree mean: ', getMean(bookgraph.indegree()))
print('indegree sum: ', getSum(bookgraph.indegree()))
print('outdegree mean: ', getMean(bookgraph.outdegree()))
print('outdegree sum: ', getSum(bookgraph.outdegree()))

print('maxdegree: ', bookgraph.maxdegree())
print("radius", bookgraph.radius())  ## not usable for this graph?
print("average path length:", bookgraph.average_path_length())

# print("node length", len(node))
# print("node", node)


# print("the degree", bookgraph.degree)
# print("length of degree", len(degree))

print("density nx", nx.density(Gnx))
print('density igraph: ', bookgraph.density())
print('girth: ', bookgraph.girth())
print("maximum pagerank ", max(bookgraph.pagerank()))  # more infos needed to understand it
print("maximum authority score ", max(bookgraph.authority_score()))  # same
# print("average pagerank", getMean((pagerank(Gnx))))


# print("the connections", connected)
print("the largest connected component", len(connected))
print("networkx size", Gnx.size())
print("correlation", degree_pearson_correlation_coefficient(Gnx, x='out', y='in', weight=None, nodes=None))
print("average clustering", average_clustering(Gnx))
# print("clustering", clustering(Gnx))
print("Assortativity coefficient", degree_assortativity_coefficient(Gnx))
print("average_degree_connectivity", average_degree_connectivity(Gnx))
# print(list(enumerate_all_cliques(Gnx))) #shows all cliques
# print("node clique number",node_clique_number(Gnx))#shows all cliques max number for each nodes
# print("find cliques",list(find_cliques(Gnx)))
eac=node_clique_number(Gnx)
cliqueVal=[]
cliquekey=[]
maxClique=[]


for i in eac.values():
    cliqueVal.append(i)
for i in eac.keys():
    cliquekey.append(i)
totalcl = 0
for i in cliqueVal:
    totalcl+=i

mxcl=None
for i in eac.values():
    if(mxcl is None or i>mxcl):
        mxcl=i

print(len(cliquekey))


print("the average clique",totalcl/len(cliquekey))
print("the max clique is",mxcl)
print(len(cliquekey))
print(len(cliqueVal))
# plt.plot(cliquekey,cliqueVal)
# plt.show()
print(count)
print("Degree correlation ",degree_pearson_correlation_coefficient(Gnx)) #Compute degree assortativity of graph. not sure if that s what is needed


#clique graph #wrong later to be fixed
# G=nx.karate_club_graph()
# g=nx.find_cliques(Gnx)
# nx.draw(g)
# print("find cliques G",g)
# for i in g:


#######place for testing

import matplotlib.pyplot as plt
import networkx as nx

# bins = 20
# plt.hist(bookgraph.degree(), bins)
# plt.show()

######   end of testing


print(" end of analysis  ")

###what does this do?
'''

node=[]
degree=[]
rank=[]
for item in Gnx.degree:
     count=1
     for sep in item:
         if count%2!=0:
            node.append(sep)
            #print("sep", sep)
            count+=1
         else:
             degree.append(sep)
rx=pagerank(Gnx)#page rank

#print("pagerank values: ", pagerank(Gnx).values)  does not return correct value
#print("the rx", rx)  what does this do
'''

"Graphing___________________________________________"

'''
Functions that dont work yet
'''

# print("cliques", bookgraph2.cliques()) # uses an undirected version of the graph because it needs to be undirected.

# print(Gnx.adj.items())#prints the node adjacent to each others
# "connected components___________________________"=
# print("connected", ([len(c) for c in sorted(nx.connected_components(Gnx), key=len, reverse=True)]))#print len of connected components
# #print(nx.node_connected_component(Gnx,'https://www.bol.com/nl/nl/p/how-not-to-die/9200000046853322/'))#prints the links connected to (https://www.bol.com/nl/nl/p/how-not-to-die/9200000046853322/)
#
# print("hits")
# h,a=nx.hits(Gnx)
# print("maximum hits", max(h.items()))#print the max value of hits and key
# print(max(a.items()))#not sure what s the a and why it prints a different value
# print("h", h)

# print page rank_________________________________________________
# plt.show()

# print(clust.cluster_graph())  # Returns a graph where each cluster is contracted into a single vertex.
# plot(clust, mark_groups=True)

# print(bookgraph.eccentricity(vertices=None,mode="in"))
# none:uses all the vertices in the graph     in:direction is followed
# returns the calculated eccentricities in a list


#######notes ######
'''one of the mechanisms that Google use to determine the importance of a web page. In essence,
 a page (or package) is deemed to be more important if many other pages (packages) link to it.
 The good news is that the igraph package has a built-in function to compute the pagerank, called page.rank ().
'''

'''A clique is a subset of vertices of an undirected graph G such that every two distinct vertices in the clique are adjacent;
that is, its induced subgraph is complete. Cliques are one of the basic concepts of graph theory and are used in many other
mathematical problems and constructions on graphs.
'''

# print(avg(bookgraph.coreness()))


# print('Total indegree:', getSum(bookgraph.indegree()))
# print('Total outdegree:', getSum(bookgraph.outdegree()))

# print('mean indegree:', getMean(bookgraph.indegree()))
# print('mean outdegree:', getMean(bookgraph.outdegree()))


# Calculates the radius of the graph.
# The radius of a graph is defined as the minimum eccentricity of its vertices (see eccentricity()).


# he k-core of a graph is a maximal subgraph in which each vertex has at least degree k.
# (Degree here means the degree in the subgraph of course). The coreness of a vertex is k if
# it is a member of the k-core but not a member of the k + 1-core.
# returns the coreness of each vertex
# print(bookgraph.coreness())


# clustering
# print(bookgraph.clusters())
# print(bookgraph.vcount())#count number of vertices
# bookgraph.components()  # clusters Calculates the (strong or weak) clusters (connected components) for a given graph.
# # Clustering Coefficient is a network analysis algorithm which describes how closely nodes in a network tend to group or “cluster” together.


# In the mathematical field of graph theory, a core is a notion that describes behavior of a graph with respect to graph homomorphisms.
# Finds the coreness (shell index) of the vertices of the network.


# doesnt work, why?
# assortativity(Totallist, None, directed=True)



