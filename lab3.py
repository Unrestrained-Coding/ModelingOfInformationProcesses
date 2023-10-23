import numpy as np
import matplotlib.pyplot as plt


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
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


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


def EigenVill(tij, ai, d):

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
        else:
            get_point[i,j] = True

    return edges

def Prim(cij):

    edges = []
    visited = np.zeros(len(cij), 'bool')
    visited[0] = True
    d = np.array([float('inf')]*len(cij))
    last = np.array([-1]*len(cij))
    queue = [0]

    while len(queue) > 0:
        i = queue.pop(0)

        for j in range(len(cij)):
            if not visited[j]:
                if d[j] == float('inf'):
                    d[j] = cij[i][j]
                else:
                    d[j] += cij[i][j]

        min_value = float('inf')
        min_j = None

        for j in range(len(cij)):
            if d[j] < min_value and not visited[j]:
                min_value = d[j]
                min_j = j

        if min_j is None:
            break

        if last[i] != -1:
            u = last[i]

            if cij[u][min_j] < cij[u][i] + cij[i][min_j]:
                edges.append((u, min_j))
                last[min_j] = u
                queue.append(min_j)
                visited[min_j] = True
            else:
                edges.append((i, min_j))
                last[min_j] = i
                queue.append(min_j)
                visited[min_j] = True

        else:
            edges.append((i, min_j))
            last[min_j] = i
            queue.append(min_j)
            visited[min_j] = True

    return edges



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

    print(ai)
    print(all_points)
    print(cij)
    print(tij)

    edges = EigenVill(tij, ai, d)
    edges1 = Prim(cij)

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
        plt.arrow(x1, y1, x2-x1, y2-y1, width=0.2, color="red")
        plt.text(x1, y1-1.5, i, fontsize=6)
        plt.text(x2, y2 - 1.5, j, fontsize=6)

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
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
        plt.arrow(x1, y1, x2 - x1, y2 - y1, width=0.2, color="red")
        plt.text(x1, y1 - 1.5, i, fontsize=6)
        plt.text(x2, y2 - 1.5, j, fontsize=6)

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.show()



if __name__ == "__main__":
    main()
