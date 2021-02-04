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
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
            if len(iMat.shape) != 2 or (iMat.shape[0] != iMat.shape[1]):
                raise ValueError('Matrix supplied to Markov Chain class not square')
            total_cols = iMat.sum(axis=0)
            sums_to_one = np.absolute((total_cols - 1)) < 0.000001
            if not all(sums_to_one):
                raise ValueError('Matrix column at position(s) '+str(np.argwhere(~sums_to_one).ravel())+' does not sum to one.')
            self.ProbMatrix = np.array(iMat)
            self.probMatrixSet = True
        if self.probMatrixSet and self.initStateSet: self.Evaluate()

    def SetInitState(self,initState):        
        if initState == None:
            print ('Initialised with no initial state')
            self.initState = None
        else:
            if np.absolute(sum(initState)-1) > 0.000001:
                raise ValueError('Initial state does not sum to one')
            self.initState = np.array(initState)
            self.initStateSet = True
        if self.probMatrixSet and self.initStateSet: self.Evaluate()

    def Evaluate(self):
        eigVals, eigVecs = np.linalg.eig(self.ProbMatrix)
        # Sort eigenvalues and associate vectors
        idx = eigVals.argsort()[::-1]
        eigVals = eigVals[idx]
        eigVecs = eigVecs[:,idx]
        eigVecs = eigVecs.transpose()        
        consts = self.initState.dot(np.linalg.inv(eigVecs))
        self.Evaluation = consts, eigVals, eigVecs
        self.RenormEigvecs()

    def RenormEigvecs(self):
        consts, eigVals, eigVecs = self.Evaluation
        # Find renorm values. Not as simple as just finding max, has to deal with negative numbers too.
        maxmin = np.array([np.max(eigVecs,axis=1),np.min(eigVecs,axis=1)])
        take_val = np.argmax(np.abs(maxmin),axis=0)
        renorms = maxmin[take_val, range(maxmin.shape[1])] 
        # Now renormalise
        eigVecs = (eigVecs.T*1./renorms).T
        consts = self.initState.dot(np.linalg.inv(eigVecs))
        self.Evaluation = consts, eigVals, eigVecs

    def CalcStateAtTime(self,t):
        consts, eigVals, eigVecs = self.Evaluation
        a = consts*eigVals**t        
        result = np.zeros(eigVecs.shape[0])
        for i in range(len(consts)):
            result += np.real(consts[i]*(eigVals[i]**t)*eigVecs[i,:])
        return result

    def StationaryState(self):
        consts, eigVals, eigVecs = self.Evaluation
        
        stationary_args = np.abs(eigVals-1) < 0.000001
        toReturn = np.zeros(len(eigVecs[0,:]))
        for e in range(len(stationary_args)):
            if stationary_args[e]: toReturn += np.real(consts[e]*np.array(eigVecs[e]))
        return np.real(toReturn)

    def PrintStateAtTime(self):
        consts, eigVals, eigVecs = self.Evaluation
        result = []
        for c, eigVal, eigVec in zip(consts, eigVals, eigVecs):
            result .append( str(c)+'*('+str(eigVal)+'^t)*'+str(eigVec)+' ' )
        print ('P(t) = '+'\n+'.join(result))

    def PlotStationary(self, outfile = 'out.pdf'):
        stationary = self.StationaryState()
        fig, ax = plt.subplots()
        fig.set_tight_layout(True)
        plt.title('Stationary state')
        plt.xlabel('Position')
        plt.ylabel('Probability')
        line = ax.plot(range(len(stationary)),stationary,linewidth=2)
        fig.savefig(outfile)

    def PlotOverTime(self, outfile='out.gif', timesteps=20, start_from=0, time_between_steps=200):
        fig, ax = plt.subplots()
        print('fig size: {0} DPI, size in inches {1}'.format(
            fig.get_dpi(), fig.get_size_inches()))
        x = range(len(self.Evaluation[0]))
        y = self.CalcStateAtTime(start_from)
        line, = ax.plot(x,y,linewidth=2)
        ax.set_xlabel('Position')
        ax.set_ylabel('Probability')
        def update(i):
            label = 'timestep {0}'.format(i)
            line.set_ydata(self.CalcStateAtTime(i))
            ax.set_title(label)
            return line,ax
        anim = FuncAnimation(fig, update, frames=np.arange(start_from,timesteps), interval=time_between_steps)
        #plt.show()
        anim.save(outfile, dpi=100, writer='imagemagick')

if __name__ == '__main__':
    #Example
   
    Mat = [
            [1./3,1./2,1./10],
            [1./3,1./4,2./10],
            [1./3,1./4,7./10]]
    iState = [1,0,0]
    
    x = MarkovChain(Mat,iState)
    print ('Initial state: ',x.initState)
    print ('Probability matrix:\n ',x.ProbMatrix)
    print ('Constants: ', x.Evaluation[0])
    print ('Eigenvalues: ', x.Evaluation[1])
    print ('Eigenvectors: ', x.Evaluation[2])
    print ('Equation with time: ')
    x.PrintStateAtTime()
    print ('Stationary state:',x.StationaryState())






