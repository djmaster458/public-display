import numpy as np
import time
from PriorityQueue import PriorityQueue, Entry

"""Globals"""
n=3
final_state=np.array([1,2,3,4,5,6,7,8,0], dtype=np.uint8).reshape((3,3))

def IsSolvable(array:np.ndarray):
    """
    IsSolvable:
        Checks if a permutation of the 8-puzzle is solvable by checking number of inversions in 1D array.
        Only use upon generation of the puzzle.
        If the number of inversions is an even number, this 8-puzzle permutation is solvable, otherwise not
        (see https://en.wikipedia.org/wiki/15_puzzle#Alternate_proof)
    """

    number_inversions = 0
    empty_slot = 0

    for i in range(len(array)):
        for j in range(i+1, len(array)):
            if array[j] != empty_slot and array[i] != empty_slot and array[i] > array[j]:
                number_inversions +=  1
    
    return (number_inversions % 2 == 0)


def HammingDistance(puzzle_state:np.ndarray):
    """
    HammingDistance:
        Calculates the number of puzzle pieces in incorrect positions based on the current and final states of the puzzle.
        Compares a puzzle state to a final state.
    """
    hamming_distance = 0

    for i in range(n):
        for j in range(n):
            if puzzle_state[i][j] != final_state[i][j]:
                hamming_distance += 1
    return hamming_distance
    

def ManhattanDistance(puzzle_state:np.ndarray):
    """
    ManhattanDistance:
        Calculates sum of how far each puzzle piece is from the final position in terms of diff in vertical and horizontal direction
        Note: If distance == 0, all nodes are in correct spot
        Formula for Manhattan distance: |x2 - x1| + |y2 - y1|
    """

    manhattan_distance = 0
    # Look-Up Table for a tile value to it's final position. (i.e. 0 value should be coordinate 2,2)
    number_map = ((2,2), (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1))

    # For each tile in the current puzzle, find where its values should be in end, and add distance in vertical and horizontal direction
    for i in range(n):
        for j in range(n):
            final_x, final_y = number_map[puzzle_state[i][j]]
            manhattan_distance += abs(i - final_x) + abs(j - final_y)
    
    return manhattan_distance


def MoveIsSafe(empty_tile:tuple, move:tuple):
    """
    Given a puzzle state, location of empty tile and a move
    Determine if the move is legal (ie not off the board)
    Return true if safe, otherwise false
    """

    x = empty_tile[0] + move[0]
    y = empty_tile[1] + move[1]

    if x > 2 or x < 0 or y > 2 or y < 0:
        return False
    return True


def GenerateNextPuzzleEntries(current_entry:Entry, cost_to_state:dict, priority_queue:PriorityQueue, cost_func):
    """
    Given an entry, generate all possible Entries for each state that are
        1. Undiscovered or
        2. Cheaper to reach than an existing path to this state

    Pushes all entries into the priority queue
    """

    # move right, left, down, up
    moves = ((1,0), (-1,0), (0,1), (0,-1))
    empty_tile = FindEmptyTile(current_entry.state)
    old_x, old_y = empty_tile

    for move in moves:
        if MoveIsSafe(empty_tile, move):
            next_state = current_entry.state.copy()
            new_x = empty_tile[0] + move[0]
            new_y = empty_tile[1] + move[1]

            # swap the empty tile with other tile based on move, and add entry to list
            next_state[old_x][old_y], next_state[new_x][new_y] = next_state[new_x][new_y], next_state[old_x][old_y]

            # if the new state is found in the cost to state dict, and the number of moves is greater or equal, skip this state to avoid double checking
            # if the new state is found in the cost to state dict, and the number of moves is less, update the dict and add this state to queue 
            # if this state is not found in the cost to state dict, it is new and needs to be added
            number_of_moves = current_entry.number_of_moves + 1
            next_state_hash = GetPuzzleHash(next_state)

            if next_state_hash in cost_to_state.keys() and number_of_moves >= cost_to_state[next_state_hash]:
                continue
            else:
                cost_to_state[next_state_hash] = number_of_moves


            next_entry = Entry(cost_func(next_state) + number_of_moves, number_of_moves, next_state, current_entry)
            priority_queue.Push(next_entry)


def FindEmptyTile(puzzle_state:np.ndarray):
    """
    Given a puzzle_state, find the empty tile in the ndarray using np.where
    Result is the row and col arrays for each coordinate so using zip to get a tuple
    """

    result = np.where(puzzle_state == 0)
    coordinate_list = list(zip(result[0], result[1]))

    return coordinate_list[0]


def GetPuzzleHash(puzzle_state:np.ndarray):
    """
    Generates a hash id for a given puzzle state. 
    Used for dict when determining cost to a given state
    Equivalent to 1D array as string
    """

    id = ''
    for i in np.nditer(puzzle_state):
        id += str(i)

    return id


def PrintPath(entry:Entry):
    """Given an entry from the Priority Queue, retrace the path to this state. Prints to terminal"""
    if entry == None:
        return

    PrintPath(entry.parent)
    print(entry.state)
    print('|\nv')


class EightPuzzle:
    def __init__(self):
        """Constructs and 8-Puzzle and the Final State"""

        self.priority_queue = PriorityQueue()
        self.original_state = None


    def GeneratePuzzle(self, solvable=True, puzzle=None, printPuzzle=True):
        """
        GeneratePuzzle:
            If solvable is True, a solvable 8-Puzzle is guaranteed to be created
            If solvable is False, it is not guaranteed to be solvable due to odd number of inversions
                (see https://en.wikipedia.org/wiki/15_puzzle#Alternate_proof)

            If puzzle is defined, use the puzzle provided
            Then reshapes the shuffled array into a 3x3 grid
        """

        if puzzle:
            self.original_state = puzzle
            return

        numbers = np.arange(9, dtype=np.uint8)
        np.random.shuffle(numbers)
        
        if(solvable):
            while(not IsSolvable(numbers)):
                np.random.shuffle(numbers)

        self.original_state = numbers.reshape((3,3))

        if printPuzzle:
            print('Generated Puzzle:')
            print(self.original_state)


    def SolvePuzzle(self, heuristic='Manhattan', showPath=True, printStats=True):
        """
        SolvePuzzle_Manhattan:
            Attempt to solve an 8-puzzle using A* with given heuristic
        """

        if heuristic == 'Manhattan':
            cost_func = ManhattanDistance
        elif heuristic == 'Hamming':
            cost_func = HammingDistance
        else:
            print('Heuristic Parameter must be "Hamming" or "Manhattan"')
            return -2

        if printStats:
            print(f'Solving Puzzle using: {heuristic} Distance')

        start_time = time.perf_counter_ns()

        self.priority_queue = PriorityQueue()
        self.cost_to_state = {}
        initial_state = self.original_state.copy()
        
        # First Entry's Fn = Gn + Hn where Gn = 0 and Hn = Manhattan Distance + 0, 0 moves made, and no parent puzzle state
        initial_entry = Entry(cost_func(initial_state), 0, initial_state, None)

        # Push initial puzzle and data into the min heap
        self.priority_queue.Push(initial_entry)

        # Cost to initial state is 0
        self.cost_to_state[GetPuzzleHash(initial_state)] = 0

        max_queue_size = 1

        while not self.priority_queue.IsEmpty():

            cur_size = self.priority_queue.GetCurrentSize()
            if cur_size > max_queue_size:
                max_queue_size = cur_size

            current_entry = self.priority_queue.Pop()

            # Check if final state found, then print out data
            if np.array_equal(current_entry.state, final_state):
                end_time = time.perf_counter_ns()
                elapsed_time = end_time - start_time
                elapsed_time /= 1000000000

                output_dict = {
                    'Number of Moves': current_entry.number_of_moves,
                    'Elapsed Time (sec)': elapsed_time,
                    'Maximal Queue Size': max_queue_size
                }

                if printStats:
                    print('Final State Reached')
                    print(output_dict)

                if showPath:
                    PrintPath(current_entry)
                    print('Done')

                return output_dict

            # Otherwise, generate the next entries to explore in the priority queue
            GenerateNextPuzzleEntries(current_entry, self.cost_to_state, self.priority_queue, cost_func)

        print('Unable to solve eight puzzle, no entries left in priority queue')
        return -1