import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint


def get_points_on_circle(n, r):
    points = []

    for _ in range(n):
        phi = np.radians(np.random.randint(0, 360))
        p = np.random.randint(2, r)
        x = p * np.cos(phi)
        y = p * np.sin(phi)
        points.append((x, y))

    return points


def d(x, y):
    return np.round(np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2), 2)


def get_matrix_cost(points):
    n = len(points)
    cij = np.zeros((n, n))

    for i, xi in enumerate(points):
        for j, xj in enumerate(points):
            if i == j:
                cij[i, j] = float('inf')
            else:
                cij[i, j] = d(xi, xj)

    return cij


def EigenVill(tij, ai, d, cij):
    S=0
    get_point = np.zeros((len(tij), len(tij)), 'bool')
    for i in range(len(tij)):
        for j in range(len(tij)):
            if i == j:
                get_point[i, j] = True
    get_point[0, :] = True
    bandwidth = [0]
    bandwidth.extend(ai)

    edges = []
    while not np.all(get_point):
        min_value = float('inf')
        min_ij = None
        for i in range(1, len(tij)):
            row = tij[i]
            for j in range(0, len(row)):
                cell = row[j]
                if cell < min_value and not get_point[i,j]:
                    min_ij = (i,j)
                    min_value = cell
        if min_ij is None:
            break
        i, j = min_ij
        if bandwidth[i] + bandwidth[j] <= d:
            bandwidth[j] += bandwidth[i]
            get_point[i,:] = True
            get_point[j,i] = True
            edges.append((i, j))
            S += cij[i][j]
        else:
            get_point[i,j] = True

    return edges, S, bandwidth


def add_neighbours(i, cij, added, queue):
    for j in range(len(cij)):
        if cij[i][j] != float('inf') and not added[j]:
            queue.append(((i,j), cij[i][j] ))

def Prim(cij):
    S = 0

    edges = []
    added = np.zeros(len(cij), 'bool')
    added[0] = True
    i = 0
    queue = []

    add_neighbours(i, cij, added, queue)

    while not np.all(added):

        min_value = float('inf')
        min_ij = None
        for ij, value in queue:
            if value < min_value:
                min_value = value
                min_ij = ij

        if min_ij is None:
            break

        queue.remove((min_ij, min_value))
        if not added[min_ij[1]]:
            edges.append(min_ij)
            S+= cij[min_ij[0]][min_ij[1]]
            added[min_ij[1]] = True
            add_neighbours(min_ij[1], cij, added, queue)

    return edges, S



def main():
    center = (0, 0)
    n = 10
    d = 7
    r = 20

    indexes = list(range(1, n + 1))
    ai = np.round([3 / 2 * np.abs(np.sin(i)) for i in indexes],1)

    points = get_points_on_circle(n, r)

    all_points = [center]
    all_points.extend(points)

    all_points = np.round(all_points, 2)

    cij = np.round(get_matrix_cost(all_points), 2)
    b = cij[:,0]

    tij = np.round(cij - np.vstack(b), 2)
    tij[1:,0] = 0
    tij[0,1:] = 0

    edges, S1, bandwidth = EigenVill(tij, ai, d, cij)
    edges1, S2 = Prim(cij)

    with open("res_lab3.txt", "w+") as file:
        file.write("ai\t" + str(ai))
        file.write("\n")
        file.write("all_points\t" + str(all_points))
        file.write("\n")

        file.write("bandwidth\t" + str(bandwidth))
        file.write("\n")

        file.write("cij\t" + str(cij))
        file.write("\n")
        file.write("tij\t" + str(tij))
        file.write("\n")

        file.write("EigenVill")
        file.write("\n")
        file.write("S1\t" + str(S1))
        file.write("\n")
        file.write("edges\t" + str(edges))
        file.write("\n")


        file.write("Prim")
        file.write("\n")
        file.write("S2\t" + str(S2))
        file.write("\n")

        file.write("edges\t" + str((edges1)))
        file.write("\n")


    circle_x = np.linspace(-r, r, 100)
    circle_y = np.sqrt(r * r - circle_x ** 2)

    plt.plot(circle_x, circle_y, linewidth=0.9, color="red")
    plt.plot(circle_x, -circle_y, linewidth=0.9, color="red")

    ps = np.array(points).T
    pointsX, pointsY = ps[0], ps[1]
    plt.plot(pointsX, pointsY, 'o', color="gray")

    plt.plot(0, 0, 'o', color="blue")

    

    for edge_index in edges:
        i, j = edge_index
        x1, y1 = all_points[i]
        x2, y2 = all_points[j]
        plt.arrow(x1, y1, (x2-x1)*0.96, (y2-y1)*0.96, width=0.2, color="red")
        plt.text(x1, y1-1.5, str(i) + "-" + str((x1, y1)), fontsize=6)
        plt.text(x2, y2 - 1.5, str(j) + "-" + str((x2, y2)), fontsize=6)

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("EigenVill.jpg")
    plt.show()

    plt.plot(circle_x, circle_y, linewidth=0.9, color="red")
    plt.plot(circle_x, -circle_y, linewidth=0.9, color="red")

    ps = np.array(points).T
    pointsX, pointsY = ps[0], ps[1]
    plt.plot(pointsX, pointsY, 'o', color="gray")
    plt.plot(0, 0, 'o', color="blue")

    for edge_index in edges1:
        i, j = edge_index
        x1, y1 = all_points[i]
        x2, y2 = all_points[j]
        plt.arrow(x1, y1, (x2-x1)*0.96, (y2-y1)*0.96, width=0.2, color="red")
        plt.text(x1, y1 - 1.5, str(i) + "-"+ str((x1, y1)), fontsize=6)
        plt.text(x2, y2 - 1.5, str(j) + "-"+ str((x2, y2)), fontsize=6)

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.savefig("Prim.jpg")
    plt.show()



if __name__ == "__main__":
    main()
