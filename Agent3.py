from GenerateGrid import GenerateGrid

import random
from UtilityFunctions import Utility
from copy import copy


class Agent3:

    def findScoutNode(self):

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

                    newBeliefArray[currentNode] = self.beliefArray[currentNode] / (1 - scoutedNodeBelief)

        self.beliefArray = copy(newBeliefArray)

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

    def scoutForPrey(self, currentNode, preyPosition):

        if currentNode == preyPosition:
            return True

        else:
            return False
    
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

    def agent3(self,graph,distance,PositionOfAgent,PositionOfPrey,PositionOfPredator,degree,totalRuns=100,):

        self.BeliefArrayModification(PositionOfAgent, PositionOfPrey)

        for currentRuns in range(totalRuns):

            if PositionOfAgent == PositionOfPredator:
                return False, 3, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            if PositionOfAgent == PositionOfPrey:
                return True, 0, 100 - currentRuns, PositionOfAgent, PositionOfPrey


            nodeToBeScouted=self.findScoutNode()

            self.BeliefArrayModification(nodeToBeScouted, PositionOfPrey)

            predictedPreyPosition = self.forecastPreyPosition()

            PositionOfAgent = self.moveAgent(PositionOfAgent,predictedPreyPosition,PositionOfPrey,
                                                        PositionOfPredator,graph,distance,degree)

            
            self.BeliefArrayRegularization(PositionOfAgent, PositionOfPrey, PositionOfPredator, graph, distance, degree)

            beliefArraySum = sum(self.beliefArray)

            print(PositionOfAgent, PositionOfPrey, PositionOfPredator, predictedPreyPosition, beliefArraySum)

            # check if we found predator
            if PositionOfAgent == PositionOfPredator:
                return False, 4, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            # check if we found predator
            if PositionOfAgent == PositionOfPrey:
                return True, 1, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            PositionOfPrey = Utility.movePreyInGrid(PositionOfPrey, graph)

            if PositionOfAgent == PositionOfPrey:
                return True, 2, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            
            PositionOfPredator = Utility.movePredatorWithoutShortestPath(PositionOfAgent, PositionOfPredator, graph, distance)


        return False, 5, 100, PositionOfAgent, PositionOfPrey

    def executeAgent3(self, gridSize):

        grid, path, distanceToGoal, degree = self.generateGrid.generateGraphUtil(gridSize)

        current = 0

        NoOfSteps = 0

        simulationCount = 100

        while(simulationCount > 0):

            positionOfPredator = random.randint(0, gridSize - 1)
            positionOfPrey = random.randint(0, gridSize - 1)
            positionOfAgent = random.randint(0, gridSize - 1)

            self.beliefArray = [1 / gridSize for i in range(gridSize)]

            answer, temp, steps, positionOfAgent, positionOfPrey = self.agent3(
                grid, distanceToGoal, positionOfAgent, positionOfPrey, positionOfPredator, degree, 100,
            )

            print(answer, positionOfAgent, positionOfPrey)
            current += answer
            NoOfSteps += steps

            simulationCount -= 1

        return current, NoOfSteps / 100

    def __init__(self):
        self.generateGrid = GenerateGrid()
if __name__ == "__main__":

    agent3 = Agent3()
    counter = 0
    NoOfstepsArray = []

    for _ in range(30):
        answer, steps = agent3.executeAgent3(50)
        counter += answer
        NoOfstepsArray.append(steps)

    print("SUCCESS RATE OF AGENT 3", counter / 30, NoOfstepsArray)
