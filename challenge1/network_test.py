# I will represent the directed graph with an adjacency list. The input 
# for this will be edges which is a tuple of tuples.
# E.g 1 -> 2 -> 3 -> 5 -> 2 -> 1 is represented as ((1,2), (2,3), (3,5), (5,2), (2,1))
def adjacency_list(edges):
    graph = {}
    for edge in edges:
        a, b = edge
        if graph.get(a):
            graph[a].append(b)
        else:
            graph[a] = [b]
    return graph

# the function above will return the adjancency list
# 1 -> 2 -> 3 -> 5 -> 2 -> 1 to {1: [2], 2: [3, 1], 3: [5], 5: [2]}


def identify_router(edges):
    #  convert the edges to an adjacency list
    graph = adjacency_list(edges)

    # create a set to track visited nodes to avoid repeated traversing in cyclical sections
    visited = set()

    # Initiating a stack for depth first traversal of the graph. Starting from the first node in the Edge list
    stack = [edges[0][0]]

    # A dictionary and list to track the biggest occurrences of nodes
    count = {}
    largest = [edges[0][0]]
    while len(stack) > 0:

        # Traverse by popping the most recent element
        current = stack.pop()

        #  If it has been recorded, add the number of its neighbors to the connections count; 
        #  if not, assign it to the connections counts of its neighbors.
        if count.get(current) is not None:
            count[current] += len(graph[current])
        else:
            count[current] = len(graph[current])
            
        # Add the explored node to the visited set to avoid repeated traversing
        visited.add(current)
        # add the neighbors of the current node to the stack
        for neighbour in graph[current]:
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


assert identify_router([(1, 2), (2, 3), (3, 5), (5, 2), (2, 1)]) == {2}
assert identify_router([(1, 3), (3, 5), (5, 6), (6, 4), (4, 5), (5, 2), (2, 6)]) == {5}
assert identify_router([(2, 4), (4, 6), (6, 2), (2, 5), (5, 6)]) == {2, 6}

# Time complexity is O(n) n being the nuber of Nodes in the Graph.
# This is becuase No nodes are acted on more that once. If they are encountered they are skipped
