#!/usr/bin/env python
#Script defining a class for Markov chain analysis

'''
The MarkovChain class allows one to define the probability matrix of a Markov chain process, and the initial state, and get the state at any time.

The probability matrix takes the form:
    [[p00,p10,p20,...]
     [p01,p11,p21,...]
     [p02,p12,p22,...]
     ...
     ]
where pxy is the probability to transition from state y to x
As a result, the columns must sum to unity. The class raises an exception otherwise.

The initial state is in the form of an array:
    [p0,p1,p2,...]
where px is the probability of the system starting at state x. The sum of this array must therefore be 1, and the class raises an exception otherwise.

The class is called as MarkovChain(probMatrix,initialState)

5 functions are available:
    SetInitState: Allows you to reset the initial state
    SetProbMatrix: Allows you to reset the probability matrix
    Evaluate: Returns the eigenvalues, eigenvectors and constants associated. You can call this yourself, of course, but it is mainly used by other functions.
    CalcStateAtTime(t): returns a vector of probabilities for the state at time t
    PrintStateAtTime(): prints the equation for calculating the state at time t.
    StationaryState(): returns the stationary state (ie. the state of the system at infinite time, which is the eigenvector with eigenvalue 1)
'''

import numpy as np

class Error(Exception):
    pass

class MarkovError(Error):
    pass

class MarkovChain:
    def __init__(self, probMatrix=None, initState=None):
        self.probMatrixSet = False
        self.initStateSet = False 
        self.Evaluation = None
        self.SetProbMatrix(probMatrix)
        self.SetInitState(initState)

    def SetProbMatrix(self,iMat):
        if isinstance(iMat,type( None )):
            print ( 'Initialised with no probability matrix.')
            self.ProbMatrix = None
        else:
            iMat = np.array(iMat)
            if False in [len(row) == len(iMat) for row in iMat]:
                print ('Matrix supplied to Markov Chain class not square')
                raise MarkovError
            for colNum in range(len(iMat)):
                column = iMat[:,colNum]
                if sum(column) != 1.:
                    print ('Matrix column ',colNum,' does not sum to one')
                    raise MarkovError
            self.ProbMatrix = np.array(iMat)
            self.probMatrixSet = True
        if self.probMatrixSet and self.initStateSet: self.Evaluate()

    def SetInitState(self,initState):        
        if initState == None:
            print ('Initialised with no initial state')
            self.initState = None
        else:
            if sum(initState) != 1.:
                print ('Initial state needs to add to one')
                raise MarkovError
            self.initState = initState
            self.initStateSet = True
        if self.probMatrixSet and self.initStateSet: self.Evaluate()

    def Evaluate(self):
        eigVals, eigVecs = np.linalg.eig(self.ProbMatrix)
        #eigVecs returned by this function are columns, not rows
        eigVecs = [eigVecs[:,i] for i in range(len(eigVecs))]
        #First component 1 for each eigenvector, for readability
        for e in range(len(eigVecs)):
            #Find first non-zero element
            nonZeroElement = 0
            for i in range(len(eigVecs[e])):
                if eigVecs[e][i] != 0.:
                    nonZeroElement = i
                    break
            eigVecs[e] = [elem/eigVecs[e][nonZeroElement] for elem in eigVecs[e]]       
        #c = inv(eigVecs) * initState        
        consts = np.linalg.inv(eigVecs).transpose().dot(self.initState)
        self.Evaluation = consts, eigVals, eigVecs

    def CalcStateAtTime(self,t):
        consts, eigVals, eigVecs = self.Evaluation
        constTimesEigvec = []
        for c, eigVal, eigVec in zip(consts, eigVals, eigVecs):
            constTimesEigvec.append([c*(eigVal**t)*v for v in eigVec])
        result = np.zeros(len(consts))
        for a in constTimesEigvec:
            result = result + a
        return np.real(result)

    def StationaryState(self):
        consts, eigVals, eigVecs = self.Evaluation

        for e in range(len(eigVals)):
            if eigVals[e] == 1:
                toReturn = np.real(consts[e])*np.array(eigVecs[e])
        return np.real(toReturn)

    def PrintStateAtTime(self):
        consts, eigVals, eigVecs = self.Evaluation
        result = []
        for c, eigVal, eigVec in zip(consts, eigVals, eigVecs):
            result .append( str(c)+'*('+str(eigVal)+'^t)*'+str(eigVec)+' ' )
        print ('P(t) = '+'+'.join(result))

if __name__ == '__main__':
    #Example
    Mat = [[2./3,1./2],[1./3,1./2]]
    iState = [1,0]
    x = MarkovChain(Mat,iState)
    print ('Initial state: ',x.initState)
    print ('Probability matrix: ',x.ProbMatrix)
    print ('Constants: ', x.Evaluation[0])
    print ('Eigenvalues: ', x.Evaluation[1])
    print ('Eigenvectors: ', x.Evaluation[2])
    print ('Equation with time: ')
    x.PrintStateAtTime()
    print (x.StationaryState())






