#!/usr/bin/env python

from MarkovClass import MarkovChain

class Monopoly:
    def __init__(self):
        initial_state = [1.] + 39*[0.]
        # Set up probability matrix

        prob_mat = [[0.]*40 for i in range(40)]
        for n in range(40):
            for m in range(2,13):
                if n+m < 40: prob_mat[n+m][n]    = dice_roll_prob(m)
                else:        prob_mat[n+m-40][n] = dice_roll_prob(m)

        # Go to jail square
        for n in range(40):
            prob_mat[10][n] += prob_mat[30][n]
            prob_mat[30][n] = 0
        # Chance cards 
        n_chance = 16
        chance_locs     = [2,7,17,22,36]
        chance_advances = [0, 24, 11]
        for n in range(40):
            for chance in chance_locs:
                for advance in chance_advances:
                    p_advance_to = prob_mat[chance][n]/n_chance
                    prob_mat[advance][n] += p_advance_to
                    prob_mat[chance][n] = prob_mat[chance][n]*(1-1/n_chance)
        
        self.initial_state = initial_state
        self.prob_matrix = prob_mat
        self.markov = MarkovChain(prob_mat,initial_state)

        print(self.markov.StationaryState())
        self.markov.PlotStationary('docs/MonopolyStationary.png')
        self.markov.PlotOverTime('docs/MonopolyOverTime.gif',100, start_from = 1)




def dice_roll_prob(n):
    if n < 2 or n > 12: return 0
    if n <= 7: p = n-1
    else:      p = 13-n
    return p/36


if __name__ == '__main__':
    x = Monopoly()
