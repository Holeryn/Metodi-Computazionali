import numpy as np
import math as mh
import matplotlib.pyplot as plt
from scipy.special import gamma


s = 0.341
Vp = 0.23
Ve = 3
Vl = 13
Dv = 52
Vm = 950
Vs = 5

alpha = 4.938
beta = 0.2627

def Xi(VIRUS):
    V = VIRUS

# Faccio la somma dei primi vicini
    return (
        np.roll(V,  1, axis=0) +
        np.roll(V, -1, axis=0) +
        np.roll(V,  1, axis=1) +
        np.roll(V, -1, axis=1) +
        np.roll(np.roll(V,  1, axis=0),  1, axis=1) +
        np.roll(np.roll(V,  1, axis=0), -1, axis=1) +
        np.roll(np.roll(V, -1, axis=0),  1, axis=1) +
        np.roll(np.roll(V, -1, axis=0), -1, axis=1)
    )


def setup_virus(giorni_totali, STORICO):
    VIRUS_LAYERS  = np.zeros((giorni_totali, 401, 401)) # VIRUS_LAYERS CONTIENE 1 E 0 giorno per giorno dei virus nella griglia
    N_LAYERS      = np.zeros((giorni_totali,401,401))  # N per cella per giorno
    
    indici = np.random.choice(401*401, size=100)
    VIRUS_LAYERS[Dv].flat[indici] = 1
    
    POP_ZERO = np.zeros((401, 401), dtype=int)

    for i in range(Dv + 1, giorni_totali):
        if i % Vs == 0:     # Ogni Vs giorni inserisco casualmente un virus al giorni i
            indici_nuovi = np.random.choice(401*401, size=1)
            VIRUS_LAYERS[i].flat[indici_nuovi] = 1

        eta           = i - np.arange(i)[:, np.newaxis, np.newaxis]         # differenze tra giorno corrente e tutti i precedenti, cosi posso confrontare col passato, (time machine whooooooo)
        infettivi_mask = (eta > Ve) & (eta <= Ve + Vl)
        VIRUS_INFETTI  = (VIRUS_LAYERS[:i] * infettivi_mask).sum(axis=0)
        Xi_val         = Xi(VIRUS_INFETTI)
        
        N                = Vp * Xi_val * STORICO[i] 
        N_LAYERS[i]      = N                        
        VIRUS_LAYERS[i] += N

        totale = VIRUS_LAYERS[:i+1].sum(axis=0)
        eccesso_mask = totale > Vm
        if eccesso_mask.any():  # Taglio le celle con più di Vm virus
            scala = np.where(eccesso_mask, Vm / totale, 1.0)
            VIRUS_LAYERS[:i+1] *= scala[np.newaxis, :, :]

        eta_full = i - np.arange(i+1)[:, np.newaxis, np.newaxis]
        VIRUS_LAYERS[:i+1] = np.where(eta_full > Ve + Vl, 0, VIRUS_LAYERS[:i+1])

        POP_ZERO = np.where(STORICO[i] == 0, POP_ZERO + 1, 0)
        maschera_morte = POP_ZERO >= 3
        VIRUS_LAYERS[i][maschera_morte] = 0
        N[maschera_morte] = 0

    return N_LAYERS, VIRUS_LAYERS

def P(x):
    return (beta**alpha)/gamma(alpha) * x**(alpha-1) * np.exp(-beta*x)