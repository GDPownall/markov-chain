#!/usr/bin/env python

from MarkovClass import MarkovChain
import numpy as np

def dice_roll_prob(n):
    '''
    Return probability of getting n when rolling two dice
    '''
    if n < 2 or n > 12: return 0
    if n <= 7: p = n-1
    else:      p = 13-n
    return p/36

class Monopoly:
    def __init__(self):
        self.three_doubles_jail = True

        self.n_chance         = 16
        self.chance_locs      = [2,7,17,22,36]
        self.chance_advances  = [0, 24, 11, 10]

class Monopoly_MarkovChain(Monopoly):
    def __init__(self):
        super().__init__()
        initial_state = [1.] + 39*[0.]
        # Set up probability matrix

        prob_mat = [[0.]*40 for i in range(40)]
        for n in range(40):
            for m in range(2,13):
                if n+m < 40: prob_mat[n+m][n]    = dice_roll_prob(m)
                else:        prob_mat[n+m-40][n] = dice_roll_prob(m)

        # Roll three doubles (probability 1/6**3), go to jail
        if self.three_doubles_jail:
            for n in range(40):
                prob_mat[10][n] += (1/6)**3
                for m in range(40):
                    prob_mat[m][n] *= (1-(1/6)**3)

        # Go to jail square
        # Unoptimised second loop because this is a relatively short loop anyway
        for n in range(40):
            prob_mat[10][n] += prob_mat[30][n]
            prob_mat[30][n] = 0

        # Chance cards 
        n_chance = self.n_chance 
        chance_locs     = self.chance_locs 
        chance_advances = self.chance_advances 
        for n in range(40):
            for chance in chance_locs:
                for advance in chance_advances:
                    p_advance_to = prob_mat[chance][n]/n_chance
                    prob_mat[advance][n] += p_advance_to
                    prob_mat[chance][n] = prob_mat[chance][n]*(1-1/n_chance)
        
        self.initial_state = initial_state
        self.prob_matrix = prob_mat
        self.markov = MarkovChain(prob_mat,initial_state)

    def plots(self):
        print(self.markov.StationaryState())
        self.markov.PlotStationary('docs/MonopolyStationary.png')
        self.markov.PlotOverTime('docs/MonopolyOverTime.gif',40, start_from = 1, time_between_steps = 500)



class Monopoly_MonteCarlo(Monopoly):
    def __init__(self, num_players=10):
        super().__init__()
        self.num_players = num_players
        self.game_states = np.zeros((1,num_players),int) 
        self.rolls1      = np.zeros((1,num_players),int)
        self.rolls2      = np.zeros((1,num_players),int)

    def advance(self):
        prev_turn = self.game_states[-1,:]

        roll_sample = np.random.choice(
                [1,2,3,4,5,6],
                size = (2,self.num_players))
        self.rolls1 = np.vstack([self.rolls1,roll_sample[0,:]])
        self.rolls2 = np.vstack([self.rolls2,roll_sample[1,:]])

        next_turn = prev_turn + roll_sample[0,:] + roll_sample[1,:]
        next_turn = self.replacements(next_turn)

        self.game_states = np.vstack([self.game_states,next_turn])

    def replacements(self,arr):
        '''
        For a given array of positions, make replacements for go to jail, advance to ..., etc.
        '''
        #Subtract 40 from those which have looped around the board
        arr2 = np.where(
                arr > 39,
                arr - 40,
                arr)
        # Go to jail square
        arr2 = np.where(arr2==30,10,arr2)
        # Advance to x chance/comm chest
        choose_advance  = np.random.choice(np.arange(0,self.n_chance),size = (1,self.num_players)) == 0
        advance_to_locs = np.random.choice(self.chance_advances, size = (1,self.num_players))
        arr2 = np.where(
                np.isin(arr2,self.chance_locs)*choose_advance,
                advance_to_locs,
                arr2)
        # Roll three doubles jail
        if self.three_doubles_jail and self.rolls1.shape[0] > 2:
            arr2 = np.where(
                    np.all(self.rolls1[-3:,:] == self.rolls2[-3:,:],axis=0),
                    10,
                    arr2)
   
        return arr2
            
    def CalcStateAtTime(self,t):
        while self.game_states.shape[0] < t+1:
            self.advance()

        state = self.game_states[t,:]
        counts = []
        for i in range(40):
            counts.append((state==i).sum())
        counts = counts/sum(counts)
        return counts



if __name__ == '__main__':
    x = Monopoly_MarkovChain()
    print(x.markov.CalcStateAtTime(20))
    monte = Monopoly_MonteCarlo(100000)
    for i in range(10):
        monte.advance()
    print(monte.CalcStateAtTime(20))
