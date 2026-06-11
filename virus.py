import numpy as np
import math as mh
import matplotlib.pyplot as plt

s = 0.341
Vp = 0.23
Ve = 3
Vl = 13
Dv = 52
Vm = 950
Vs = 5

def Xi(VECCHIA, VIRUS_MASK):
    V  = VECCHIA
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

def Setup(POPOLAZIONE, STORICO, giorno):
    VIRUS       = np.zeros((401, 401))
    VIRUS_MASK  = np.zeros((401, 401))
    GIORNO_MASK = np.full((401, 401), -999)  # -999 = mai infettato
    MASK        = np.zeros((401, 401))
    POP_MASK    = np.full((401, 401), 3)     # contatore 3 giorni popolazione

    if giorno < Dv:
        return VIRUS

    # Regola 1: pianta virus al giorno Dv
    indici = np.random.choice(VIRUS.size, size=100, replace=False)

    VIRUS.flat[indici] = 1
    GIORNO_MASK.flat[indici] = Dv
    MASK.flat[indici]        = 1

    for i in range(Dv + 1, giorno):

        # Regola 2: propaga virus
        X_i   = Xi(VIRUS, VIRUS_MASK)

        N     = Vp * X_i * STORICO[i]     
        VIRUS = VIRUS + N

        print(N)

        # Segna giorno di nascita per le celle appena infettate
        GIORNO_MASK = np.where((VIRUS != 0) & (MASK == 0), i, GIORNO_MASK)
        MASK        = np.where((VIRUS != 0) & (MASK == 0), 1, MASK)

        # Regola 3: calcola quanti giorni è vivo il virus in ogni cella
        giorni_vita = i - GIORNO_MASK

        # Infettivo solo nella finestra (Ve, Ve+Vl]
        VIRUS_MASK = np.where(
            (giorni_vita > Ve) & (giorni_vita <= Ve + Vl),
            1, 0
        )

        # Rimuovi virus solo quando ha superato tutta la sua vita (Ve + Vl)
        VIRUS = np.where(giorni_vita > Ve + Vl, 0, VIRUS)

        # Regola 4: se popolazione = 0 per 3 giorni consecutivi, azzera virus
        POP_MASK = np.where(STORICO[i] == 0, POP_MASK - 1, 3)
        POP_MASK = np.clip(POP_MASK, 0, 3)
        VIRUS    = np.where(POP_MASK == 0, 0, VIRUS)

    return VIRUS