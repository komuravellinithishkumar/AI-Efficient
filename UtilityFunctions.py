import math
import random
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np


class Utility:

    @staticmethod
    def getSurroundingNodesOfAParticularNode(grid, nodePosition, include=False):

        # initialize surrounding node list, to find the surrounding nodes and populate this list.
        surroundingNodes = []

        isEdgePresent = 1

        rowLength = len(grid[nodePosition])

        for currentIndex, column in enumerate(grid[nodePosition]):

            if column == isEdgePresent:
                surroundingNodes.append(currentIndex)

        return surroundingNodes

    @staticmethod
    def printFullGrid(grid):

        rows = len(grid)
        columns = len(grid[0])

        for row in range(rows):
            for col in range(columns):
                print(grid[row][col], end=", ")
            print()

    @staticmethod
    def movePreyInGrid(positionOfPrey, grid):

        possibleMovements = [positionOfPrey]

        finalPosition = -1

        rowLength = len(grid[positionOfPrey])

        for column in range(rowLength):

            if grid[positionOfPrey][column] == 1:
                possibleMovements.append(column)

        finalPosition = random.choice(possibleMovements)

        return finalPosition

    # @staticmethod
    # def movePredatorInGrid(positionOfAgent, positionOfPredator, pathWay):

    #     # Move Predator based on the shortest path between predator and agent

    #     # pathWay consists of shortest distance from one node to any node, which we calculated in floyd Warshall

    #     return pathWay[positionOfPredator][positionOfAgent]

    @staticmethod
    def applyFloydWarshal(grid, size):

        distance = [[math.inf for i in range(
            len(grid[0]))] for j in range(len(grid))]

        path = [[-1 for i in range(size)] for j in range(size)]

        rows = len(grid)

        # shortest distance from a node to itself is zero.

        for currentRow in range(rows):
            distance[currentRow][currentRow] = 0

        for y in range(size):
            for z in range(size):

                if grid[y][z] == 1:
                    distance[y][z] = 1
                    distance[z][y] = 1

        for x in range(size):
            for y in range(size):
                for z in range(size):

                    if distance[y][x] == math.inf or distance[x][z] == math.inf:
                        continue

                    if distance[y][z] > distance[y][x] + distance[x][z]:
                        distance[y][z] = min(
                            distance[y][z], distance[y][x] + distance[x][z])
                        distance[z][y] = min(
                            distance[y][z], distance[y][x] + distance[x][z])

        return path, distance

    # @staticmethod
    # def movePredatorWithoutShortestPath(positionOfAgent, positionOfPredator, grid, distance):

    #     # At any point predator can move to any of it's surrounding nodes.

    #     surroundingNodes = Utility.getSurroundingNodesOfAParticularNode(
    #         grid, positionOfPredator)
    #     surroundingDistanceMapping = defaultdict(list)

    #     # Find the minimum distance from all those surrounding nodes to the agent

    #     for x in surroundingNodes:
    #         surroundingDistanceMapping[distance[x][positionOfAgent]].append(x)

    #     # minimum distance to the agent.

    #     #minSurroundingDistance = min(surroundingDistanceMapping)

    #     minimumDistanceList = surroundingDistanceMapping.get(
    #         min(surroundingDistanceMapping), [])

    #     # Pick a node for the predator to move which is nearer to the agent.

    #     newPredatorPosition = random.choice(minimumDistanceList)

    #     # return the new predator position

    #     return newPredatorPosition

    @staticmethod
    def movePredatorNewStrategy(positionOfAgent, positionOfPredator, graph, distance):

        movement_list = [0, 1]

        move_strategy = random.choices(movement_list, weights=(40, 60), k=1)

        if(move_strategy[0]):
            surroundingNodes = Utility.getSurroundingNodesOfAParticularNode(
                graph, positionOfPredator)
            surroundingNodesDistanceMap = defaultdict(list)

            for currentSurroundingNode in surroundingNodes:
                surroundingNodesDistanceMap[distance[currentSurroundingNode][positionOfAgent]].append(
                    currentSurroundingNode)

            minimumDistanceList = surroundingNodesDistanceMap.get(
                min(surroundingNodesDistanceMap), [])
            #print(minimumDistanceList, "inside move_predator func")
            return random.choice(minimumDistanceList)

        else:
            listOfmoves = []

            size = len(graph[positionOfPredator])

            for currentPos in range(size):

                if graph[positionOfPredator][currentPos] == 1:
                    listOfmoves.append(currentPos)

            return random.choice(listOfmoves)
