
import numpy as np
import math as mh

A0 = 3
W = 401
H = 401

B = np.array([[1, 1],
              [0, 0]])

D = np.array([[0, 0],
              [1, 1]])

S = np.array([[1, 0],
              [0, 1]])


def Ai(POPOLAZIONE):
    G = POPOLAZIONE[0]
    return (
        np.roll(G, -1, axis=0) +   # i+1, j
        np.roll(G, +1, axis=0) +   # i-1, j
        np.roll(G, -1, axis=1) +   # i, j+1
        np.roll(G, +1, axis=1) +   # i, j-1
        np.roll(np.roll(G, -1, axis=0), -1, axis=1) +  # i+1, j+1
        np.roll(np.roll(G, -1, axis=0), +1, axis=1) +  # i+1, j-1
        np.roll(np.roll(G, +1, axis=0), -1, axis=1) +  # i-1, j+1
        np.roll(np.roll(G, +1, axis=0), +1, axis=1)    # i-1, j-1
    )

    
def V(giorno):
    if giorno <= 90:
        return 1
    elif giorno <= 106:
        return 0.9
    elif giorno <= 113:
        return 0.85
    elif giorno <= 120:
        return 0.75
    elif giorno <= 134:
        return 0.88
    elif giorno <= 141:
        return 0.86
    elif giorno <= 155:
        return 0.85
    elif giorno <= 180:
        return 0.86
    elif giorno <= 190:
        return 0.85
    elif giorno <= 211:
        return 0.8
    elif giorno <= 230:
        return 0.75
    elif giorno <= 252:
        return 1
    elif giorno <= 259:
        return 0.80
    elif giorno <= 280:
        return 0.98
    elif giorno <= 308:
        return 1
    elif giorno <= 322:
        return 1.15
    else:
        return 1.2


def G(POPOLAZIONE, giorno):
    v = V(giorno)
    A = Ai(POPOLAZIONE)
    A_ = A[:, :, np.newaxis, np.newaxis]

    cond1 = A_ <= A0 - 2*v
    cond2 = (A_ > A0 - 2*v) & (A_ <= A0 - v)
    cond3 = (A_ > A0 - v)   & (A_ <= A0)
    cond4 = (A_ > A0)       & (A_ <= A0 + v)
    cond5 = A_ >= A0 + v

    
    Gi = np.where(cond1, D, np.zeros([W,H,2,2])) 
    Gi = np.where(cond2, (mh.sqrt(2)+1)*(A0 - v - A_)*D + (A_ - A0 + 2*v)*S, Gi) 
    Gi = np.where(cond3, (mh.sqrt(2)+1)*(A0 - A_)*S + (A_ - A0 + v)*B, Gi) 
    Gi = np.where(cond4, (mh.sqrt(2)+1)*(A0 + v - A_)*B + (A_ - A0)*D, Gi)
    Gi = np.where(cond5, D, Gi)
    
    return Gi

def esperimento(giorni):
    POPOLAZIONE = np.zeros([2,W,H])
    POPOLAZIONE[0] = np.random.rand(W,H)
    POPOLAZIONE[1] = np.sqrt(1 - POPOLAZIONE[0]**2)
    
    STORICO = np.zeros([giorni,W,H])

    STORICO[0] = POPOLAZIONE[0]
    for i in range(1,giorni):
        Gi = G(POPOLAZIONE,i)
        P0 = Gi[:,:,0,0]*POPOLAZIONE[0] + Gi[:,:,0,1]*POPOLAZIONE[1]
        P1 = Gi[:,:,1,0]*POPOLAZIONE[0] + Gi[:,:,1,1]*POPOLAZIONE[1]
    
        N = np.sqrt(P0**2 + P1**2)
        POPOLAZIONE[0] = P0/N
        POPOLAZIONE[1] = P1/N

        STORICO[i] = POPOLAZIONE[0] 


    return STORICO,POPOLAZIONE