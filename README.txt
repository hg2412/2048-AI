Name: Haoxiang Gao
UNI: hg2412
Email: hg2412@columbia.edu

Description of PlayerAI:

The Player AI used iterative depth MiniMax search and α − β pruning to find the best move.

To speed up the computation, I set the maximum depth of search to 8. I also simplified Computer AI's move by assuming all inserted tiles are 2, because 2 or 4 has little effect on evaluation of the grid.

The core part of Player AI is the evaluation function. The utility is the weighted sum of log2(Max Number of tile), number of available cells, monotonicity and smoothness.

log2(Max Number of tile) ensures that the player AI will merge tiles to produce higher maximum number.

Number of available cells also make the PlayerAI tends to merge tiles to save more space.

Monotonicity is calculated by get_monotonicity function, if the tile with max number is at the corner, the function will calculate the maximum of sum of log2 of monotonous tiles along two paths (e.g. if max tile is at (0, 0), the first path is (0, 0) -> ... -> (3, 0) ->(3,1) ->... ->(0, 1), and the second path is(0, 0) -> ... -> (0, 3) ->(1,3) -> ...->（1, 0)).

Smoothness is calculated by get_smootheness function. For each tile, the calculate if it is within 1 manhattan distance away from the tile with similar numbers. If it is near the tile with the same number, the smoothness will increment by log2 of the number. If it is near the tile with the same number +- 1, the smootheness increments by 0.5 * log2 of the number. Smoothness guranttees that the tiles can be moved to merge with other tiles.

The best result of my PlayerAI is maximum number of 2048. Please kindly find the screenshot in the folder.