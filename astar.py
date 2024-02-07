import heapq  
import sys


"""
Function to read inputs from file.
Returns tuples containing capacities and target volume.

"""
def read_input_file(file_path):
    with open(file_path) as file:
        jug_capacities = tuple(map(int, file.readline().strip().split(',')))
        target_volume = int(file.readline().strip())
        
    # Returning capacities(infinite represented by maxsize) and target volume 
    return (sys.maxsize,) + jug_capacities, target_volume


"""

Function to estimate the cost from current state to goal state.
Utilized by A* algorithm to find priority state to explore next.


"""
def calculate_heuristic(current_state, container_capacities, goal_quantity):
   
    # Return heuristic of 0 if we have reached the goal 
    if goal_quantity == current_state[0]:
        return 0

    # Check if any container combination matches target, return minimal positive heuristic
    for index in range(1, len(container_capacities)):
        if goal_quantity == current_state[0] + current_state[index]:
            return 1 / goal_quantity
    
    
    distance_from_goal_actual = goal_quantity - current_state[0]
    distance_from_goal_next_step = distance_from_goal_actual - max(current_state[1:])
    
    # If the goal quantity is greater than the first element in the state tuple 
    #and less than the sum of the first element and the maximum capacity in capacities,
    #calculate the actual and next distances to the target quantity
    
    if current_state[0] < goal_quantity <= current_state[0] + max(container_capacities[1:]):
        distance_from_goal_next_step = abs(goal_quantity - current_state[0] - max(current_state[1:]))
    
    # Evaluate if adding any container's max capacity to the first element achieves the target; 
    # return corresponding heuristic if so
    for capacity in container_capacities:
        if goal_quantity == current_state[0] + max(current_state[1:]) + capacity:
            return (distance_from_goal_actual + distance_from_goal_next_step) / 2 / goal_quantity

    # If the target volume is not achieved in the above conditions, return a heuristic value based on the distance 
    return (distance_from_goal_actual + distance_from_goal_next_step) / goal_quantity

"""
Function to create all possible next states to explore at each step.

Utilized by a_star function. 

Takes current_state and jug_capacities and returns possible states list


"""
def generate_next_states(current_state, jug_capacities):
    
    # Initialize a empty list to hold all possible state tuples
    possible_states = []
    
    # Iterating through each jug to explore possible actions
    for i, water_amount in enumerate(current_state):
       
        # Skip the first jug since it has infinite amount of water and cannot change its volume
        if i == 0:
            continue
            
        # Emptying a jug which creates new state
        new_state_empty = list(current_state)
        new_state_empty[i] = 0
        possible_states.append(tuple(new_state_empty))
        
        # Transferring water from the current jug to other jugs
        for j, other_amount in enumerate(current_state):
            # Skip the jug itself
            if i == j:
                continue
            
            # If current jug is empty, fill the jug up to its capacity
            if water_amount == 0:
                new_state = list(current_state)
                new_state[i] += jug_capacities[i]
                possible_states.append(tuple(new_state))
             
            # Ensuring jug does not overflow and giving jug does not go below 0, transfer water from current jug to other jug
            elif water_amount >= jug_capacities[j] - current_state[j] and jug_capacities[j] - current_state[j] >= 0:
                new_state = list(current_state)
                new_state[i] = water_amount - (jug_capacities[j] - current_state[j])
                new_state[j] += (jug_capacities[j] - current_state[j])
                possible_states.append(tuple(new_state))
                
            # If it does not have enough capacity, add as much as possible to other jug
            elif water_amount < jug_capacities[j] - current_state[j]:
                new_state = list(current_state)
                new_state[i] = 0
                new_state[j] += water_amount
                possible_states.append(tuple(new_state))
                
    return possible_states

"""

A* search to find the minimum steps to reach a target quantity in containers.

It takes the containers' capacities and the desired target quantity as inputs, 
returning the least number of actions needed or -1 if the target cannot be reached.

"""
def a_star(capacities, target_quantity): 
    
    start_state =  (0,) * len(capacities)
    frontier = [(calculate_heuristic(start_state, capacities, target_quantity), 0, start_state)]
    explored = set()
    
    while frontier:
        current_total_cost, cost_so_far, current_state = heapq.heappop(frontier)
        
        if current_state[0] > target_quantity:
            continue
        if str(current_state) in explored:
            continue

        if current_state[0] == target_quantity:
            return cost_so_far
        
        while frontier :
            x, y, z = heapq.heappop(frontier)

        explored.add(str(current_state))
        for next_state in generate_next_states(current_state, capacities):                
            next_cost = cost_so_far + 1 
            total_cost = next_cost + calculate_heuristic(next_state, capacities, target_quantity)
            heapq.heappush(frontier, (total_cost, next_cost, next_state))
        
        if current_state[0] > target_quantity+2*max(capacities[1:]):
            return -1
    return -1


if __name__ == '__main__':
    capacities, target_quantity = read_input_file(r"/path_to_file")
    steps = a_star(capacities, target_quantity)
    print(steps)