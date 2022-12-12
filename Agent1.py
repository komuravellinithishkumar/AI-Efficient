from GenerateGrid import GenerateGrid
from collections import defaultdict
import random
from UtilityFunctions import Utility
import time
import Grid as g
import math
import copy
import json


class Agent1:
    def __init__(self):
        self.generateGrid = GenerateGrid()
        self.discount = 0.90
        # self.nonterminalReward = -0.001
        self.error = 1e-22

        self.utility = None

    def valueIteration(self, grid, distance, degree, positionofAgent, positionofPrey, positionofpredator, size=50, iterations=100):

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

        a = 0
        while iterations > 0:
            print("enteereeedd while looppppp")
            a += 1
            error = 0

            nextUtility = copy.deepcopy(utility)

            # Compute Next Utility
            # agent, prey, pred = 0, 0, 0
            # For all the states
            for agentPosition in range(size):
                for preyPosition in range(size):
                    for predPosition in range(size):
                        nextValue = math.inf
                        # Compute the utility for all the actions
                        allPossibleAgentActions = Utility.getSurroundingNodesOfAParticularNode(
                            grid, agentPosition)
                        su = 0
                        for everyNewPossibleAgent in allPossibleAgentActions:
                            preyActions = Utility.getSurroundingNodesOfAParticularNode(
                                grid, preyPosition, include=True
                            )
                            predActions = Utility.getSurroundingNodesOfAParticularNode(
                                grid, predPosition)

                            additionOfAllPosibilities = 0
                            for everyNewPossiblePrey in preyActions:
                                for everyNewPossiblePred in predActions:
                                    prob = self.findingProbabilityofNextState(
                                        grid,
                                        distance,
                                        degree,
                                        utility,
                                        (agentPosition, preyPosition, predPosition),
                                        (everyNewPossibleAgent,
                                         everyNewPossiblePrey, everyNewPossiblePred),
                                    )

                                    additionOfAllPosibilities += (
                                        prob * utility[everyNewPossibleAgent][everyNewPossiblePrey][everyNewPossiblePred])

                            nextValue = min(
                                nextValue, additionOfAllPosibilities * self.discount)
                            # print(nextVal)
                        #print("agent", agent)
                        #print("pred", pred)
                        if agentPosition == predPosition:
                            reward = math.inf
                        elif agentPosition == preyPosition:
                            reward = 0

                        else:
                            reward = 1

                        nextUtility[agentPosition][preyPosition][predPosition] = nextValue + reward

                        if (
                            utility[agentPosition][preyPosition][predPosition] == math.inf
                            or nextUtility[agentPosition][preyPosition][predPosition] == math.inf
                        ):

                            continue

                        error = max(error, abs(
                            utility[agentPosition][preyPosition][predPosition] - nextUtility[agentPosition][preyPosition][predPosition]),)

            utility = copy.deepcopy(nextUtility)
            print(
                "Value iteration for",
                a,
                error,
                self.error * (1 - self.discount) / self.discount,
                # utility,
            )
            if error < 10**-15:
                break

            iterations -= 1

        return utility

    def agent1(self, grid, distance, degree, positionofAgent, positionofPrey, positionofpredator, size=50, iteratative=100, visualize=False,):

        if self.utility is None:

            self.utility = self.valueIteration(
                grid, distance, degree, positionofAgent, positionofPrey, positionofpredator, size
            )

            with open("test.txt", "w") as f:

                f.write(json.dumps(self.utility))

            print(self.utility)

        while iteratative > 0:

            if positionofAgent == positionofpredator:
                return False, 3, 100 - iteratative, positionofAgent, positionofpredator, positionofPrey

            if positionofAgent == positionofPrey:
                return True, 0, 100 - iteratative, positionofAgent, positionofpredator, positionofPrey

            agentSorroundingNodes = Utility.getSurroundingNodesOfAParticularNode(
                grid, positionofAgent)

            maxValue = math.inf
            maxNeighbour = 1

            for agent in agentSorroundingNodes:

                val = self.utility[agent][positionofPrey][positionofpredator]

                if val < maxValue:
                    maxValue = val
                    maxNeighbour = agent

            positionofAgent = maxNeighbour

            if positionofAgent == positionofpredator:
                return False, 4, 100 - iteratative, positionofAgent, positionofpredator, positionofPrey

            # check prey
            if positionofAgent == positionofPrey:
                return True, 1, 100 - iteratative, positionofAgent, positionofpredator, positionofPrey

            positionofPrey = Utility.movePrey(positionofPrey, grid)

            if positionofAgent == positionofPrey:
                return True, 2, 100 - iteratative, positionofAgent, positionofpredator, positionofPrey

            positionofpredator = Utility.movePredator(
                positionofAgent, positionofpredator, grid, distance)

            iteratative -= 1

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

            result, line, steps, positionofAgent, positionofpredator, positionofPrey = self.agent1(
                grid, distance, degree, positionofAgent, positionofPrey, positionofpredator, size, 100, False
            )

            print(result, positionofAgent, positionofpredator, positionofPrey)
            counter += result
            stepsCount += steps
        # print(self.agent1(graph, path, dist, agentPos, preyPos, predPos))
        # print(result, line)

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


if __name__ == "__main__":

    agent1 = Agent1()
    counter = 0
    stepsArray = []
    for _ in range(1):

        result, steps = agent1.AgentOperation(50)
        counter += result
        stepsArray.append(steps)
    print(counter, stepsArray)
