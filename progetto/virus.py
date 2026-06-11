import numpy as np
import math as mh
import matplotlib.pyplot as plt

s = 0.341
Vp = 0.23
Ve = 3
Vl = 13
Dv = 52         # A noi è diverso????
Vm = 950
Vs = 5

def Xi(VECCHIA,VIRUS_MASK):
    V = VECCHIA
    VM = VIRUS_MASK

    return (
        np.roll(V,  1, axis=0) * np.roll(VM,  1, axis=0) +
        np.roll(V, -1, axis=0) * np.roll(VM, -1, axis=0) +
        np.roll(V,  1, axis=1) * np.roll(VM,  1, axis=1) +
        np.roll(V, -1, axis=1) * np.roll(VM, -1, axis=1) +
        np.roll(np.roll(V,  1, axis=0),  1, axis=1) * np.roll(np.roll(VM,  1, axis=0),  1, axis=1) +
        np.roll(np.roll(V,  1, axis=0), -1, axis=1) * np.roll(np.roll(VM,  1, axis=0), -1, axis=1) +
        np.roll(np.roll(V, -1, axis=0),  1, axis=1) * np.roll(np.roll(VM, -1, axis=0),  1, axis=1) +
        np.roll(np.roll(V, -1, axis=0), -1, axis=1) * np.roll(np.roll(VM, -1, axis=0), -1, axis=1)
    )

def Setup(POPOLAZIONE,STORICO,giorno):
    VIRUS = np.zeros([401,401])         #3D: 1 : contagioso , 0: Non contagioso
                                        #4D: giorno in cui inizia il contagio
    VIRUS_MASK = np.zeros([401,401])
    GIORNO_MASK = np.full([401,401],-999)
    MASK = np.zeros([401,401])
    POP_MASK = np.zeros([401,401])
                                               

    if(giorno < Dv):
        return VIRUS
    
    VIRUS[::40, ::40] = 1                   # GIORNO 52(DV) Aggiungi 1 ogni 1600
    VIRUS_MASK[::40,::40] = 0               # Non cotagioso
    GIORNO_MASK[::40,::40] = Dv             # Nace a Dv
    MASK[::40,::40] = 1                     # Nom modificare più
    POP_MASK[::40,::40] = 3
    
    for i in range(Dv + 1, giorno-2):
        X_i = Xi(VIRUS,VIRUS_MASK)
        N = Vp*X_i*POPOLAZIONE[0]
        VIRUS = VIRUS + N
        GIORNO_MASK = np.where((VIRUS != 0) & (MASK == 0),i,GIORNO_MASK)
        VIRUS_MASK = np.where((i > (GIORNO_MASK + Ve + 1)) & (i < (GIORNO_MASK + Ve + Vl + 1)),1,0)
        VIRUS = np.where(VIRUS_MASK == 0, 0,VIRUS)
        MASK = np.where((VIRUS != 0) & (MASK == 0), 1, MASK)

        POP_MASK = np.where((STORICO[i] == 0) & (POP_MASK >= 0),POP_MASK - 1,POP_MASK)
        VIRUS = np.where(POP_MASK != 0, VIRUS,0)





          


