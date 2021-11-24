''' Project - Solver for the 24 Game. https://www.24game.com/
            The goal of the game is to use simple operations with 4 chosen integers to yield 24. This solver takes any
            four numbers and displays all possible solutions resulting in 24. The program also prompts the user to change
            the default settings, so that any number not just 24, can be chosen as the target (with a variable number of 
            integers to choose from). 7 starting integers was the highest number I tested. 

- Developed by Peter Richieri
- Completed 11/24/2021
- Tested with Python 3.9.7
- No special packages needed

Running this file will start the solver. Currently it uses integer math which is probably cheating, ignore those solutions. 
    Currently it removes solutions with swapped steps to leave only the "unique" ones, change the global toggle to change that.

 '''

import copy
import time
TARGET = 24
STARTING_NUMBERS = 4
LEAVES = 0  # Dont' touch
# Removes "duplicate" answers. Duplicates either have the same operations done but the order
CLEAN_SOLUTIONS = True
# reversed ( (1-2)+5 vs (1+5)-2 ), or the or the order reversed in the same operation (3*2 vs 2*3)

''' Node class for each number in the tree. Keeps track of operations taken to get there, 
as well as if it's a solution or not.    ex: 2 3 7 8    Level 0   __24__
                                                                /       \
                                                          +2  / \-2  *2 / \ %2  (also w/ 3, 7, 8)
                                                             /   \     /   \
                                                Level 1   {26}  {22}{48}  {12} 
                                                          /  \  / \  / \  / \
                                                               etc. Stop if you hit 2,3,7, or 8 at level 3
'''
class Node:
    def __init__(self, value, history=[], level=0):
        self.value = value
        self.history = history

        # Not really needed in the end but was fine for testing.
        self.level = level
        self.children = []
        self.solution = False

    def PrintTree(self):
        print(self.value)

    def insert(self, value, operation):
        self.children.append(
            Node(value, self.history.append(operation), self.level + 1))

    ''' Adds a node and modifies parameters '''

    def insert(self, child):  # child should be a Node, can't seem to enforce this here though
        self.children.append(child)
        if self.history is not None:
            child.history = self.history + child.history
        else:
            pass
        child.level = self.level + 1

    '''Find all solutions at the leaves of the tree, return in a list '''

    def inOrderTraversal(self, currentNode):
        res = []
        if currentNode.children == [] and currentNode.solution == True and currentNode.value != '0':
            res.append((str(float(currentNode.value)), currentNode.history))
        else:
            for elem in currentNode.children:
                res = res + currentNode.inOrderTraversal(elem)
        return res


''' Standardizes list contents '''

def convertToFloat(myList):
    newList = []
    for elem in myList:
        newList.append(str(float(elem)))
    return newList


''' Fetches numbers from user. Checks for four parameters. Assumes that user knows what integers are. '''

def getInts():
    global TARGET
    global STARTING_NUMBERS
    skip = False
    while(True):

        while(not skip):
            choice = input(
                f"\n The target number is {TARGET}, and there will be a pool of {STARTING_NUMBERS} numbers to use. Would you like to change these settings (y/n)? \n >")
            if choice == 'y' or choice == 'yes':

                TARGET = float(
                    int(input("\n Please enter the new target number: ")))
                STARTING_NUMBERS = int(
                    input("\n Please enter the new size of the pool of starting numbers: "))
                skip = True
            elif choice == 'n' or choice == 'no':
                skip = True
            else:
                continue

        numList = input(f"\n Enter {STARTING_NUMBERS} integers: ")
        numList1 = numList.split(' ')
        numList2 = numList.split(',')

        if len(numList1) == STARTING_NUMBERS:
            return convertToFloat(numList1)

        elif len(numList2) == STARTING_NUMBERS:
            return convertToFloat(numList2)

        else:
            print(
                f"\n Error! The game needs exactly {STARTING_NUMBERS} numbers.")


''' Find all values reachable from {value} using any operation with {num}. Append resulting number, in a tuple
    with a record of what operation was used, to an array to be returned. '''

def allPossible(node, num):     # Expect (String, String)
    neighbors = []
    cleanedNumber = str(float(num))
    neighbors.append((str(float(node) * float(num)), '/' + cleanedNumber))
    neighbors.append((str(float(node) + float(num)), '-' + cleanedNumber))

    # Can't divide by zero
    if float(num) != 0:
        neighbors.append((str(float(node) / float(num)), '*' + cleanedNumber))
    neighbors.append((str(float(node) - float(num)), '+' + cleanedNumber))

    return neighbors


''' Assemble a directional graph (tree), with 24 at the root, of all possible combinations of operations. 
  Edges represent an operation (+,-,*, /) and number choice, and nodes represent the numbers that result from them. '''

def constructGraph(currentNode, numList):
    global LEAVES
    # Done if no more numbers left to try. Mark the node if it's a solution
    if len(numList) == 1:
        if currentNode.value == numList[0]:
            currentNode.solution = True
        LEAVES += 1
        return None

    # Find reachable values, insert them as children
    for num in numList:
        neighbors = allPossible(currentNode.value, num)
        for neighbor in neighbors:
            # value, operation (appended into history)
            child = Node(neighbor[0], [neighbor[1]])
            currentNode.insert(child)

            # Recurse with the children
            updatedList = copy.copy(numList)  # Don't mess with parent array
            updatedList.remove(num)
            constructGraph(child, updatedList)

    return None


''' Call the traversal function in the Node class. '''

def findSolutions(completeGraph):
    results = completeGraph.inOrderTraversal(completeGraph)
    return results


''' Do math with strings '''

def evaluateExpression(current, next, operand):
    if '+' == operand:
        return float(current) + float(next)
    elif '-' == operand:
        return float(current) - float(next)
    elif '*' == operand:
        return float(current) * float(next)
    else:
        return float(current) / float(next)


''' Finds and purges duplicate solutions. Though they have distinct paths to distinct leaves in the tree,
        they are functionally identical mathmatical expressions. 
        Additionally, shifting the contents of the array makes it easier to spot duplicates
        Input: [ [2, ( '+14', '*2','+3') ] , [second solution] , [etc...] ]
        New format: [[('2', '+', '3'), ('5','*', '2'), ('10', '+', '14')], [second solution], [etc]]'''

def removeDuplicates(results):

    # Shifting the contents of the array makes it easier to spot duplicates
    # New format: [[('2', '+', '3'), ('5','*', '2'), ('10', '+', '14')], [second solution], [etc]]
    def _convertToTuples(results):
        output = []
        count = 0
        for elem in results:
            output.append([])
            current = elem[0]
            for i in range(STARTING_NUMBERS - 1):
                next = elem[1].pop()
                evaluated = evaluateExpression(current, next[1:], next[0])
                output[count].append((current, next[0], next[1:]))
                current = evaluated
            count += 1
        return output

    cleaned = _convertToTuples(results)

    if CLEAN_SOLUTIONS:  # Global toggle
        mfd = []
        # Compare each solution against each other once. Check is order-agnostic by casting solutions as sets
        for i in range(len(cleaned)):
            for j in range(i+1, len(cleaned)):
                same = True
                for expression in range(STARTING_NUMBERS - 1):
                    if set(cleaned[i][expression]) != set(cleaned[j][expression]):
                        same = False
                if same:
                    mfd.append(j)

        # Have to remove indexes back to front to preserve validity of marked duplicates
        mfd = set(mfd)
        for index in sorted(mfd, reverse=True):
            del cleaned[index]

        mfd = []
        output = []
        # Similar to before, but now try to find solutions with swapped steps, instead of checking inside each step.
        for i in range(len(cleaned)):
            for j in range(i+1, len(cleaned)):
                # In place for loop to keep things concise
                if(set([cleaned[i][expression][1] + cleaned[i][expression][2] for expression in range(STARTING_NUMBERS - 1)]).union({'+' + cleaned[i][0][0]})
                        == set([cleaned[j][expression][1] + cleaned[j][expression][2] for expression in range(STARTING_NUMBERS - 1)]).union({'+' + cleaned[j][0][0]})):

                    mfd.append(j)
                    output.append((cleaned[i], cleaned[j]))

        # Have to remove indexes back to front to preserve validity of marked duplicates
        mfd = set(mfd)
        for index in sorted(mfd, reverse=True):
            del cleaned[index]

    return cleaned


''' Print the solutions to the terminal nicely. Didn't have to evaluate the expressions again really,
        but it seemed easiet. 
        Input: [[('2', '+', '3'), ('5','*', '2'), ('10', '+', '14')], [second solution], [etc]] '''

def printResults(results):
    if len(results) == 0:
        return f"there are no solutions that equal {str(int(float(TARGET)))}."
    elif len(results) == 1:
        out = f"there is one solution that equals {str(int(float(TARGET)))}.\n"
    else:
        out = f"there are {len(results)} unique solutions that equal {str(int(float(TARGET)))}.\n"
    count = 1
    for elem in results:
        print(f"Solution {count}:\n")
        current = elem[0][0]
        for line in elem:
            operand = line[1]
            evaluated = evaluateExpression(line[0], line[2], operand)

            # Chop off the '.0' from floats but preserve meaningful digits without messing with the actualy variables.
            # This is the dumbest, most inefficient way to accomplish this ... but it works?
            pcurrent = current
            pevaluated = evaluated
            p2 = line[2]
            if float(current) - float(int(float(current))) == 0.0:
                pcurrent = str(int(float(current)))
            if float(evaluated) - float(int(float(evaluated))) == 0.0:
                pevaluated = str(int(float(evaluated)))
            if float(p2) - float(int(float(p2))) == 0.0:
                p2 = str(int(float(p2)))

            print(f"{pcurrent} {operand} {p2} = {pevaluated}")
            current = evaluated
        print("____________________\n")
        count += 1
    return out


def main():
    numList = getInts()
    root = Node(f'{str(TARGET)}')  # TARGET set as 24 by default up top

    startTime = time.time()
    print("\nCreating dynamic programming table ...")
    startConstruct = time.time()
    constructGraph(root, numList)
    print(
        f"Done. That took {round(time.time() - startConstruct, 5)} seconds.\n")
    print("Searching tree for solutions ...")
    startSolutions = time.time()
    results = findSolutions(root)
    print(
        f"Done. That took {round(time.time() - startSolutions, 5)} seconds.\n")
    print("Removing duplicate solutions ...")
    startClean = time.time()
    cleanedResults = removeDuplicates(results)
    print(f"Done. That took {round(time.time() - startClean, 5)} seconds.\n")
    print("Printing solutions ...\n")
    numberOfSolutions = printResults(cleanedResults)
    print(f"\nTask completed in {round(time.time() - startTime, 5)} seconds.")
    print(f"Out of {LEAVES} possible calculations, {numberOfSolutions}")


if __name__ == '__main__':
    main()
