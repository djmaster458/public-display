import heapq

class Entry:
    """
    Entries into the Priority Queue for A* search:
        fn: Predicted cost calculated by current number of moves (gn) plus predictive function (hn) towards goal (Hamming or Manhattan)
        number_of_moves: Number of moves to reach current state
        current_state: copy of the current board state
        parent_entry: reference to the previous entry for path tracing and loopback checking

        Also define the compare function for min-heap / priority queue 
    """
    def __init__(self, fn, number_of_moves, state, parent):
        self.fn = fn
        self.number_of_moves = number_of_moves
        self.state = state
        self.parent = parent
    

    def __lt__(self, entry2):
        return self.fn < entry2.fn


class PriorityQueue:
    """
    Priority Queue:
        Wraps the heapq algorithm to implement a min heap as a priority queue for the A* algorithm.
        Typical functions of IsEmpty, Push, Peek, and Pop are implemented.
    """
    def __init__(self):
        self.min_heap = []


    def GetCurrentSize(self):
        return len(self.min_heap)


    def IsEmpty(self):
        return False if len(self.min_heap) > 0 else True


    def Push(self, entry):
        heapq.heappush(self.min_heap, entry)


    def Peek(self):
        if self.IsEmpty():
            return None
        return self.min_heap[0]


    def Pop(self):
        if self.IsEmpty():
            return None
        return heapq.heappop(self.min_heap)