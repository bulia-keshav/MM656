# Python implementation of Vogel's Approximation Method for transportation problem

def vogel_approximation_method(costs, supply, demand):
    """
    Solve transportation problem using Vogel's Approximation Method
    
    Args:
        costs: List of lists containing transportation costs
        supply: List of supply values
        demand: List of demand values
        
    Returns:
        Total minimum transportation cost
    """
    import copy
    INF = float('inf')
    
    # Create deep copies to avoid modifying original data
    costs_copy = copy.deepcopy(costs)
    supply_copy = copy.deepcopy(supply)
    demand_copy = copy.deepcopy(demand)
    
    n = len(costs_copy)  # Number of sources
    m = len(costs_copy[0])  # Number of destinations
    total_cost = 0
    allocation = [[0 for _ in range(m)] for _ in range(n)]
    
    # Calculate row and column penalties
    def calculate_penalties():
        row_penalties = []
        col_penalties = []
        
        # Row penalties
        for i in range(n):
            if supply_copy[i] == 0:
                row_penalties.append(-1)
                continue
                
            valid_costs = [costs_copy[i][j] for j in range(m) if costs_copy[i][j] < INF]
            if len(valid_costs) <= 1:
                row_penalties.append(-1)
            else:
                valid_costs.sort()
                row_penalties.append(valid_costs[1] - valid_costs[0])
        
        # Column penalties
        for j in range(m):
            if demand_copy[j] == 0:
                col_penalties.append(-1)
                continue
                
            valid_costs = [costs_copy[i][j] for i in range(n) if costs_copy[i][j] < INF]
            if len(valid_costs) <= 1:
                col_penalties.append(-1)
            else:
                valid_costs.sort()
                col_penalties.append(valid_costs[1] - valid_costs[0])
        
        return row_penalties, col_penalties
    
    # Find cell with minimum cost in given row or column
    def find_min_cost_cell(index, is_row):
        min_cost = INF
        min_index = -1
        
        if is_row:
            for j in range(m):
                if costs_copy[index][j] < min_cost and demand_copy[j] > 0:
                    min_cost = costs_copy[index][j]
                    min_index = j
            return index, min_index, min_cost
        else:
            for i in range(n):
                if costs_copy[i][index] < min_cost and supply_copy[i] > 0:
                    min_cost = costs_copy[i][index]
                    min_index = i
            return min_index, index, min_cost
    
    # Main algorithm loop
    while sum(supply_copy) > 0 and sum(demand_copy) > 0:
        row_penalties, col_penalties = calculate_penalties()
        
        # Find maximum penalty
        max_row_penalty = max(row_penalties) if row_penalties else -1
        max_col_penalty = max(col_penalties) if col_penalties else -1
        
        if max_row_penalty >= max_col_penalty and max_row_penalty != -1:
            # Process row with maximum penalty
            row_index = row_penalties.index(max_row_penalty)
            i, j, cost = find_min_cost_cell(row_index, True)
        elif max_col_penalty != -1:
            # Process column with maximum penalty
            col_index = col_penalties.index(max_col_penalty)
            i, j, cost = find_min_cost_cell(col_index, False)
        else:
            # No valid penalties found
            break
        
        # Allocate maximum possible units
        allocation_amount = min(supply_copy[i], demand_copy[j])
        allocation[i][j] = allocation_amount
        total_cost += allocation_amount * cost
        
        # Update supply and demand
        supply_copy[i] -= allocation_amount
        demand_copy[j] -= allocation_amount
        
        # Mark cell as unavailable if either supply or demand is exhausted
        if supply_copy[i] == 0:
            for j in range(m):
                costs_copy[i][j] = INF
                
        if demand_copy[j] == 0:
            for i in range(n):
                costs_copy[i][j] = INF
    
    return total_cost, allocation

# Example usage for GlobalFreight
costs_global = [
    [80, 150, 95, 115],
    [120, 90, 80, 125],
    [100, 70, 130, 105]
]

supply = [1500, 1750, 2750]
demand = [1000, 1350, 2000, 1650]

total_cost, allocation = vogel_approximation_method(costs_global, supply, demand)
print(f"The minimum transportation cost for GlobalFreight is ₹{total_cost}")

# For TransLogic (with redistributed demand)
costs_translogic = [
    [90, 140, 95],
    [110, 90, 85],
    [100, 80, 115]
]

supply_trans = [1500, 1750, 2750]
demand_trans = [1550, 1900, 2550]  # Redistributed demand including P4

total_cost_trans, allocation_trans = vogel_approximation_method(costs_translogic, supply_trans, demand_trans)
print(f"The minimum transportation cost for TransLogic is ₹{total_cost_trans}")