#!/usr/bin/env python

from MarkovClass import MarkovChain
import numpy as np


def page_rank_algo(page_dict):
    '''
    Takes input dictionary of format
    {webpage1: [link1, link2, link3, ...],
    webpage2: [link1, link2, link3, ...], ...}
    And uses markov chain analysis to solve probability of being on each page at infinite time
    '''

    # Simple checks
    pages = list(page_dict.keys())
    links = []
    for p in pages:
        if any([x not in pages for x in page_dict[p]]):
            raise ValueError('One of the links provided is not in the list of pages being evaluated.')

    # Create matrix
    columns = {}
    for p in pages:
        columns[p] = [0.] * len(pages)
        for q in range(len(pages)):
            columns[p][q] = float(page_dict[p].count(pages[q]))/len(page_dict[p])

    prob_matrix = np.transpose([columns[p] for p in pages])
    init = [1.] + [0.]*(len(pages)-1)

    m = MarkovChain(prob_matrix,init)

    toReturn = {}
    for p,x in zip(pages,m.StationaryState()):
        toReturn[p] = x
    return toReturn 
            




if __name__ == '__main__':
    example = {
            'A' : ['B', 'C', 'D'],
            'B' : ['A', 'C'],
            'D' : ['A', 'B'],
            'C' : ['A', 'D']
            }
    print (page_rank_algo(example))

