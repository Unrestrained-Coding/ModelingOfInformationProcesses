import random

import numpy as np
import matplotlib.pyplot as plt

def randAtoB(x, a, b):
    return x * (b-a) + a

def main():
    n = 10
    b = 30
    k = 13
    indexes = list(range(1, n + 1))
    bi = [randAtoB(random.random(), 2, 10) for _ in indexes]
    ci = [3 + 2 * np.sin(k * i) for i in indexes]
    valuesB = []

    _sorted_indexes = sorted(indexes, key=lambda x: ci[x - 1])

    # sum(xi)
    S = 0
    #
    B = 0
    B1 = 0
    #
    bcX = []
    bcY = []
    _lambda = None
    _notFind = True
    for index in _sorted_indexes:
        i = index - 1
        bcX.append(ci[i])
        bcY.append(B)
        if _notFind:
            _lambda = ci[i]
            if B + bi[i] <= b:
                B1 += bi[i]
                S += bi[i] * ci[i]
            else:
                B1 += (b - B)
                S += (b - B) * ci[i]
                _notFind = False
        B += bi[i]
        valuesB.append(round(B,2))
        bcX.append(ci[i])
        bcY.append(B)

    print(np.round(bi,2))
    print(np.round(ci,2))
    print(np.round([ci[index - 1] for index in _sorted_indexes],2))
    print(np.round([bi[index - 1] for index in _sorted_indexes],2))
    print(np.round(_lambda,2))
    print(np.round(B1,2))
    print(np.round(S,2))

    noll = [0] * n
    plt.subplots(figsize=(30, 30))

    plt.plot(bcX, bcY)
    plt.axhline(b, linewidth=0.8, color="gray", linestyle="-.")
    plt.axvline(_lambda, linewidth=0.8, color="gray", linestyle="-.")
    plt.plot(_lambda, b, 'o', color="darkgreen")
    plt.plot([ci[index - 1] for index in _sorted_indexes], noll, linewidth=0.8, color="red")
    plt.plot([ci[index - 1] for index in _sorted_indexes], noll, 'o', color="red")

    for i, (x,y) in enumerate(zip(bcX[1::2], bcY[1::2])):
        plt.text(x,y+0.5, str(valuesB[i]), fontsize=6)

    for x in [ci[index - 1] for index in _sorted_indexes]:
        plt.text(x, -1.5, str(round(x, 2)), fontsize=7)

    plt.savefig("lab1.jpg")
    plt.show()


if __name__ == "__main__":
    main()
