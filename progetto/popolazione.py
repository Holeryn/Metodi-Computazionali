import numpy as np
import math as mh
import matplotlib.pyplot as plt

A0 = 3
W = 401
H = 401

POPOLAZIONE = np.zeros([2,W,H])
B = np.array([[1,1],[0,0]])         # Nascita
D = np.array([[0,0],[1,1]])         # Morte
S = np.array([[1,0],[0,1]])         # Sopravvivenza (a.k.a Identità nello spazio vettoriale delle matrici 2*2)

def Ai(i,j):
    return (POPOLAZIONE[0][(i + 1)%W][j] +
            POPOLAZIONE[0][i][(j+1)%H] +
            POPOLAZIONE[0][(i+1)%W][(j+1)%H] +
            POPOLAZIONE[0][(i-1)%W][j] +
            POPOLAZIONE[0][i][(j-1)%H] +
            POPOLAZIONE[0][(i-1)%W][(j-1)%H] +
            POPOLAZIONE[0][(i+1)%W][(j-1)%H] +
            POPOLAZIONE[0][(i-1)%W][(j+1)%H])

def V(giorno):
    if giorno <= 23:
        return 1
    elif giorno > 23 and giorno <= 115:
        return 0.85
    elif giorno > 115 and giorno <= 126:
        return 0.009*giorno - 0.185
    elif giorno > 126 and giorno <= 156:
        return 0.002*giorno + 0.688
    elif giorno > 156 and giorno <= 186:
        return 0.007*giorno - 0.092
    else: 
        return 1.2

def G(i,j,giorno):
    A = Ai(i,j)

    if A <= (A0 - 2*V(giorno)):
        return D
    elif (A > (A0-2*V(giorno))) and (A <= A0 - V(giorno)):
        return (mh.sqrt(2) + 1)*(A0 - V(giorno) - A)*D + (A - A0 + 2*V(giorno))*S
    elif (A > (A0 - V(giorno))) and (A <= A0):
        return (mh.sqrt(2) + 1)*(A0 - A)*S + (A-A0+V(giorno))*B
    elif A >= A0 and (A <= (A0 + V(giorno))):
        return (mh.sqrt(2) + 1)*(A0 + V(giorno) - A)*B + (A - A0)*D
    elif A >= (A0 + V(giorno)):
        return D
    else: 
        return S                # Ritorna stato corrente


def esperimento(giorni):
    POPOLAZIONE[0][:][:] = 1

    for g in range(giorni):
        for i in range(W):
            for j in range(H):
                U = G(i,j,g)
                [POPOLAZIONE[0][i][j],POPOLAZIONE[1][i][j]] = U@np.array([POPOLAZIONE[0][i][j],POPOLAZIONE[1][i][j]])
    
    return POPOLAZIONE

esperimento(15)
"""
X = np.linspace(0,190,100)
Y = np.zeros(len(X))
i = 0
for x in X:
    Y[i] = V(x)
    i = i + 1

plt.plot(X,Y)
plt.show()
"""
