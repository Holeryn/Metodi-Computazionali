
import numpy as np
import math as mh

A0 = 3
W = 401
H = 401

POPOLAZIONE = np.zeros((2, W, H))
VECCHIA = np.zeros((2, W, H))

B = np.array([[1, 1],
              [0, 0]])

D = np.array([[0, 0],
              [1, 1]])

S = np.array([[1, 0],
              [0, 1]])


def Ai(i, j):
    return (
        VECCHIA[0, (i+1) % W, j] +
        VECCHIA[0, (i-1) % W, j] +
        VECCHIA[0, i, (j+1) % H] +
        VECCHIA[0, i, (j-1) % H] +
        VECCHIA[0, (i+1) % W, (j+1) % H] +
        VECCHIA[0, (i+1) % W, (j-1) % H] +
        VECCHIA[0, (i-1) % W, (j+1) % H] +
        VECCHIA[0, (i-1) % W, (j-1) % H]
    )



def V(giorno):
    if giorno <= 113: #23
        return 1
    elif giorno <= 207: #115
        return 0.85
    elif giorno <= 218: #126
        return 0.009 * giorno - 0.185
    elif giorno <= 248: #156
        return 0.002 * giorno + 0.688
    elif giorno <= 278: #186
        return 0.007 * giorno - 0.092
    else:
        return 1.2


def G(i, j, giorno):

    A = Ai(i, j)
    v = V(giorno)

    if A <= A0 - 2*v:
        return D

    elif A <= A0 - v:
        return (
            (mh.sqrt(2)+1)*(A0-v-A)*D +
            (A-A0+2*v)*S
        )

    elif A <= A0:
        return (
            (mh.sqrt(2)+1)*(A0-A)*S +
            (A-A0+v)*B
        )

    elif A < A0 + v:
        return (
            (mh.sqrt(2)+1)*(A0+v-A)*B +
            (A-A0)*D
        )

    else:
        return D


def esperimento(giorni):

    global VECCHIA

    POPOLAZIONE[0] = np.random.rand(W, H)
    POPOLAZIONE[1] = 1.0 - POPOLAZIONE[0]

    STORICO = np.zeros([giorni,W,H])

    for g in range(giorni):

        VECCHIA = POPOLAZIONE.copy()

        for i in range(W):
            for j in range(H):

                U = G(i, j, g)

                POPOLAZIONE[:, i, j] = U @ VECCHIA[:, i, j]

                # normalizzazione probabilistica
                s = mh.sqrt(POPOLAZIONE[0, i, j]**2 + POPOLAZIONE[1, i, j]**2)

                if s > 0:
                    POPOLAZIONE[:, i, j] /= s
        STORICO[g] = VECCHIA[0].copy()

    return STORICO,POPOLAZIONE