from GenerateGrid import GenerateGrid

import random
from UtilityFunctions import Utility
import time
from copy import copy


class Agent4:
    
    def __init__(self):
        self.generateGrid = GenerateGrid()

    def BeliefArrayRegularization(self, PositionOfAgent, PositionOfPrey, PositionOfPredator, grid, dist, degree):

        #Normalize belief array for all the nodes in the grid.

        currentBeliefArrayLength = len(self.beliefArray)

        #Create a new belief array from the previous belief array and initialize all it's values to zero.

        futureBeliefArray = [None] * currentBeliefArrayLength

        for k in range(currentBeliefArrayLength):
            futureBeliefArray[k] = 0

        #Split the probability of a particular node to it's surrounding nodes.

        for i in range(currentBeliefArrayLength):

            surroundingNodes = Utility.getSurroundingNodesOfAParticularNode(grid, i)

            surroundingNodes.append(i)

            for currentSurroundedNode in surroundingNodes:

                currentSurroundedNodeDegree = degree[currentSurroundedNode]

                #Update the probability present in the belief array, not replace.

                futureBeliefArray[i] = futureBeliefArray[i] + (self.beliefArray[currentSurroundedNode] / (currentSurroundedNodeDegree + 1))

        self.beliefArray = copy(futureBeliefArray)

        self.BeliefArrayModification(PositionOfAgent, PositionOfPrey)  

    def scoutForPreyInGraph(self, currentNode, preyPosition):

        if currentNode != preyPosition:
            return False

        else:
            return True
    
    def findNodeToScout(self):

        #Find all the nodes, having highest probability from the belief array

        nodesAvailableToScout = []

        #Scout the node, having the max probability

        maximumProbability = max(self.beliefArray)

        for currentNode, b in enumerate(self.beliefArray):

            current_max_value = b

            if current_max_value == maximumProbability:

                #Store all the nodes having the highest probability (which we have calculated before)
                nodesAvailableToScout.append(currentNode)

        scoutNodesLength = len(nodesAvailableToScout)

        #Pick one of the node having the highest probability

        if scoutNodesLength > 0:
            return random.choice(nodesAvailableToScout)

    def moveAgent(self, PositionOfAgent, predictedPreyPos, PositionOfPrey, PositionOfPredator, graph, dist, degree):

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

    def BeliefArrayModification(self, positionOfAgent, PositionOfPrey):

        prevBeliefArrayLength = len(self.beliefArray)

        newBeliefArray = [None] * prevBeliefArrayLength

        for k in range(prevBeliefArrayLength):
            newBeliefArray[k] = 0

        scoutedNode = positionOfAgent

        if scoutedNode == PositionOfPrey:
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
    
    def forecastPreyPosition(self):
        #Find all the nodes, having highest probability from the belief array

        nodesAvailableForPrayToMove = []

        #Scout the node, having the max probability

        maximumProbability = max(self.beliefArray)

        for a, b in enumerate(self.beliefArray):

            current_max_value = b

            if current_max_value == maximumProbability:

                #Store all the nodes having the highest probability (which we have calculated before)
                nodesAvailableForPrayToMove.append(a)

        scoutNodesLength = len(nodesAvailableForPrayToMove)

        #Pick one of the node having the highest probability

        if scoutNodesLength > 0:
            return random.choice(nodesAvailableForPrayToMove)

    def calculateWeightFactor(self, PositionOfAgent, PositionOfPrey, PositionOfPredator, nextPreyPositions, distance, beliefArray, graph):
        
        agentSurroundingNodes = Utility().getSurroundingNodesOfAParticularNode(graph, PositionOfAgent)

        weightFactor = {}
        for z in agentSurroundingNodes:

            currWeightFactor = 0
            for probablePreyPosition in nextPreyPositions:

                neighbourPredDistance = distance[z][PositionOfPredator]

                denominator = (neighbourPredDistance + 0.5) ** 100

                tempBelief = beliefArray[probablePreyPosition]

                currWeightFactor += (distance[z][probablePreyPosition] * (1 - tempBelief)) / denominator

            weightFactor[z] = currWeightFactor

        return weightFactor

    def nextbeliefArray(self, beliefArray, graph, degree, PositionOfPrey):

        # create a future belief array with same length of belief array

        # initialize all the elements of future belief array with 0.

        lengthOfBeliefArray = len(beliefArray)

        futureBeliefArray = [None] * lengthOfBeliefArray

        for a in range(lengthOfBeliefArray):
            futureBeliefArray[a] = 0

        surroundingNodes = Utility.getSurroundingNodesOfAParticularNode(graph, PositionOfPrey)
        surroundingNodes.append(PositionOfPrey)

        #Increment the next belief array of surrounding nodes based on the belief of prey.

        for currentSurroundingNode in surroundingNodes:

            beliefOfPrey = beliefArray[PositionOfPrey]

            degreeOfPreyNode = degree[PositionOfPrey]

            futureBeliefArray[currentSurroundingNode] = futureBeliefArray[currentSurroundingNode] + beliefOfPrey / (degreeOfPreyNode + 1)

        #At last return the updated belief array

        return futureBeliefArray

    def agent4(self, grid, path, distance, PositionOfAgent, PositionOfPrey, PositionOfPredator, degree, TotalRuns=100, visualize=False,):

        self.BeliefArrayModification(PositionOfAgent, PositionOfPrey)

        while TotalRuns > 0:

            if PositionOfAgent == PositionOfPredator:
                return False, 3, 100 - TotalRuns, PositionOfAgent, PositionOfPrey

            #Agent wins, if the positon of agent is same as the position of prey

            if PositionOfAgent == PositionOfPrey:
                return True, 0, 100 - TotalRuns, PositionOfAgent, PositionOfPrey

            scoutnode = self.findNodeToScout()

            self.BeliefArrayModification(scoutnode, PositionOfPrey)

            predictedPreyPosition = self.forecastPreyPosition()

            futureBeliefArray = self.nextbeliefArray(self.beliefArray, grid, degree, predictedPreyPosition)

            nextPreyPositions = []
            
            for preyPosition, beliefArray in enumerate(futureBeliefArray):
                
                if beliefArray != 0:
                    nextPreyPositions.append(preyPosition)

            weightFactorMap = self.calculateWeightFactor(PositionOfAgent, PositionOfPrey, PositionOfPredator, nextPreyPositions, distance, futureBeliefArray, grid,)

            # move agent
            PositionOfAgent = sorted(weightFactorMap.items(), key=lambda x: x[1])[0][0]

            self.BeliefArrayRegularization(PositionOfAgent, PositionOfPrey, PositionOfPredator, grid, distance, degree)
            
            beliefArraySum = sum(self.beliefArray)

            print("Belief Array Sum ->",beliefArraySum)
            
            print(PositionOfAgent, PositionOfPrey, PositionOfPredator, predictedPreyPosition)

            # check predator position
            if PositionOfAgent == PositionOfPredator:
                return False, 4, 100 - TotalRuns, PositionOfAgent, PositionOfPrey

            # check prey position
            if PositionOfAgent == PositionOfPrey:
                return True, 1, 100 - TotalRuns, PositionOfAgent, PositionOfPrey

            # move prey in grid
            PositionOfPrey = Utility.movePreyInGrid(PositionOfPrey, grid)

            if PositionOfAgent == PositionOfPrey:
                return True, 2, 100 - TotalRuns, PositionOfAgent, PositionOfPrey

            # move predator in grid
            PositionOfPredator = Utility.movePredatorWithoutShortestPath(PositionOfAgent, PositionOfPredator, grid, distance)

            TotalRuns -= 1

        return False, 5, 100, PositionOfAgent, PositionOfPrey

    def executeAgent4(self, graphSize):

        graph, path, dist, degree = self.generateGrid.generateGraphUtil(graphSize)

        counter = 0

        stepsCount = 0

        NoOfSimulations = 100

        while(NoOfSimulations > 0):

            PositionOfPredator = random.randint(0, graphSize - 1)

            PositionOfAgent = random.randint(0, graphSize - 1)

            PositionOfPrey = random.randint(0, graphSize - 1)
            

            self.beliefArray = [1 / graphSize for i in range(graphSize)]
            ans, line, steps, PositionOfAgent, PositionOfPrey = self.agent4(graph, path, dist, PositionOfAgent, PositionOfPrey, PositionOfPredator, degree, 100, False)

            print(ans, PositionOfAgent, PositionOfPrey)
            counter += ans
            stepsCount += steps

            NoOfSimulations -= 1

        return counter, stepsCount / 100

if __name__ == "__main__":

    agent4 = Agent4()
    counter = 0
    stepsArray = []
    for _ in range(30):
        result, steps = agent4.executeAgent4(50)
        counter += result
        stepsArray.append(steps)
    print("SUCCESS RATE OF AGENT 4 --> ", counter / 30, stepsArray)
