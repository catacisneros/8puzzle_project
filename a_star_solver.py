import heapq

goal_state = [1,2,3,4,5,6,7,8,0]  # 0 = blank

def manhattan(puzzle):
    dist = 0
    for i, val in enumerate(puzzle):
        if val == 0: continue
        target = goal_state.index(val)
        dist += abs(i // 3 - target // 3) + abs(i % 3 - target % 3)
    return dist

def get_neighbors(state):
    moves = []
    zero = state.index(0)
    row, col = zero // 3, zero % 3
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    for dr, dc in directions:
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_zero = new_r * 3 + new_c
            new_state = state[:]
            new_state[zero], new_state[new_zero] = new_state[new_zero], new_state[zero]
            moves.append(new_state)
    return moves

def solve_puzzle(start):
    heap = [(manhattan(start), 0, start, [])]
    visited = set()

    while heap:
        f, g, current, path = heapq.heappop(heap)
        if current == goal_state:
            return path + [current]
        visited.add(tuple(current))
        for neighbor in get_neighbors(current):
            if tuple(neighbor) not in visited:
                heapq.heappush(heap, (g + 1 + manhattan(neighbor), g + 1, neighbor, path + [current]))
    return []
