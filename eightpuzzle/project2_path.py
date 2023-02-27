from EightPuzzle import EightPuzzle

puzzle = EightPuzzle()

# Generate a random, solvable puzzle. 
# Note: The same puzzle is kept until regeneration (solving again will be on the same seeded puzzle)
puzzle.GeneratePuzzle()
puzzle.SolvePuzzle(heuristic='Manhattan', showPath=True, printStats=True)
print('------------------------')
puzzle.SolvePuzzle(heuristic='Hamming', showPath=True, printStats=True)
print('------------------------')
