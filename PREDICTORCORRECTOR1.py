import numpy as np
import matplotlib.pyplot as plt
import math

N = 10000
J = 5
x = np.zeros(N)
v = np.zeros(N)

dt = 2*math.pi/N
x[0] = 0
v[0] = 1

for i in range(N - 1):
    # PREDICT: algortimo di eulero
    x[i+1] = x[i]+v[i]*dt
    v[i+1] = v[i]-x[i]*dt

    # correzzione: metodo di picard
    # mi fermo alla prima evoluzione
    # ossia approsimo tramite il metodo dei trapezi
    # Le approssimazioni successive (i.e simpson) 
    # hanno bisogno di piu punti quindi una volta che ho
    # trovato questa potrei cercarne delle altre
    x[i+1] = x[i] + (v[i] + v[i+1])*dt/2
    v[i+1] = v[i] - (x[i]+ x[i+1])*dt/2
    

T = np.linspace(0,N,N)
plt.scatter(T*dt,x)
plt.scatter(T*dt,v)
plt.show()