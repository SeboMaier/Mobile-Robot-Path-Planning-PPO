import pandas as pd
import matplotlib.pyplot as plt

dataframe = pd.read_csv('MP_5M_norm_fixedlr.csv', skiprows=1, delimiter=",")

x = dataframe.Step
y = dataframe.Value
plt.scatter(x, y)
plt.show()  # or plt.savefig("name.png")
