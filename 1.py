from pulp import *

# Define the distance matrix
distances = [
    [0, 51, 44, 64, 19, 42, 94, 57, 76, 23],
    [51, 0, 35, 39, 100, 13, 20, 92, 91, 40],
    [44, 35, 0, 25, 49, 64, 85, 34, 66, 89],
    [64, 39, 25, 0, 92, 10, 60, 80, 44, 23],
    [19, 100, 49, 92, 0, 28, 96, 10, 73, 53],
    [42, 13, 64, 10, 28, 0, 60, 79, 20, 57],
    [94, 20, 85, 60, 96, 60, 0, 82, 16, 26],
    [57, 92, 34, 80, 10, 79, 82, 0, 51, 69],
    [76, 91, 66, 44, 73, 20, 16, 51, 0, 35],
    [23, 40, 89, 23, 53, 57, 26, 69, 35, 0]
]

# Define the number of cities
num_cities = len(distances)

# Create a binary variable indicating whether an edge is selected
edges = [(i, j) for i in range(num_cities) for j in range(num_cities) if i != j]
x = LpVariable.dicts("x", edges, cat="Binary")

# Create the TSP model
tsp_model = LpProblem("TSP", LpMinimize)

# Set the objective function: minimize the total distance
tsp_model += lpSum([distances[i][j] * x[(i, j)] for (i, j) in edges])

# Add the constraints: each city is visited exactly once
for i in range(num_cities):
    tsp_model += lpSum([x[(i, j)] for j in range(num_cities) if i != j]) == 1

# Add the constraints: each city is left exactly once
for j in range(num_cities):
    tsp_model += lpSum([x[(i, j)] for i in range(num_cities) if i != j]) == 1

# Add the subtour elimination constraints
N = num_cities
u = LpVariable.dicts("u", range(num_cities), lowBound=0, upBound=N - 1, cat="Integer")
for (i, j) in edges:
    if i != 0 and j != 0:
        tsp_model += u[i] - u[j] + N * x[(i, j)] <= N - 1

# Solve the TSP problem
tsp_model.solve()

# Extract the solution
optimal_route = [0]
next_city = 0
while True:
    for j in range(num_cities):
        if next_city != j and value(x[(next_city, j)]) == 1:
            optimal_route.append(j)
            next_city = j
            break
    if next_city == 0:
        break



# Print the optimal route and its distance
optimal_distance = value(tsp_model.objective)
print("Optimal Route:", optimal_route)
print("Optimal Distance:", optimal_distance)
