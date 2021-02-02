#!/usr/bin/env python

from Monopoly import *
import time
import psutil

start_CPU = psutil.virtual_memory().used
print('CPU at start' , start_CPU/10**6)

start_time = time.time()
x = Monopoly_MarkovChain()
x.markov.CalcStateAtTime(40)
print('Time to calculate state at 40 iterations with Markov Chain: ',time.time()-start_time)
used_CPU = (psutil.virtual_memory().used - start_CPU)/10**6
print('CPU usage:', used_CPU)

start_time = time.time()
monte = Monopoly_MonteCarlo(100000)
monte.CalcStateAtTime(40)
print('Time to calculate state at 40 iterations with Monte Carlo: ',time.time()-start_time)
print('CPU usage:',(psutil.virtual_memory().used - used_CPU)/10**6)
