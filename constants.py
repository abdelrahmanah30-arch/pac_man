from typing import Tuple
 
# Pixel size of a single maze cell, used by every sprite/rendering
# calculation (player, ghosts, renderer).
CELL_SIZE = 45
 
# A maze cell coordinate, expressed as (row, col).
Position = Tuple[int, int]