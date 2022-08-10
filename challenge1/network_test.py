#class Implementation

#still using the adajancy_list to represent a graph.

#we will an instantiate empty dictionary. It is best we use an ordered dictionary but since the rules says no library.
#we will have a first_node element to keep track of the first element in the graph.
# then we have a function that add edges to the graph.
#and our identify function.
#more explanation is made below.



class Graph:
    def __init__(self):
        #initialization. 
        #first_node will store our first node in edge list. this makes it easier to get a starting node.
        self.graph = {}
        self.first_node = None
    
    def add_edge(self, edge):
        a, b = edge

        #assign the first_node 
        if self.first_node is None:
            self.first_node = a

        if self.graph.get(a):
            self.graph[a].append(b)
        else:
            self.graph[a] = [b]

    
    def add_multiple_edges(self, edges):
        for edge in edges:
            self.add_edge(edge)

    def identify_router(self):
        # create a set to track visited nodes to avoid repeated traversing in cyclical sections
        visited = set()

        # Initiating a stack for depth first traversal of the graph. Starting from the first node in the Edge list
        stack = [self.first_node]
    

        # A dictionary and list to track the biggest occurrences of nodes
        count = {}
        largest = [self.first_node]
        while len(stack) > 0:

            # Traverse by popping the most recent element
            current = stack.pop()

            #  If it has been recorded, add the number of its neighbors to the connections count; 
            #  if not, assign it to the connections counts of its neighbors.
            if count.get(current) is not None:
                count[current] += len(self.graph[current])
            else:
                count[current] = len(self.graph[current])
                
            # Add the explored node to the visited set to avoid repeated traversing
            visited.add(current)
            # add the neighbors of the current node to the stack
            for neighbour in self.graph[current]:
                if neighbour not in visited:
                    stack.append(neighbour)
                    # start counting them on append
                    if neighbour not in count:
                        count[neighbour] = 1
                else:
                    count[neighbour] += 1
                    # check the neighbors frequency and add to the largest list based on that
                    if count[neighbour] > count[largest[0]]:
                        largest = [neighbour]
                    elif count[neighbour] == count[largest[0]]:
                        largest.append(neighbour)
        # return a unique list of nodes with the highest connections
        return set(largest)
        

#TESTCASE.
graph_one = Graph()
graph_one.add_multiple_edges([(1, 2), (2, 3), (3, 5), (5, 2), (2, 1)])
assert graph_one.identify_router() == {2}

graph_two = Graph()
graph_two.add_multiple_edges([(1, 3), (3, 5), (5, 6), (6, 4), (4, 5), (5, 2), (2, 6)])
assert graph_two.identify_router() == {5}

graph_three = Graph()
graph_three.add_multiple_edges([(2, 4), (4, 6), (6, 2), (2, 5), (5, 6)])
graph_three.identify_router() == {2,6}

# # Time complexity is O(n) n being the nuber of Nodes in the Graph.
# # This is becuase No nodes are acted on more that once. If they are encountered they are skipped
