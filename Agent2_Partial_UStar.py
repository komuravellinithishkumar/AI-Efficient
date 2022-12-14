import csv
from GenerateGrid import GenerateGrid
from collections import defaultdict
import random
from UtilityFunctions import Utility
import time
import Grid as g
import math
import json
import copy
# from copy import copy, deepcopy
# from copy import deepcopy




class Agent2_Partial_UStar:
    def __init__(self):

        self.generateGrid = GenerateGrid()
        self.utility = None
        self.errorValue = 1e-22
        self.valueToBeDiscounted = 0.90



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

        if len(nodesAvailableToScout) > 0:
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

        # print("new belief", newBeliefArray)

        # print("old beliefArray", self.beliefArray)

        #self.beliefArray = copy(newBeliefArray)

        self.beliefArray = copy.deepcopy(newBeliefArray)

        # print("old beliefArray1", self.beliefArray)

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

        #self.beliefArray = copy(futureBeliefArray)

        self.beliefArray = copy.deepcopy(futureBeliefArray)

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

    def valueIteration(self, grid, distance, degree, positionofAgent, positionofPrey, positionofpredator, size=50, iterativeValue=100):

        utility = [[[-1 for i in range(size)]
                    for j in range(size)] for k in range(size)]
        # i = agent , j = prey k = pred
        agent, prey, pred = 0, 0, 0

        while(agent < size):
            while(prey < size):
                while(pred < size):

                    utility[agent][agent][prey] = 0
                    utility[agent][prey][pred] = distance[agent][prey]
                    utility[agent][prey][agent] = math.inf
                    predatorSorrundingNodes = Utility.getSurroundingNodesOfAParticularNode(
                        grid, pred)
                    for neigh in predatorSorrundingNodes:
                        utility[neigh][prey][pred] = math.inf

                    pred += 1
                prey += 1
            agent += 1

        index = 0
        while iterativeValue > 0:
            index += 1
            errorValue = 0

            nextUtility = copy.deepcopy(utility)

            # agent_1, prey_1, pred_1 = 0, 0, 0

            for agent_1 in range(size):
                for prey_1 in range(size):
                    for pred_1 in range(size):

                        nextValue = math.inf

                        allPossibleAgentActions = Utility.getSurroundingNodesOfAParticularNode(grid, agent_1)

                        # su = 0

                        for everyNewPossibleAgent in allPossibleAgentActions:
                            preyActions = Utility.getSurroundingNodesOfAParticularNode(grid, prey_1, include=True)
                            predActions = Utility.getSurroundingNodesOfAParticularNode(grid, pred_1)

                            additionOfAllPosibilities = 0
                            for everyNewPossiblePrey in preyActions:
                                for everyNewPossiblePred in predActions:
                                    prob = self.findingProbabilityofNextState(grid,distance,degree,utility,(agent_1, prey_1, pred_1),
                                        (everyNewPossibleAgent,everyNewPossiblePrey, everyNewPossiblePred),)

                                    additionOfAllPosibilities += ( prob * utility[everyNewPossibleAgent][everyNewPossiblePrey][everyNewPossiblePred])

                            nextValue = min(
                                nextValue, additionOfAllPosibilities * self.valueToBeDiscounted)
                            
                        if agent_1 == pred_1:
                            reward = math.inf
                        elif agent_1 == prey_1:
                            reward = 0
                        else:
                            reward = 1

                        #print("rew", reward)
                        # print("nextValue", nextValue)

                        # print("utility", nextUtility[agent_1][prey_1][pred_1])

                        nextUtility[agent_1][prey_1][pred_1] = nextValue + reward

                        if (utility[agent_1][prey_1][pred_1] == math.inf or nextUtility[agent_1][prey_1][pred_1] == math.inf
                        ):
                            #pred_1 += 1
                            continue

                        utilityVal = utility[agent_1][prey_1][pred_1];

                        nextUtilityVal = nextUtility[agent_1][prey_1][pred_1];

                        absoluteDifference = abs(utilityVal - nextUtilityVal)

                        errorValue = max(errorValue, absoluteDifference,)

            #         pred_1 += 1
            #     prey_1 += 1
            # agent_1 += 1

            utility = copy.deepcopy(nextUtility)
            print(
                "Value iteration for",
                index,
                errorValue,
                self.errorValue * (1 - self.valueToBeDiscounted) / self.valueToBeDiscounted,
                # utility,
            )
            if errorValue < 10**-15:
                break

            iterativeValue -= 1

        return utility

    def agent1(self, grid, distance, degree, positionofAgent, positionofPrey, positionofpredator, size=50, iterantValue=100, visualize=False,):

        if self.utility is None:

            # Stored utility from U* value in file, so no need to value iteration again.

            self.utility = self.getUtilityFromFile()

            # self.utility = self.valueIteration(
            #     grid, distance, degree, positionofAgent, positionofPrey, positionofpredator, size
            # )

        while iterantValue > 0:

            if positionofAgent == positionofpredator:
                return False, 3, 100 - iterantValue, positionofAgent, positionofpredator, positionofPrey

            if positionofAgent == positionofPrey:
                return True, 0, 100 - iterantValue, positionofAgent, positionofpredator, positionofPrey

            self.BeliefArrayModification(positionofAgent, positionofPrey)
            nodeScouted = self.findScoutNode()
            self.BeliefArrayModification(nodeScouted, positionofPrey)

            agentSorroundingNodes = Utility.getSurroundingNodesOfAParticularNode(
                grid, positionofAgent)

            maxValue = math.inf
            maxNeighbour = 1

            # maxValue = math.inf
            # maxNeighbour = 1

            for currentNode in agentSorroundingNodes:

                Summation=0

                length = len(self.beliefArray)

                for currentBeliefIndex in range(length):

                    currentBelief = self.beliefArray[currentBeliefIndex]

                    currentUtility = self.utility[currentNode][currentBeliefIndex][positionofpredator]

                    Summation += currentBelief * currentUtility

                currentValue = Summation

                if currentValue < maxValue:
                    maxValue = currentValue
                    maxNeighbour = currentNode

            positionofAgent = maxNeighbour


            # for agent in agentSorroundingNodes:

            #     val = self.utility[agent][positionofPrey][positionofpredator]

            #     if val < maxValue:
            #         maxValue = val
            #         maxNeighbour = agent

            # positionofAgent = maxNeighbour

            self.BeliefArrayRegularization(positionofAgent, positionofPrey, positionofpredator, grid, distance, degree)

            if positionofAgent == positionofpredator:
                return False, 4, 100 - iterantValue, positionofAgent, positionofpredator, positionofPrey

            # check prey
            if positionofAgent == positionofPrey:
                return True, 1, 100 - iterantValue, positionofAgent, positionofpredator, positionofPrey

            positionofPrey = Utility.movePreyInGrid(positionofPrey, grid)

            if positionofAgent == positionofPrey:
                return True, 2, 100 - iterantValue, positionofAgent, positionofpredator, positionofPrey

            positionofpredator = Utility.movePredatorNewStrategy(
                positionofAgent, positionofpredator, grid, distance)

            iterantValue -= 1

        return False, 5, 100, positionofAgent, positionofpredator, positionofPrey

    def AgentOperation(self, size):

        # graph, path, dist, degree = self.generateGraph.generateGraph(size)

        grid, distance, degree = (
            g.getGrid(), g.getDistance(), g.getDegree(),)
        counter = 0

        stepsCount = 0
        for _ in range(100):

            positionofAgent = random.randint(0, size - 1)
            positionofPrey = random.randint(0, size - 1)
            positionofpredator = random.randint(0, size - 1)

            while positionofpredator == positionofAgent:
                positionofpredator = random.randint(0, size - 1)

            self.beliefArray = [1 / size for i in range(size)]


            result, line, steps, positionofAgent, positionofpredator, positionofPrey = self.agent1(
                grid, distance, degree, positionofAgent, positionofPrey, positionofpredator, size, 100, False
            )

            print(result, positionofAgent, positionofpredator, positionofPrey)
            counter += result
            stepsCount += steps

        return counter, stepsCount / 100

    def findingProbabilityofNextState(self, grid, distance, degree, utility, currState, nextState):
        """
        Adding rewards for taking that particular action
        """
        agentProbability = 1
        preyProbability = 1 / (degree[currState[1]] + 1)

        predatorSorrundingNodes = Utility.getSurroundingNodesOfAParticularNode(
            grid, currState[2])

        neighbourDistanceMap = defaultdict(list)
        for everyPossiblePredator in predatorSorrundingNodes:
            neighbourDistanceMap[distance[everyPossiblePredator]
                                 [nextState[0]]].append(everyPossiblePredator)
        minimumDistanceList = neighbourDistanceMap.get(
            min(neighbourDistanceMap), [])
        if nextState[2] in minimumDistanceList:
            predProbability = 0.6 / (len(minimumDistanceList)) + 0.4 / (
                degree[currState[2]] + 1
            )
        else:
            predProbability = 0.4 / (degree[currState[2]] + 1)
        # print(preyProbability, predProbability,"test")
        return preyProbability * predProbability

    def getUtilityFromFile(self):
        utility = [[[-1 for i in range(50)] for j in range(50)] for k in range(50)]
        with open("/common/home/gs943/Desktop/AI Project 1312/AI Project 3 github(nithish)/AI-Efficient-main/Utilitydata.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    utility[int(row[0])][int(row[1])][int(row[2])] = float(row[-1])
                    line_count += 1
        return utility

if __name__ == "__main__":

    agent1 = Agent2_Partial_UStar()
    counter = 0
    stepsArray = []
    for _ in range(1):

        result, steps = agent1.AgentOperation(50)
        counter += result
        stepsArray.append(steps)
    print(counter, stepsArray)
