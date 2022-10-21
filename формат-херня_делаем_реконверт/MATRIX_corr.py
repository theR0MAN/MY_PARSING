import pandas as pd
import numpy as np

data = {'A': [1, 2, 3, 4],
        'B': [38, 31, 26, 90],
        'C': [10, 15, 17, 100],
        'D': [60, 99, 23, 56],
        'E': [76, 98, 78, 90]
        }




df = pd.DataFrame(data)
M = df.corr()
print( M)

# z=M.sort_values(by = "B", ascending=False)
# print(z)

cols = M.columns
# print(cols)

for i in M.columns:
        print(i)


# z=dict(M['A'].sort_values( ascending=False))
# print(z)



for i in M.columns:
        z=dict(M[i].sort_values( ascending=False))
        print(z)