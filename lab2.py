import numpy as np
import matplotlib.pyplot as plt

def get_points_on_circle(n, r):
    points = []

    for _ in range(n):
        phi = np.radians(np.random.randint(0, 360))
        x = r * np.cos(phi)
        y = r * np.sin(phi)
        points.append((x,y))

    return np.array(points)

def main():
    n = 10
    k = 13
    r = 20
    indexes = list(range(1, n + 1))
    tau = np.array([5 + 4 * np.sin(k * i / 2) for i in indexes])

    points = get_points_on_circle(n, r)
    pointsX = points.T[0]
    pointsY = points.T[1]

    d = np.sum(tau)

    xx = np.sum(tau * pointsX) / d
    xy = np.sum(tau * pointsY) / d

    print(tau)
    print(points)

    print(xx,xy)
    print(np.sqrt(xx*xx + xy*xy))

    circle_x = np.linspace(-r, r, 100)
    circle_y = np.sqrt(r*r - circle_x ** 2)

    plt.plot(circle_x, circle_y, linewidth=0.9, color="red")
    plt.plot(circle_x, -circle_y, linewidth=0.9, color="red")

    plt.plot(pointsX, pointsY, 'o', color="gray")

    plt.plot(xx, xy, 'o', color="blue")
    plt.text(xx, xy+1, "x*")

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    main()