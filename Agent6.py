from collections import defaultdict
from copy import copy

from GenerateGrid import GenerateGrid
import random
from UtilityFunctions import Utility


class Agent6:
    
    def __init__(self):
        self.generateGrid = GenerateGrid()

    def progressAgent(self, PositionOfAgent, predictedPreyPos, PositionOfPredator, graph, dist):

        surroundingNodesOfAgent = Utility.getSurroundingNodesOfAParticularNode(graph, PositionOfAgent)

        PreyDistanceFromNeighbours = []
        PredatorDistanceFromNeighbours = []

        presentPreyDistance = dist[PositionOfAgent][predictedPreyPos]
        presentPredatorDistanc = dist[PositionOfAgent][PositionOfPredator]

        for index, elem in enumerate(surroundingNodesOfAgent):
            PreyDistanceFromNeighbours.append(dist[elem][predictedPreyPos])
            PredatorDistanceFromNeighbours.append(dist[elem][PositionOfPredator])

        #Move the Agent based on the priorities as mentioned in the write-up.

        availableMovesForAgent = []
        for i in range(len(PredatorDistanceFromNeighbours)):
            if (
                PreyDistanceFromNeighbours[i] < presentPreyDistance
                and PredatorDistanceFromNeighbours[i] > presentPredatorDistanc
            ):
                availableMovesForAgent.append(surroundingNodesOfAgent[i])

        #If we get a move based on the first priority itself, return that move.

        countOfAvailablMovesForAgent = len(availableMovesForAgent)

        if countOfAvailablMovesForAgent > 0:
            return random.choice(availableMovesForAgent)


        #Other-wise, explore other priorities.

        for i in range(len(PredatorDistanceFromNeighbours)):
            if (
                PreyDistanceFromNeighbours[i] < presentPreyDistance
                and PredatorDistanceFromNeighbours[i] == presentPredatorDistanc
            ):
                availableMovesForAgent.append(surroundingNodesOfAgent[i])
    

        countOfAvailablMovesForAgent = len(availableMovesForAgent)

        if countOfAvailablMovesForAgent > 0:
            return random.choice(availableMovesForAgent)




        for i in range(len(PredatorDistanceFromNeighbours)):
            if (
                PreyDistanceFromNeighbours[i] == presentPreyDistance
                and PredatorDistanceFromNeighbours[i] > presentPredatorDistanc
            ):
                availableMovesForAgent.append(surroundingNodesOfAgent[i])

        countOfAvailablMovesForAgent = len(availableMovesForAgent)

        if countOfAvailablMovesForAgent > 0:
            return random.choice(availableMovesForAgent)




        for i in range(len(PredatorDistanceFromNeighbours)):
            if (
                PreyDistanceFromNeighbours[i] == presentPreyDistance
                and PredatorDistanceFromNeighbours[i] == presentPredatorDistanc
            ):
                availableMovesForAgent.append(surroundingNodesOfAgent[i])


        countOfAvailablMovesForAgent = len(availableMovesForAgent)

        if countOfAvailablMovesForAgent > 0:
            return random.choice(availableMovesForAgent)




        for i in range(len(PredatorDistanceFromNeighbours)):
            if PredatorDistanceFromNeighbours[i] > presentPredatorDistanc:
                availableMovesForAgent.append(surroundingNodesOfAgent[i])


        countOfAvailablMovesForAgent = len(availableMovesForAgent)

        if countOfAvailablMovesForAgent > 0:
            return random.choice(availableMovesForAgent)




        for i in range(len(PredatorDistanceFromNeighbours)):
            if PredatorDistanceFromNeighbours[i] == presentPredatorDistanc:
                availableMovesForAgent.append(surroundingNodesOfAgent[i])


        countOfAvailablMovesForAgent = len(availableMovesForAgent)

        if countOfAvailablMovesForAgent > 0:
            return random.choice(availableMovesForAgent)

        return PositionOfAgent

    def BeliefArrayModification(self, positionOfAgent, PositionOfPredator):

        prevBeliefArrayLength = len(self.beliefArray)

        newBeliefArray = [None] * prevBeliefArrayLength

        for k in range(prevBeliefArrayLength):
            newBeliefArray[k] = 0

        scoutedNode = positionOfAgent

        if scoutedNode == PositionOfPredator:
            newBeliefArray[scoutedNode] = 1

        else:

            #If prey is not present in scout node, make the belief of that node to 0.
            newBeliefArray[scoutedNode] = 0

            newBeliefArrayLength = len(newBeliefArray)

            for currentNode in range(newBeliefArrayLength):

                if(currentNode!=scoutedNode):

                    scoutedNodeBelief = self.beliefArray[scoutedNode]

                    currentNodeBelief = self.beliefArray[currentNode]

                    newBeliefArray[currentNode] = currentNodeBelief / (1 - scoutedNodeBelief)

        self.beliefArray = copy(newBeliefArray)
    
    def findNodeToSurvey(self,PositionOfAgent,distance):
        #Find all the nodes, having highest probability from the belief array

        nodesAvailableForScout = []

        #Scout the node, having the max probability

        maximumProbability = max(self.beliefArray)

        for a, b in enumerate(self.beliefArray):

            current_max_value = b

            if current_max_value == maximumProbability:

                #Store all the nodes having the highest probability (which we have calculated before)
                nodesAvailableForScout.append(a)

        nodesSameProbability=[]

        int_min=999999

        for x in nodesAvailableForScout:

            if(distance[PositionOfAgent][x]<int_min):
                int_min=distance[PositionOfAgent][x]

        for x in nodesAvailableForScout:

            if(distance[PositionOfAgent][x]==int_min):
                nodesSameProbability.append(x)


        availableOptionsLength = len(nodesSameProbability)

        #Pick one of the node having the highest probability

        if availableOptionsLength > 0:
            return random.choice(nodesSameProbability)

    def executeAgent(self, graphSize):

        graph, path, dist, degree = self.generateGrid.generateGraphUtil(graphSize)

        counter = 0

        stepsCount = 0

        NoOfSimulations = 100

        while(NoOfSimulations > 0):

            PositionOfPredator = random.randint(0, graphSize - 1)

            PositionOfAgent = random.randint(0, graphSize - 1)

            PositionOfPrey = random.randint(0, graphSize - 1)


            self.beliefArray = [0 for i in range(graphSize)]
            self.beliefArray[PositionOfPredator] = 1

            ans, line, steps, PositionOfAgent, PositionOfPrey = self.agent6(graph, path, dist, PositionOfAgent, PositionOfPrey, PositionOfPredator, degree, 100)

            print(ans, PositionOfAgent, PositionOfPrey)
            counter += ans
            stepsCount += steps

            NoOfSimulations -= 1

        return counter, stepsCount / 100

    def calculateWeightFactor(self, PositionOfAgent, PositionOfPrey, futurePredatorPosition, distance, beliefArray, graph):

        agentSurroundingNodes = Utility().getSurroundingNodesOfAParticularNode(graph, PositionOfAgent)
        agentSurroundingNodes.append(PositionOfAgent)

        predatorSurroundingNodes= Utility().getSurroundingNodesOfAParticularNode(graph, futurePredatorPosition)

        weightFactor = {}
        for z in agentSurroundingNodes:

            currWeightFactor = 0
            for probablePreyPosition in predatorSurroundingNodes:

                neighbourPredDistance = distance[z][probablePreyPosition] * 2 - distance[PositionOfPrey][z]

                tempBelief = beliefArray[probablePreyPosition]

                currWeightFactor += neighbourPredDistance * (1 - tempBelief)

            tempLength = len(predatorSurroundingNodes)

            weightFactor[z] = -currWeightFactor / tempLength

        return weightFactor

    def scoutForPredatorInGraph(self, currentNode, predatorPosition):
        if currentNode != predatorPosition:
            return False

        else:
            return True

    def agent6(self,grid,path,dist,PositionOfAgent,PositionOfPrey,PositionOfPredator,degree,totalRuns=100,):


        while totalRuns > 0:

            if PositionOfAgent == PositionOfPredator:
                return False, 3, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            if PositionOfAgent == PositionOfPrey:
                return True, 0, 100 - totalRuns, PositionOfAgent, PositionOfPrey


            self.BeliefArrayModification(PositionOfAgent, PositionOfPredator)

            scoutnode=self.findNodeToSurvey(PositionOfAgent,dist)

            self.BeliefArrayModification(scoutnode, PositionOfPredator)

            predictedPredPosition = self.forecastPredatorPosition(PositionOfAgent,dist)
            
            weightFactorMap = self.calculateWeightFactor(PositionOfAgent,PositionOfPrey,predictedPredPosition,dist,self.beliefArray,grid,)

            # move agent
            PositionOfAgent = sorted(weightFactorMap.items(), key=lambda x: x[1])[0][0]

            self.BeliefArrayRegularization(PositionOfAgent, grid, dist, degree)
            
            print(PositionOfAgent, PositionOfPrey, PositionOfPredator, predictedPredPosition, sum(self.beliefArray))
            
            # check predator
            if PositionOfAgent == PositionOfPredator:
                return False, 4, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            # check prey
            if PositionOfAgent == PositionOfPrey:
                return True, 1, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            # move prey
            PositionOfPrey = Utility.movePreyInGrid(PositionOfPrey, grid)

            if PositionOfAgent == PositionOfPrey:
                return True, 2, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            # move predator
            PositionOfPredator = Utility.movePredatorNewStrategy(PositionOfAgent, PositionOfPredator, grid, dist)

            totalRuns -= 1

        return False, 5, 100, PositionOfAgent, PositionOfPrey

    def BeliefArrayRegularization(self, PositionOfAgent, grid, dist, degree):

        #Normalize belief array for all the nodes in the grid.

        currentBeliefArrayLength = len(self.beliefArray)

        #Create a new belief array from the previous belief array and initialize all it's values to zero.

        futureBeliefArray = [None] * currentBeliefArrayLength

        for k in range(currentBeliefArrayLength):
            futureBeliefArray[k] = 0

        newBeliefArray1 = [None] * currentBeliefArrayLength

        newBeliefArray2 = [None] * currentBeliefArrayLength

        for k in range(currentBeliefArrayLength):
            newBeliefArray1[k] = 0.4*self.beliefArray[k]
            newBeliefArray2[k] = 0.6*self.beliefArray[k]

        for i in range(currentBeliefArrayLength):

            surroundingNodes = Utility.getSurroundingNodesOfAParticularNode(grid, i)

            surroundingNodesDistanceMap = defaultdict(list)

            for currentSurroundedNode in surroundingNodes:

                surroundingNodesDistanceMap[dist[currentSurroundedNode][PositionOfAgent]].append(currentSurroundedNode)

            minimumDistanceList = surroundingNodesDistanceMap.get(min(surroundingNodesDistanceMap), [])

            for intelligent_choice in minimumDistanceList:
                futureBeliefArray[intelligent_choice] += newBeliefArray2[i]/(len(minimumDistanceList))

            surroundingNodes = Utility.getSurroundingNodesOfAParticularNode(grid, i)

            for currentSurroundedNode in surroundingNodes:

                currentSurroundedNodeDegree = degree[currentSurroundedNode]

                #Update the probability present in the belief array, not replace.

                futureBeliefArray[i] = futureBeliefArray[i] + (newBeliefArray1[currentSurroundedNode] / (currentSurroundedNodeDegree))

        self.beliefArray = copy(futureBeliefArray)

    def forecastPredatorPosition(self, PositionOfAgent, distance):
        #Find all the nodes, having highest probability from the belief array

        nodesAvailableForPredatorToMove = []

        #Scout the node, having the max probability

        maximumProbability = max(self.beliefArray)

        for a, b in enumerate(self.beliefArray):

            current_max_value = b

            if current_max_value == maximumProbability:

                #Store all the nodes having the highest probability (which we have calculated before)
                nodesAvailableForPredatorToMove.append(a)

        nodesSameProbability=[]

        int_min=999999
        for x in nodesAvailableForPredatorToMove:

            if(distance[PositionOfAgent][x]<int_min):
                int_min=distance[PositionOfAgent][x]

        for x in nodesAvailableForPredatorToMove:
            
            if(distance[PositionOfAgent][x]==int_min):
                nodesSameProbability.append(x)


        availableOptionsLength = len(nodesSameProbability)

        #Pick one of the node having the highest probability

        if availableOptionsLength > 0:
            return random.choice(nodesSameProbability)

if __name__ == "__main__":

    agent6 = Agent6()
    counter = 0
    stepsArray = []
    for _ in range(30):

        result, steps = agent6.executeAgent(50)
        counter += result
        stepsArray.append(steps)
    print(counter/30, stepsArray)
