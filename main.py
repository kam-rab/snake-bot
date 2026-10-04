import time
from pynput.keyboard import Controller
from time import perf_counter
from PIL import Image
import numpy as np
import mss
from pathlib import Path


keyboard1 = Controller()
sct = mss.MSS()
monitor = sct.monitors[1]

start = float(0)
t = float(0)
ASSETS = Path(__file__).resolve().parent / "assets"
board_coords = []
snakeLength = 4
nums = []
for i in range(0, 10):
    nums.append(np.array(Image.open(ASSETS / "digits" / f"{i}.png")))
snake_loc = [(16, 8), (15, 8), (14, 8), (13, 8), (12, 8)]
moves = [(16, 9), (17, 9), (17, 10)]
tileTime = 0.13499991665  # 0.13   0.1349950   0.1350117   0.1350052, 10336, 11288
apple = (16, 8)
prev_apple = (16, 8)
run_astar = False
ham_path = [(1, 14), (1, 13), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2),
            (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12),
            (2, 13), (2, 14), (3, 14), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (3, 6), (3, 5),
            (3, 4), (3, 3), (3, 2), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
            (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (5, 14), (5, 13), (5, 12), (5, 11), (5, 10), (5, 9), (5, 8),
            (5, 7), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
            (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (7, 14), (7, 13), (7, 12), (7, 11),
            (7, 10), (7, 9), (7, 8), (7, 7), (7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1), (8, 1), (8, 2), (8, 3),
            (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (9, 14),
            (9, 13), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1),
            (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11),
            (10, 12), (10, 13), (10, 14), (11, 14), (11, 13), (11, 12), (11, 11), (11, 10), (11, 9), (11, 8), (11, 7),
            (11, 6), (11, 5), (11, 4), (11, 3), (11, 2), (11, 1), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6),
            (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14), (13, 14), (13, 13), (13, 12),
            (13, 11), (13, 10), (13, 9), (13, 8), (13, 7), (13, 6), (13, 5), (13, 4), (13, 3), (13, 2), (13, 1),
            (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11),
            (14, 12), (14, 13), (14, 14), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (15, 9), (15, 8), (15, 7),
            (15, 6), (15, 5), (15, 4), (15, 3), (15, 2), (15, 1), (16, 1), (17, 1), (17, 2), (16, 2), (16, 3), (17, 3),
            (17, 4), (16, 4), (16, 5), (17, 5), (17, 6), (16, 6), (16, 7), (17, 7), (17, 8), (16, 8), (16, 9), (17, 9),
            (17, 10), (16, 10), (16, 11), (17, 11), (17, 12), (16, 12), (16, 13), (17, 13), (17, 14), (16, 14),
            (16, 15), (15, 15), (14, 15), (13, 15), (12, 15), (11, 15), (10, 15), (9, 15), (8, 15), (7, 15), (6, 15),
            (5, 15), (4, 15), (3, 15), (2, 15), (1, 15), (1, 14), (1, 13), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8),
            (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
            (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (3, 14), (3, 13), (3, 12), (3, 11),
            (3, 10), (3, 9), (3, 8), (3, 7), (3, 6), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (4, 1), (4, 2), (4, 3),
            (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (5, 14),
            (5, 13), (5, 12), (5, 11), (5, 10), (5, 9), (5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1),
            (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13),
            (6, 14), (7, 14), (7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8), (7, 7), (7, 6), (7, 5), (7, 4),
            (7, 3), (7, 2), (7, 1), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
            (8, 11), (8, 12), (8, 13), (8, 14), (9, 14), (9, 13), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7),
            (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6),
            (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (11, 14), (11, 13), (11, 12),
            (11, 11), (11, 10), (11, 9), (11, 8), (11, 7), (11, 6), (11, 5), (11, 4), (11, 3), (11, 2), (11, 1),
            (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11),
            (12, 12), (12, 13), (12, 14), (13, 14), (13, 13), (13, 12), (13, 11), (13, 10), (13, 9), (13, 8), (13, 7),
            (13, 6), (13, 5), (13, 4), (13, 3), (13, 2), (13, 1), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6),
            (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (15, 14), (15, 13), (15, 12),
            (15, 11), (15, 10), (15, 9), (15, 8), (15, 7), (15, 6), (15, 5), (15, 4), (15, 3), (15, 2), (15, 1),
            (16, 1), (17, 1), (17, 2), (16, 2), (16, 3), (17, 3), (17, 4), (16, 4), (16, 5), (17, 5), (17, 6), (16, 6),
            (16, 7), (17, 7), (17, 8), (16, 8), (16, 9), (17, 9), (17, 10), (16, 10), (16, 11), (17, 11), (17, 12),
            (16, 12), (16, 13), (17, 13), (17, 14), (17, 15), (16, 15), (15, 15), (14, 15), (13, 15), (12, 15),
            (11, 15), (10, 15), (9, 15), (8, 15), (7, 15), (6, 15), (5, 15), (4, 15), (3, 15), (2, 15), (1, 15),
            (1, 14), (1, 13), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2),
            (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12),
            (2, 13), (2, 14), (3, 14), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (3, 6), (3, 5),
            (3, 4), (3, 3), (3, 2), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
            (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (5, 14), (5, 13), (5, 12), (5, 11), (5, 10), (5, 9), (5, 8),
            (5, 7), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
            (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (7, 14), (7, 13), (7, 12), (7, 11),
            (7, 10), (7, 9), (7, 8), (7, 7), (7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1), (8, 1), (8, 2), (8, 3),
            (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (9, 14),
            (9, 13), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1),
            (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11),
            (10, 12), (10, 13), (10, 14), (11, 14), (11, 13), (11, 12), (11, 11), (11, 10), (11, 9), (11, 8), (11, 7),
            (11, 6), (11, 5), (11, 4), (11, 3), (11, 2), (11, 1), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6),
            (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14), (13, 14), (13, 13), (13, 12),
            (13, 11), (13, 10), (13, 9), (13, 8), (13, 7), (13, 6), (13, 5), (13, 4), (13, 3), (13, 2), (13, 1),
            (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11),
            (14, 12), (14, 13), (14, 14), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (15, 9), (15, 8), (15, 7),
            (15, 6), (15, 5), (15, 4), (15, 3), (15, 2), (15, 1), (16, 1), (17, 1), (17, 2), (16, 2), (16, 3), (17, 3),
            (17, 4), (16, 4), (16, 5), (17, 5), (17, 6), (16, 6), (16, 7), (17, 7), (17, 8), (16, 8), (16, 9), (17, 9),
            (17, 10), (16, 10), (16, 11), (17, 11), (17, 12), (16, 12), (16, 13), (17, 13), (17, 14), (16, 14),
            (16, 15), (15, 15), (14, 15), (13, 15), (12, 15), (11, 15), (10, 15), (9, 15), (8, 15), (7, 15), (6, 15),
            (5, 15), (4, 15), (3, 15), (2, 15), (1, 15)]


def find_board():
    while True:
        time.sleep(0.2)
        ss = np.array(sct.grab(monitor))
        ss = ss[:, :, :3][:, :, ::-1]  #BGRA -> RGB
        scale = ss.shape[1] / monitor["width"]

        r, g, b = (ss[..., i].astype(int) for i in range(3))
        mask = (g > r+15) & (g > b+40) & (g>150)  #filter for green-dominant pixels

        def find_board_by_dim(ss, mask, dim):
            vals, avg_green = np.unique(mask, return_counts=True)
            if True not in vals:
                return False
            avg_green = avg_green[np.where(vals)[0][0]] / ss.shape[dim]
            
            streak, start = 0, 0
            longest_streak, longest_start = 0, 0
            for i in range(mask.shape[dim] + 1):
                if i == mask.shape[dim]:
                    vals = []
                elif dim==0:
                    vals, num_greens = np.unique(mask[i], return_counts=True)
                else:
                    vals, num_greens = np.unique(mask[:, i], return_counts=True)
                if True in vals and num_greens[np.where(vals)[0][0]] > avg_green:
                    if streak == 0:
                        start = i
                    streak += 1
                else:
                    if streak > 0:
                        if streak > longest_streak:
                            longest_streak = streak
                            longest_start = start
                        streak = 0

            return longest_start, longest_streak

        h_dims, w_dims = (find_board_by_dim(ss, mask, i) for i in (0, 1))
        if not h_dims or not w_dims:
            continue

        ratio = w_dims[1] / h_dims[1] # confirm board ratio
        if abs(ratio - 17/15) > 0.03:
            continue

        tile_width = w_dims[1] / 17
        board_coords_temp = (w_dims[0], h_dims[0], w_dims[0] + w_dims[1], h_dims[0] + h_dims[1])

        def find_pix(w, h):
            return ss[board_coords_temp[1] + int((h-0.5)*tile_width)][board_coords_temp[0] + int((w-0.5)*tile_width)].astype(int)
        
        snake_r, snake_g, snake_b = find_pix(3, 8)
        if (snake_b < snake_r+40) or (snake_b < snake_g):
            continue
        snake_r, snake_g, snake_b = find_pix(4, 8)
        if (snake_b < snake_r+40) or (snake_b < snake_g):
            continue
        apple_r, apple_g, apple_b = find_pix(13, 8)
        if (apple_r < apple_g + 50) or (apple_r < apple_b):
            continue
        empty_r, empty_g, empty_b = find_pix(1, 1)
        if (empty_g < empty_r+15) or (empty_g < empty_b+40) or (empty_g<150):
            continue
        empty_r, empty_g, empty_b = find_pix(17, 15)
        if (empty_g < empty_r+15) or (empty_g < empty_b+40) or (empty_g<150):
            continue

        return tuple(np.array(board_coords_temp) / scale)



def press_key(key, tiles):
    global t
    t += (tiles * tileTime)  # 0.12958538
    if tiles > 2:
        time.sleep(0.75 * (t + start - perf_counter()))
    while time.perf_counter() < t + start:
        pass
    else:
        keyboard1.press(key)
        keyboard1.release(key)


def update_snake_vars(new, apple):
    global snake_loc, moves
    moves = moves[1:len(moves)]
    snake_loc.insert(0, new)
    if not apple:
        snake_loc = snake_loc[0:len(snake_loc) - 1]


def find_key(cord):
    direction = [0, 0]
    s = cord[0] - snake_loc[0][0]
    if s != 0:
        direction = [s, 0]
    else:
        direction = [0, (cord[1] - snake_loc[0][1])]
    for i in range(0, 2):
        if snake_loc[1][i] != (snake_loc[0][i] - direction[i]):
            if direction == [1, 0]:
                return "d"
            elif direction == [-1, 0]:
                return "a"
            elif direction == [0, 1]:
                return "s"
            elif direction == [0, -1]:
                return "w"
    return False


def update_path():
    global apple, snakeLength, run_astar, moves, prev_apple
    if run_astar == 2:
        print(2)
        maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        ind = ham_path.index(apple)
        for i in range(0, len(snake_loc)):
            h = ham_path[(ind + 1 + i) % len(ham_path)]
            maze[h[1] - 1][h[0] - 1] = 1
            if not abs(snake_loc[0][0] - snake_loc[i][0]) + abs(snake_loc[0][1] - snake_loc[i][1]) > len(
                    snake_loc) + 2 - i:
                maze[snake_loc[i][1] - 1][snake_loc[i][0] - 1] = 1
        a = astar(maze, (moves[0][0] - 1, moves[0][1] - 1), (apple[0] - 1, apple[1] - 1))
        if a:
            run = True
            for j in range(0, len(a)):
                a[j] = (a[j][0] + 1, a[j][1] + 1)
            astar1 = a
            astar1.extend(snake_loc)
            astar1 = astar1[0:len(snake_loc)]
            if prev_apple in astar1:
                astar1 = astar1[astar1.index(prev_apple):len(astar1)]
                le = len(astar1)
                ham1 = ham_path[ind:] + ham_path[:ind]
                for m in range(0, le):
                    if le + 1 - m >= ham1.index(astar1[m]):
                        run = False
                        break
            if run:
                moves = a
                run_astar = False
    elif run_astar == 1:
        print(1)
        prev_apple = apple
        header = 2.58*(board_coords[2] - board_coords[0]) / 17
        ss = sct.grab({'left': board_coords[0], 'top': (board_coords[1] - header), 'width': board_coords[2] - board_coords[0], 'height': board_coords[3] - board_coords[1] + header})
        im = np.array(Image.frombytes('RGB', ss.size, ss.bgra, "raw", "BGRX").resize((1088, 1124)))
        print(f"{int(time.perf_counter())}: {apple}. {snake_loc}. {moves[1:20]}")
        apple, snakeLength = apple_length(im)
        if apple:
            run_astar = 2
    elif snake_loc[0] == apple:
        print(0)
        ind = ham_path.index(apple)
        moves = ham_path[(ind + 1):(ind + 260)]
        moves.extend(ham_path[0:ind])
        run_astar = 1


def app1(a, b):
    return a == b


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
            # DELETE FOR MORE SQUIGGLY SNAKE
            elif item.f == current_node.f and item.h < current_node.h:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        if in_list(current_node, closed_list):
            continue
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path
        if len(closed_list) > 17 * 15:
            return False

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[1] > (len(maze) - 1) or node_position[1] < 0 or node_position[0] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[0] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[1]][node_position[0]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if in_list(child, closed_list):
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1

            # SWITCH THESE FOR MORE SQUIGGLY SNAKE (uncomment first line + comment out second line)
            # child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.h = (abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1]))

            child.f = child.g + child.h

            # Child is already in the open list
            if any(child == open_node and child.g >= open_node.g for open_node in open_list):
                continue

            # Add the child to the open list
            open_list.append(child)


def in_list(x, y):
    for i in y:
        if x == i:
            return True
    return False


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def apple_length(arr):
    return [find_apple(0, 165, arr), (snake_length(50, 0, arr) + 4)]


def find_apple(x0, y0, im):
    for q in range(y0 + 32, y0 + 929, 64):
        for p in range(x0 + 32, x0 + 1057, 64):
            if im[q][p][0] > 200 > im[q][p][2]:
                ap1 = (int((((p - x0) - 32) / 64) + 1), int((((q - y0) - 32) / 64) + 1))
                if ap1 == apple:
                    return False
                else:
                    return ap1
    return False


def snake_length(x0, y0, arr):
    num = 0
    read = [0, x0]
    for i in range(1, 4):
        g = make_guesses(i)
        read = read_num(read[1], y0, arr, g)
        if not read:
            break
        num = 10 * num + read[0]
    return num


def make_guesses(a):
    snakeLength1 = snakeLength - 4
    if (snakeLength1 + 3) / (10 ** (a - 1)) >= 1:
        ret = []
        for i in [0, 3, 2, 1]:
            if (snakeLength1 + i) / (10 ** (a - 1)) >= 1:
                app = int(((snakeLength1 + i) % (10 ** a)) / (10 ** (a - 1)))
                if app not in ret:
                    ret.append(app)
        return ret
    else:
        return []


def read_num(x0, lower_bound, arr, guess):
    x1 = x0
    x2 = 0
    letter = True
    found_letter = False
    upper_bound = lower_bound + 164
    while x1 - x0 < 30 or letter:
        letter = False
        for i in range(lower_bound, upper_bound):
            if arr[i][x1][2] == 227:
                letter = True
                if not found_letter:
                    x2 = x1
                    found_letter = True
                lower_bound = max(i - 35, 0)
                upper_bound = min(i + 35, 164)
                break
        x1 += 1
    if not found_letter:
        return False
    else:
        possible = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for g in guess:
            possible.remove(g)
            possible.insert(0, g)
        for possibles in possible:
            for offset in [0, 1, -1, -2, 2, 3, -3]:
                if match_column(arr[:, x2 + 3 + offset][1:165], nums[possibles][:, 3][1:165]):
                    ret = True
                    for column in range(x2 + 6, x1 - 3, 3):
                        if not match_column(arr[:, offset + column][8:92], nums[possibles][:, column - x2][8:92]):
                            ret = False
                            break
                    if ret:
                        return possibles, x1 - 1


def match_column(c1, c2):
    for i in range(0, len(c1)):
        if c1[i][2] == 227:
            pix = False
            for j in [0, 1, -1, 2, -2]:
                if c2[i + j][2] > 215:
                    pix = True
                    i += (2 + j)
                    break
            if not pix:
                return False
    for k in range(0, len(c2)):
        if c2[k][2] == 227:
            pix = False
            for l in [0, 1, -1, 2, -2]:
                if c1[k + l][2] == 227:
                    pix = True
                    k += (2 + l)
                    break
            if not pix:
                return False
    return True


def everything():
    global start, board_coords
    board_coords = find_board()
    time.sleep(1)
    start = perf_counter()
    press_key("d", 2)
    press_key("s", (1.5649948 / tileTime))  # used to be 1.68461/tileTime   1.5649948
    snake()


def snake():
    global t
    while True:
        update_path()
        key = find_key(moves[0])
        if t + start - time.perf_counter() >= 0.05:
            time.sleep(t + start - time.perf_counter())
        while time.perf_counter() < (t + start):
            pass
        if key:
            keyboard1.press(key)
            keyboard1.release(key)
        t += tileTime
        update_snake_vars(moves[0], app1(moves[0], apple))


if __name__ == "__main__":
    everything()
