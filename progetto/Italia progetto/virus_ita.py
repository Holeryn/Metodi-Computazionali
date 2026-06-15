import numpy as np
import math as mh
import matplotlib.pyplot as plt
import random
from scipy.special import gamma

s = 0.341
Vp = 0.25
Ve = 3
Vl = 13
Dv = 48
Vm = 1050
Vs = 5

# Parametri P(x)
alpha = 4.0
beta = 0.19

def Xi(VIRUS):
    V = VIRUS
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
    VIRUS_LAYERS  = np.zeros((giorni_totali, 401, 401))
    N_LAYERS      = np.zeros((giorni_totali, 401, 401))
    
    indici = np.random.choice(401*401, size=100, replace=False)
    VIRUS_LAYERS[Dv].flat[indici] = 1
    
    POP_ZERO = np.zeros((401, 401), dtype=int)

    for i in range(Dv + 1, giorni_totali):
        if i % Vs == 0:
            indici_nuovi = np.random.choice(401*401, size=1, replace=False)
            VIRUS_LAYERS[i].flat[indici_nuovi] = 1

        eta            = i - np.arange(i)[:, np.newaxis, np.newaxis]
        infettivi_mask = (eta > Ve) & (eta <= Ve + Vl)
        VIRUS_INFETTI  = (VIRUS_LAYERS[:i] * infettivi_mask).sum(axis=0)
        Xi_val         = Xi(VIRUS_INFETTI)
        
        N = Vp * Xi_val * STORICO[i]

        # ---- SPOSTATO QUI: regola 4 applicata PRIMA di salvare N_LAYERS ----
        POP_ZERO = np.where(STORICO[i] == 0, POP_ZERO + 1, 0)
        maschera_morte = POP_ZERO >= 3
        N[maschera_morte] = 0
        # ---------------------------------------------------------------------

        # ---- N_LAYERS salvato DOPO la regola 4, così è corretto ----
        N_LAYERS[i] = N
        VIRUS_LAYERS[i] += N
        # --------------------------------------------------------------

        # ---- SPOSTATO QUI: prima azzera i layer vecchi, poi calcola il cap ----
        eta_full = i - np.arange(i+1)[:, np.newaxis, np.newaxis]
        VIRUS_LAYERS[:i+1] = np.where(eta_full > Ve + Vl, 0, VIRUS_LAYERS[:i+1])

        totale = VIRUS_LAYERS[:i+1].sum(axis=0)
        eccesso_mask = totale > Vm
        if eccesso_mask.any():
            scala = np.where(eccesso_mask, Vm / totale, 1.0)
            VIRUS_LAYERS[:i+1] *= scala[np.newaxis, :, :]
        # -----------------------------------------------------------------------

    return N_LAYERS, VIRUS_LAYERS

def P(x):
    return (beta**alpha)/gamma(alpha) * x**(alpha-1) * np.exp(-beta*x)