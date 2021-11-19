
import copy
class Graph:
    
    graph_dict={}
    
    def addEdge(self,node,neighbour):  
        if node not in self.graph_dict:
            self.graph_dict[node]=[neighbour]
        else:
            self.graph_dict[node].append(neighbour)
            
    def show_edges(self):
        for node in self.graph_dict:
            for neighbour in self.graph_dict[node]:
                print("(",node,", ",neighbour,")")
    
    
    def find_path(self,start,end,path=[]):
            path = path + [start]    
            if start==end:
                return path
            attempt = self.graph_dict.get(start)
            if attempt:
                for node in self.graph_dict[start]:
                    if node not in path:
                        newPath=self.find_path(node,end,path)
                        if newPath:
                            return newPath
                        return None
    
    def BFS(self,s):
        visited={}
        for i in self.graph_dict:
            visited[i]=False
        queue=[]
        queue.append(s)
        visited[s]=True
        while len(queue)!=0:
            s=queue.pop(0)
            for node in self.graph_dict[s]:
                if visited[node]!=True:
                    visited[node]=True
                    queue.append(node)
            print(s,end=" ")
            
    def All_Paths(self,start,end,path=[]):
        path = path + [start]
        if start == end:
            return [path]
        paths = []
        for node in self.graph_dict[start]:
            if node not in path:
              newpaths = self.All_Paths(node, end, path)
              for newpath in newpaths:
                paths.append(newpath)
        return paths
    
    def Shortest_Path(self,start,end,path=[]):
        path=path+[start]
        if start==end:
            return path
        shortest=None
        for node in self.graph_dict[start]:
            if node not in path:
                newpath=self.Shortest_Path(node, end, path)
                if newpath:
                    if not shortest or len(shortest)>len(newpath):
                        shortest=newpath
        return shortest
    
    def DFS(self,s):
        visited={}
        for i in self.graph_dict:
            visited[i]=False
        stack=[s]
        visited[s]=True
        while stack:
            n=stack.pop(len(stack)-1)
            for i in self.graph_dict[n]:
                if not visited[i]:
                    stack.append(i)
                    visited[i]=True
            print(n)


def getInts():
    while(True):
        numList = input("\n Enter four integers: ")
        numList1 = numList.split(' ')
        numList2 = numList.split(',')

        if len(numList1) ==4:
            # for item in numList1:
            #     item = int(item)
            return numList1

        elif len(numList2) ==4:
            # for item in numList2:
            #     item = int(item)
            return numList2
        
        else:
            print("\n Error: The game needs exactly four numbers.")


def allPossible(node, num):
    neighbors = []
    neighbors.append( str(float(node) * float(num)) ) 
    neighbors.append( str(float(node) + float(num)) )
    if float(num) != 0:
        neighbors.append( str(float(node) / float(num)) )
    if float(node) != 0:
        neighbors.append( str(float(num) / float(node)) )
    neighbors.append( str(float(node) - float(num)) )
    neighbors.append( str(float(num) - float(node)) )
    return neighbors
        


# Assemble a directional map, with 24 at the center, of all possible combinations of operations. 
# Edges represent operations (+,-,*, /) and node represent the numbers that result from them.
def constructGraph(g,node, numList):
    #print("\n ################################################################################################### NEW NODE")
    #print("\n numlist is: ", numList)
    #print("\n node is: ", node)
    if numList == []:
        return None
    
    for num in numList:
        neighbors = allPossible(node, num)
        #print("\n Checking ", num)
        #print("\n neighbors are: ", neighbors)
        for neighbor in neighbors:
            #g.addEdge(node, neighbor)
            g.addEdge(neighbor, node)
       
        
        for neighbor in neighbors:
            #print("\n ABOUT TO REMOVE: ", num)
            updatedList = copy.copy(numList)
            #print("\n HERE IS THE COPY: ", updatedList)
            updatedList.remove(num)
            #print("\n Updated list is: ", updatedList)
            #print("\n -- Constructing next layer of graph -- ")
            constructGraph(g, neighbor, updatedList)
    return None

def findSolutions(completeGraph, numList):
    print("\n FINDING PATHS NOW")
    print("\n HERE ARE THE TARGETS", numList)
    for num in numList:
        print("\n SEARCHING FOR ", str(float(num)))
        print("first try")
        print(completeGraph.All_Paths(str(float(num)), '24.0'))
        print("second try")
        print(completeGraph.find_path( '24.0', str(float(num))))
        print("third try")
        print("fourth try")
    return None


def main():
    numList = getInts()
    g = Graph()
    completeGraph = constructGraph(g,'24.0', numList)
    #g.show_edges()
    print("\n")
    results = findSolutions(g, numList)
    # print results
    #g.show_edges()
    # print(g.All_Paths('4','1'))



if __name__ == '__main__':
    main()