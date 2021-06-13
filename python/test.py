#!/usr/bin/env python
import numpy as np

x = np.array([[1,2,3],[4,5,6],[7,8,9]])
y = np.array([[1,2,4],[4,2,8],[7,2,9]])

print(x)
print(y)

z = (x[-3:] == y)
print(z)
print(np.all(z,axis=0))
