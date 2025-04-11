import heapq 
#This module provides an implementation of the heap queue algorithm, also known as the priority queue algorithm

# Node class represents each state in the puzzle
class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # Cost from start node to current node
        self.h = h  # Heuristic cost from current node to goal
        self.f = g + h  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(self.state))

# Function to calculate the Manhattan distance heuristic
def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(1, 9):
        current_index = state.index(i)
        goal_index = goal_state.index(i)
        current_row, current_col = divmod(current_index, 3)
        goal_row, goal_col = divmod(goal_index, 3)
        distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

# Function to get the possible moves from the current state
def get_neighbors(node, goal_state):
    neighbors = []
    state = node.state
    blank_index = state.index(0)
    blank_row, blank_col = divmod(blank_index, 3)

    moves = [
        (blank_row - 1, blank_col, "up"),
        (blank_row + 1, blank_col, "down"),
        (blank_row, blank_col - 1, "left"),
        (blank_row, blank_col + 1, "right")
    ]

    for row, col, move in moves:
        if 0 <= row < 3 and 0 <= col < 3:
            new_index = row * 3 + col
            new_state = state[:]
            new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
            g = node.g + 1
            h = manhattan_distance(new_state, goal_state)
            neighbors.append(Node(new_state, node, g, h))

    return neighbors

# Function to reconstruct the path from the goal node to the start node
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

# A* search algorithm to solve the 8-puzzle problem
def astar(start_state, goal_state):
    start_node = Node(start_state, h=manhattan_distance(start_state, goal_state))
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node)

        if current_node.state == goal_state:
            return reconstruct_path(current_node)

        neighbors = get_neighbors(current_node, goal_state)
        for neighbor in neighbors:
            if neighbor in closed_list:
                continue
            if neighbor not in open_list:
                heapq.heappush(open_list, neighbor)
            else:
                index = open_list.index(neighbor)
                if neighbor.g < open_list[index].g:
                    open_list[index].g = neighbor.g
                    open_list[index].parent = current_node

    return None  # No path found

# Main function to solve the 8-puzzle problem
def main():
    start_state = [1, 2, 3, 4, 0, 5, 6, 7, 8]  # 0 represents the blank tile
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    path = astar(start_state, goal_state)

    if path:
        print("Solution found!")
        for step in path:
            print(step[:3])
            print(step[3:6])
            print(step[6:])
            print()
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()

# Explanation of the Code
# Node Class:

# Represents each state in the puzzle.
# Stores the state, parent node, costs g (cost to reach this node), h (heuristic cost to the goal), and f (total cost g + h).
# Manhattan Distance Function:

# Calculates the Manhattan distance heuristic, which is the sum of the absolute differences of the current position and the goal position for each tile.
# Get Neighbors Function:

# Generates possible moves (up, down, left, right) from the current state.
# Ensures moves are within bounds.
# Creates new states based on the moves and calculates their costs.
# Reconstruct Path Function:

# Traces back from the goal node to the start node to reconstruct the path.
# A Search Algorithm*:

# Uses a priority queue (min-heap) to manage nodes to be explored.
# Pops the node with the lowest f value and explores its neighbors.
# If the goal state is reached, reconstructs and returns the path.
# Main Function:

# Defines the start state and goal state.
# Runs the A* algorithm to find the solution path.
# Prints the solution path if found.
# This implementation of the A* search algorithm effectively solves the 8-puzzle problem by considering both the actual cost and the heuristic estimate to reach the goal state.