import numpy

data = numpy.load('PPO2.npz')
lst = data["obs"]
print(lst)
