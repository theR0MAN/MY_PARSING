import pandas as pd

data = {'assists': [4, 5, 5, 6, 7, 8, 8, 10],
        'rebounds': [12, 14, 13, 7, 8, 8, 9, 13],
        'points': [22, 24, 26, 26, 29, 32, 20, 14]
        }

df = pd.DataFrame(data, columns=['assists','rebounds','points'])
print (df )

print (df.corr().round(3) )
# corr = df.corr()
# corr.style.background_gradient(cmap='coolwarm')
# print (corr.round(3) )