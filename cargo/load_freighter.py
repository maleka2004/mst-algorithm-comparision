# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT TASK D.
# The freighter loader.
#
# __author__ = 'Maleka Ramchandani'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from fold.databrick import Databrick

# A memo maps a sub-problem key to a (records, weight) pair: the most
# records achievable for that sub-problem, and the smallest weight that
# achieves it. Keys are (i, c) for the weight-only loader and (i, c, l)
# for the weight-and-volume loader.
Memo = dict[tuple, tuple[int, int]]


def load_freighter(bricks: list[Databrick],
                   weight_capacity: int,
                   volume_capacity: int | None = None
                   ) -> tuple[list[Databrick], int, int, int, Memo]:
    """
    Chooses which databricks to load onto the freighter.

    This function is the entry point the tests and the operation report
    call. It dispatches to one of the two loaders you implement below,
    depending on whether the volume limit is switched on. You should not
    need to change this function.

    @param bricks: The recovered databricks to choose from.
    @param weight_capacity: The freighter's weight limit in kilograms.
    @param volume_capacity: The freighter's volume limit in litres, or
                            None for no volume limit.
    @returns: A tuple of:
              - list[Databrick]: the databricks to load;
              - int: total records freed;
              - int: total weight loaded;
              - int: total volume loaded;
              - Memo: the sub-problem answers computed along the way.
    """
    if volume_capacity is None:
        selected, memo = load_weight_only(bricks, weight_capacity)
    else:
        selected, memo = load_weight_and_volume(
            bricks, weight_capacity, volume_capacity)

    value = sum(b.records for b in selected)
    weight = sum(b.weight for b in selected)
    volume = sum(b.volume for b in selected)
    return selected, value, weight, volume, memo


def load_weight_only(bricks: list[Databrick],
                     weight_capacity: int
                     ) -> tuple[list[Databrick], Memo]:
    """
    The single-limit loader (Task D.1): choose the load that frees the
    most records within the weight limit, breaking ties toward the
    lightest load.

    @param bricks: The databricks to choose from.
    @param weight_capacity: The freighter's weight limit in kilograms.
    @returns: A tuple of:
              - list[Databrick]: the databricks to load;
              - Memo: the sub-problem answers, keyed (i, c).

    HINT: a sub-problem is "the best you can do using the first i bricks
    with c kg of capacity left" --- decide whether brick i is taken.
    """
    memo = {}
    def best(i, c):   #smallest weight achieving most records
        if i == 0:         #base case= no bricks to chose from so nothing to load
            return (0,0)             
        if (i, c) in memo:      #since we already solved the sub problem, reuse the stored answer
            return memo[(i, c)]  
        b = bricks[i - 1] #bricks are numbered from 1
        result = best(i - 1, c) # Option 1: leave brick i behind. Capacity is unchanged
        if b.weight <= c:         # Option 2: take brick i, but only if it fits in the remaining capacity.       
            r, w = best(i - 1, c-b.weight)  #best of the rest, with less capacity
            take = (r + b.records, w + b.weight) # add this brick's records and weight
             # Keep "take" if it frees more records, or the same records with less weight
            if take[0] > result[0] or (take[0] == result[0] and take[1] < result[1]):
                result = take
        memo[(i, c)] = result  # store it so it is never solved twice
        return result

    best(len(bricks), weight_capacity)       # solve the whole problem

    chosen = []
    c = weight_capacity
    for i in range(len(bricks), 0, -1):      # go backwards through the bricks
        if best(i, c) != best(i - 1, c):     # answer changed, so brick i was taken
            chosen.append(bricks[i - 1])
            c -= bricks[i - 1].weight        # it used up some capacity
    return chosen, memo


def load_weight_and_volume(bricks: list[Databrick],
                           weight_capacity: int,
                           volume_capacity: int
                           ) -> tuple[list[Databrick], Memo]:
    """
    The dual-limit loader (Task D.2): choose the load that frees the
    most records within both the weight and volume limits, breaking ties
    toward the lightest load.

    @param bricks: The databricks to choose from.
    @param weight_capacity: The freighter's weight limit in kilograms.
    @param volume_capacity: The freighter's volume limit in litres.
    @returns: A tuple of:
              - list[Databrick]: the databricks to load;
              - Memo: the sub-problem answers, keyed (i, c, l).

    HINT: this is load_weight_only with one extra coordinate to track.
    """
    memo = {} 
 
    def best(i, c, l): 
        # Returns the maximum number of records and the lowest weight needed 
        # using the first i bricks and the remaining capacities. 
 
        # If there are no bricks left, nothing can be added. 
        if i == 0: 
            return (0, 0) 
 
        # If we have already solved this case, use the saved result. 
        if (i, c, l) in memo: 
            return memo[(i, c, l)] 
 
        # Get the current brick we need to decide on. 
        b = bricks[i - 1] 
 
        # Option 1: Do not take this brick. 
        result = best(i - 1, c, l) 
 
        # Option 2: Take the brick if it fits within both capacities. 
        if b.weight <= c and b.volume <= l: 
            r, w = best(i - 1, c - b.weight, l - b.volume) 
            take = (r + b.records, w + b.weight) 
 
            # Choose the option with more records. If they are equal, 
            # choose the one that uses less weight. 
            if take[0] > result[0] or (take[0] == result[0] and take[1] < result[1]): 
                result = take 
 
        # Save the result so we do not have to calculate it again. 
        memo[(i, c, l)] = result 
        return result 
 
    # Find the best solution using all the bricks and full capacities. 
    best(len(bricks), weight_capacity, volume_capacity) 
 
    # Work backwards through the bricks to find which ones were selected. 
    chosen = [] 
    c, l = weight_capacity, volume_capacity 
    for i in range(len(bricks), 0, -1): 
        # If the answer changes when brick i is included, it was selected. 
        if best(i, c, l) != best(i - 1, c, l): 
            chosen.append(bricks[i - 1]) 
            c -= bricks[i - 1].weight 
            l -= bricks[i - 1].volume 
    return chosen, memo
