# %%
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
# %%
np.random.seed(1)
np.mean(np.random.exponential(10,1_000))
# %%
plt.plot(np.cumsum(np.random.exponential(10,1_000)))
plt.grid()
plt.show()
# %%
A1 = 4
A2 = 1
p1 = 0.2
lamda = 2
mu1 = 1
mu2 = 0.5
# %%
np.random.seed(2)

quiet = True

TMAX = 2_000
BIGNUM = 30
T = 0
N = 0

ESTOT = 0

TESPERAC1 = np.zeros(BIGNUM)
TESPERAC2 = np.zeros(BIGNUM)

TESPERAA1 = np.zeros(A1)
TESPERAA2 = np.zeros(A2)

NC1 = np.zeros(BIGNUM, dtype=int)
NC2 = np.zeros(BIGNUM, dtype=int)

NA1 = np.zeros(A1, dtype=int)
NA2 = np.zeros(A2, dtype=int)

TPEC1 = np.random.exponential(1/lamda)

TPEA1 = np.ones(A1) * np.inf
TPEA2 = np.ones(A2) * np.inf

if not quiet:

    print(f"T: {T}")
    print(f"N: {N}")
    print(f"ESTOT: {ESTOT}")
    print()
    print(f"TPEC1: {TPEC1}")
    print(f"TPEA1: {TPEA1}")
    print(f"TPEA2: {TPEA2}")
    print()
    print(f"NC1: {NC1}")
    print(f"NC2: {NC2}")
    print(f"NA1: {NA1}")
    print(f"NA2: {NA2}")
    print()
    print(f"TESPERAC1: {TESPERAC1}")
    print(f"TESPERAC2: {TESPERAC2}")
    print(f"TESPERAA1: {TESPERAA1}")
    print(f"TESPERAA2: {TESPERAA2}")

while True:

    if not quiet:
        
        sleep(0.1)

    min_times = [TPEC1, np.min(TPEA1), np.min(TPEA2)]
    var_indice = np.argmin(min_times)

    TAVANCE = min_times[var_indice]

    T += TAVANCE

    if T > TMAX:

        break

    TPEC1 -= TAVANCE
    TPEA1 -= TAVANCE
    TPEA2 -= TAVANCE

    TESPERAC1 += TAVANCE * NC1
    TESPERAC2 += TAVANCE * NC2
    TESPERAA1 += TAVANCE * NA1
    TESPERAA2 += TAVANCE * NA2

    if var_indice == 0:

        if np.sum(NA1) < A1:

            posA1 = np.argmin(NA1)
            NA1[posA1] = 1
            TPEA1[posA1] = np.random.exponential(1/mu1)

        else:
            if np.min(NC1) == 1:
                print("ALERTA! BIGNUM MUY PEQUEÑO!")
            posC1 = np.argmin(NC1)
            NC1[posC1] = 1

        TPEC1 = np.random.exponential(1/lamda)

    elif var_indice == 1:

        posA1 = np.argmin(TPEA1)

        moneda = np.random.rand()

        res_moneda = moneda > p1

        if not quiet:

            print("+"*70)
            print(f"MONEDA: {moneda}")
            print("+"*70)
        
        if res_moneda:

            N += 1
            ESTOT += TESPERAA1[posA1]

        else:
            # Pasa a A2
            if np.sum(NA2) < A2:

                posA2 = np.argmin(NA2)

                NA2[posA2] = 1
                TPEA2[posA2] = np.random.exponential(1/mu2)
                TESPERAA2[posA2] = TESPERAA1[posA1]

            else:
                if np.min(NC2) == 1:
                    print("ALERTA! BIGNUM MUY PEQUEÑO!")
                posC2 = np.argmin(NC2)
                NC2[posC2] = 1
                TESPERAC2[posC2] = TESPERAA1[posA1]

        if any(NC1):
            
            TESPERAA1[posA1] = TESPERAC1[0]
            TPEA1[posA1] = np.random.exponential(1/mu1)
            
            NC1[:-1] = NC1[1:]
            NC1[-1] = 0

            TESPERAC1[:-1] = TESPERAC1[1:]
            TESPERAC1[-1] = 0

        else:

            TESPERAA1[posA1] = 0
            TPEA1[posA1] = np.inf
            NA1[posA1] = 0

    else:

        posA2 = np.argmin(TPEA2)
        N += 1
        ESTOT += TESPERAA1[posA2]

        if any(NC2):

            TESPERAA2[posA2] = TESPERAC2[0]
            TPEA2[posA2] = np.random.exponential(1/mu2)
            
            NC2[:-1] = NC2[1:]
            NC2[-1] = 0

            TESPERAC2[:-1] = TESPERAC2[1:]
            TESPERAC2[-1] = 0

        else:

            TESPERAA2[posA2] = 0
            TPEA2[posA2] = np.inf
            NA2[posA2] = 0            
    
    if not quiet:

        print("-"*72)
        print(f"T: {T}")
        print(f"N: {N}")
        print(f"ESTOT: {ESTOT}")
        print()
        print(f"TPEC1: {TPEC1}")
        print(f"TPEA1: {TPEA1}")
        print(f"TPEA2: {TPEA2}")
        print()
        print(f"NC1: {NC1}")
        print(f"NC2: {NC2}")
        print(f"NA1: {NA1}")
        print(f"NA2: {NA2}")
        print()
        print(f"TESPERAC1: {TESPERAC1}")
        print(f"TESPERAC2: {TESPERAC2}")
        print(f"TESPERAA1: {TESPERAA1}")
        print(f"TESPERAA2: {TESPERAA2}")
    
# %%
print(f"N: {N}")
print(f"W = ESTOT / N: {ESTOT / N}")
print(f"N / T: {N / T}")
print(f"L = l_e * W: {lamda * ESTOT / N}")
# %%
