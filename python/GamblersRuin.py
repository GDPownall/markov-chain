#!/usr/bin/env python
#GamblersRuin.py 
#Evaluates the standard GamblersRuin game by matrix markov chain analysis

from MarkovClass import MarkovChain


def GetGamblersRuin(initialState=100, probUp = 0.5, upperLimit = 200, lowerLimit = 0):
    probDown = 1.-probUp
    nStates = upperLimit-lowerLimit+1
    initState = [0.]*nStates
    initState[initialState] = 1.

    transitionMatrix = []
    for n in range(nStates):
        transitionMatrix.append([0.]*nStates)


    transitionMatrix[0][0] = 1. #Probability from transitioning once hit lower limit is 0, so probability of staying is 1

    transitionMatrix[nStates-1][nStates-1] = 1. #Similar reasoning for when one hits the upper limit

    for n in range(1,nStates-1):
        transitionMatrix[n+1][n] = probUp #probability from going from n to n+1
        transitionMatrix[n-1][n] = probDown

    chain = MarkovChain(transitionMatrix,initState)
    return chain



if __name__ == '__main__':   
    x = GetGamblersRuin(4,0.5,10,0)
    print (x.StationaryState())
    x.PrintStateAtTime()
    print('\n')
    for t in range(10):
        print(x.CalcStateAtTime(t))
    x.PlotOverTime('docs/GamblerRuin.gif',100)
