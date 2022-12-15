from GenerateGrid import GenerateGrid
import random
from UtilityFunctions import Utility
import time


class Agent2:
    def __init__(self):
        self.generateGrid = GenerateGrid()

    def futurebeliefArray(self, prevBeliefArray, grid, degree, positionOfPrey):

        #The prey can choose to stay in the same node or move to it's neighbours.

        prevBeliefArrayLength = len(prevBeliefArray)

        newBeliefArray = [None] * prevBeliefArrayLength

        for k in range(prevBeliefArrayLength):
            newBeliefArray[k] = 0

        surroundingNodes = Utility.getSurroundingNodesOfAParticularNode(grid, positionOfPrey)
        surroundingNodes.append(positionOfPrey)

        degreeOfPreyNode = degree[positionOfPrey]

        prevBeliefValue = prevBeliefArray[positionOfPrey]

        probabilitySplit = (prevBeliefValue / (degreeOfPreyNode + 1))

        for currentNode in surroundingNodes:
            
            newBeliefArray[currentNode] = newBeliefArray[currentNode] + probabilitySplit

        return newBeliefArray

    def calculateWeightFactor(self, PositionOfAgent, preyPos, PositionOfPredator, futurePreyPositions, dist, beliefArray, graph):
        agentNeighbours = Utility().getSurroundingNodesOfAParticularNode(graph, PositionOfAgent)

        weightFactor = {}
        for n in agentNeighbours:

            currWeightFactor = 0
            for i in futurePreyPositions:

                neighbourPredDsitance = dist[n][PositionOfPredator]

                denominator = (neighbourPredDsitance + 0.005) ** 100

                currWeightFactor = currWeightFactor + (dist[n][i] * (1 - beliefArray[i])) / denominator

            weightFactor[n] = currWeightFactor

        return weightFactor

    def agent2(self,grid,distance,PositionOfAgent,PositionOfPrey,PositionOfPredator,degree,totalRuns=100,):

        currentRuns = totalRuns

        for x in range(currentRuns):

            if PositionOfAgent == PositionOfPredator:
                return False, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            if PositionOfAgent == PositionOfPrey:
                return True, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            graphLength = len(grid)

            currentBeliefArray = [None] * graphLength

            for i in range(graphLength):
                currentBeliefArray[i] = 0

            # If prey is present in a particular node, then the belief value of that particular node becomes 1

            currentBeliefArray[PositionOfPrey] = 1

            futureBeliefArray = self.futurebeliefArray(
                currentBeliefArray, grid, degree, PositionOfPrey
            )

            nextPreyPositions = []
            for i, j in enumerate(futureBeliefArray):
                if j != 0:
                    nextPreyPositions.append(i)

            weightFactorMap = self.calculateWeightFactor(PositionOfAgent,PositionOfPrey,PositionOfPredator,nextPreyPositions,distance,futureBeliefArray,grid,)

            # move agent
            PositionOfAgent = sorted(weightFactorMap.items(), key=lambda x: x[1])[0][0]

            # check Predator
            if PositionOfAgent == PositionOfPredator:
                return False, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            # check prey
            if PositionOfAgent == PositionOfPrey:
                return True, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            # move prey
            PositionOfPrey = Utility.movePreyInGrid(PositionOfPrey, grid)

            if PositionOfAgent == PositionOfPrey:
                return True, 100 - currentRuns, PositionOfAgent, PositionOfPrey

            PositionOfPredator = Utility.movePredatorWithoutShortestPath(PositionOfAgent, PositionOfPredator, grid, distance)

        return False, 100, PositionOfAgent, PositionOfPrey

    def executeAgent(self, gridSize):

        grid, path, distanceToGoal, degree = self.generateGrid.generateGraphUtil(gridSize)

        current = 0

        NoOfSteps = 0

        simulationCount = 100

        while(simulationCount > 0):

            positionOfPredator = random.randint(0, gridSize - 1)
            positionOfPrey = random.randint(0, gridSize - 1)
            positionOfAgent = random.randint(0, gridSize - 1)

            answer, steps, positionOfAgent, positionOfPrey = self.agent2(
                grid, distanceToGoal, positionOfAgent, positionOfPrey, positionOfPredator, degree, 100
            )

            print(answer, positionOfAgent, positionOfPrey)

            current += answer
            NoOfSteps += steps
            simulationCount -= 1

        return current, NoOfSteps / 100


if __name__ == "__main__":

    agent1 = Agent2()
    counter = 0
    stepsArray = []
    for _ in range(30):

        result, steps = agent1.executeAgent(50)
        counter += result
        stepsArray.append(steps)
    print(counter / 30, stepsArray)
