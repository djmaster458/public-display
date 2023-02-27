from EightPuzzle import EightPuzzle

"""
Note this takes around ITERATIONS number of seconds to complete.
40 was chosen to be a sufficient population of puzzles for statical purposes
"""

ITERATIONS=40

puzzle = EightPuzzle()

man_avg_num_moves = 0
man_avg_queue_size = 0
man_avg_runtime = 0

ham_avg_num_moves = 0
ham_avg_queue_size = 0
ham_avg_runtime = 0

for i in range(ITERATIONS):
    puzzle.GeneratePuzzle(printPuzzle=False)
    man_stats = puzzle.SolvePuzzle(heuristic='Manhattan', showPath=False, printStats=False)
    ham_stats = puzzle.SolvePuzzle(heuristic='Hamming', showPath=False, printStats=False)

    man_avg_num_moves += man_stats['Number of Moves']
    man_avg_queue_size += man_stats['Maximal Queue Size']
    man_avg_runtime += man_stats['Elapsed Time (sec)']

    ham_avg_num_moves += ham_stats['Number of Moves']
    ham_avg_queue_size += ham_stats['Maximal Queue Size']
    ham_avg_runtime += ham_stats['Elapsed Time (sec)']

man_avg_num_moves /= ITERATIONS
man_avg_queue_size /= ITERATIONS
man_avg_runtime /= ITERATIONS

ham_avg_num_moves /= ITERATIONS
ham_avg_queue_size /= ITERATIONS
ham_avg_runtime /= ITERATIONS


print(f'Manhattan Distance Metric on {ITERATIONS} puzzles:')
print(f'Avg. Number of Moves for Shortest Path: {man_avg_num_moves}')
print(f'Avg. Maximal Queue Size: {man_avg_queue_size}')
print(f'Avg. Runtime (sec): {man_avg_runtime}')
print('------------------------')
print(f'Hamming Distance Metric on {ITERATIONS} puzzles:')
print(f'Avg. Number of Moves for Shortest Paths: {ham_avg_num_moves}')
print(f'Avg. Maximal Queue Size: {ham_avg_queue_size}')
print(f'Avg. Runtime (sec): {ham_avg_runtime}')
print('------------------------')
print('Done')
