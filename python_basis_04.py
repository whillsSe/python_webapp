import pandas as pd
import matplotlib.pyplot as plt
df_data = pd.read_csv('./input/sample1.csv',header=None,names=['depth','temp','concentration'])
dx = df_data.iloc[:,0].values
dy1 = df_data.iloc[:,1].values
dy2 = df_data.iloc[:,2].values

fig,ax1 = plt.subplots()

ax1.plot(dx,dy1,'b-')
ax1.set_xlabel('X')
ax1.set_ylabel('Y1',color='b')
ax1.tick_params('y',colors='b')

ax2 = ax1.twinx()
ax2.plot(dx,dy2,'r-')
ax2.set_ylabel('Y2',color='r')
ax2.tick_params('y',colors='r')

fig.tight_layout()
plt.show()