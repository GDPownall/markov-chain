#!/usr/bin/env python

from Monopoly import *
import time
import psutil

start_RAM = psutil.virtual_memory().used
print('RAM at start' , start_RAM/10**6)

start_time = time.time()
x = Monopoly_MarkovChain()
x.markov.CalcStateAtTime(40)
print('Time to calculate state at 40 iterations with Markov Chain: ',time.time()-start_time)
used_RAM = (psutil.virtual_memory().used - start_RAM)
print('RAM usage:', used_RAM*10**-6)

start_time = time.time()
monte = Monopoly_MonteCarlo(100000)
monte.CalcStateAtTime(40)
print('Time to calculate state at 40 iterations with Monte Carlo: ',time.time()-start_time)
print('RAM usage:',(psutil.virtual_memory().used - used_RAM - start_RAM)*10**-6)
