from GenerateGrid import GenerateGrid
import random
from UtilityFunctions import Utility
import time


class Agent1:
    def __init__(self):
        self.generateGrid = GenerateGrid()

    def moveAgent(self, PositionOfAgent, PositionOfPrey, PositionOfPredator, graph, dist):

        surroundingNodesOfAgent = Utility.getSurroundingNodesOfAParticularNode(graph, PositionOfAgent)

        PreyDistanceFromNeighbours = []
        PredatorDistanceFromNeighbours = []

        presentPreyDistance = dist[PositionOfAgent][PositionOfPrey]
        presentPredatorDistanc = dist[PositionOfAgent][PositionOfPredator]

        for index, elem in enumerate(surroundingNodesOfAgent):
            PreyDistanceFromNeighbours.append(dist[elem][PositionOfPrey])
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

    def agent1(self, graph, path, dist, PositionOfAgent, PositionOfPrey, PositionOfPredator, totalRuns=100,):

        while totalRuns > 0:

            print(PositionOfAgent, PositionOfPredator, PositionOfPrey)

            if PositionOfAgent == PositionOfPredator:
                return False, 3, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            if PositionOfAgent == PositionOfPrey:
                return True, 0, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            # move agent
            PositionOfAgent = self.moveAgent(PositionOfAgent, PositionOfPrey, PositionOfPredator, graph, dist)

            # check predator
            if PositionOfAgent == PositionOfPredator:
                return False, 4, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            # check prey
            if PositionOfAgent == PositionOfPrey:
                return True, 1, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            # move prey
            PositionOfPrey = Utility.movePreyInGrid(PositionOfPrey, graph)

            if PositionOfAgent == PositionOfPrey:
                return True, 2, 100 - totalRuns, PositionOfAgent, PositionOfPrey

            # move predator
            PositionOfPredator = Utility.movePredatorWithoutShortestPath(PositionOfAgent, PositionOfPredator, graph, dist)

            totalRuns -= 1

        return False, 5, 100, PositionOfAgent, PositionOfPrey

    def executeAgent(self, gridSize):

        grid, path, distanceToGoal, degree = self.generateGrid.generateGraphUtil(gridSize)

        current = 0

        NoOfSteps = 0

        simulationCount = 100

        while(simulationCount > 0):

            positionOfPredator = random.randint(0, gridSize - 1)
            positionOfPrey = random.randint(0, gridSize - 1)
            positionOfAgent = random.randint(0, gridSize - 1)

            answer, line, steps, positionOfAgent, positionOfPrey = self.agent1(
                grid, 10, distanceToGoal, positionOfAgent, positionOfPrey, positionOfPredator, 100
            )

            print(answer, positionOfAgent, positionOfPrey)

            current += answer
            NoOfSteps += steps
            simulationCount -= 1

        return current, NoOfSteps / 100


if __name__ == "__main__":

    agent1 = Agent1()
    counter = 0
    stepsArray = []
    for _ in range(30):

        result, steps = agent1.executeAgent(50)
        counter += result
        stepsArray.append(steps)
    print(counter / 30, stepsArray)
