import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Тетрис")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(112,163,218), (218,112,163), (163,218,11), (204,0,0), (204,153,255)]


BLOCK_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE
board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


tetrominoes = [
    [(1, 1, 1, 1)],
    [(1, 1), (1, 1)],
    [(0, 1, 0), (1, 1, 1)],
    [(1, 0, 0), (1, 1, 1)],
    [(0, 0, 1), (1, 1, 1)]
]

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     ((self.x + j) * BLOCK_SIZE, (self.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def create_tetromino():
    idx = random.randint(0, len(tetrominoes) - 1)
    return Tetromino(tetrominoes[idx], COLORS[idx])


def valid_space(tetromino, board):
    accepted_positions = [[(j, i) for j in range(BOARD_WIDTH) if board[i][j] == 0] for i in range(BOARD_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]  # Flatten list
    formatted = convert_shape_format(tetromino)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def convert_shape_format(tetromino):
    positions = []
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell == 1:
                positions.append((tetromino.x + j, tetromino.y + i))

    return positions

def rotate_shape(shape):
    rotated_shape = [list(row) for row in zip(*shape[::-1])]
    return rotated_shape

def lock_position(tetromino, board):
    for pos in convert_shape_format(tetromino):
        x, y = pos
        if y > -1:
            board[y][x] = COLORS.index(tetromino.color) + 1

def check_game_over(board):
    for x in range(BOARD_WIDTH):
        if board[0][x] != 0:
            return True
    return False


def clear_rows(board):
    global score
    for i in range(len(board) - 1, -1, -1):
        row = board[i]
        if 0 not in row:
            del board[i]
            board.insert(0, [0 for _ in range(BOARD_WIDTH)])

def draw_window(screen, board):
    screen.fill(BLACK)
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            pygame.draw.rect(screen, WHITE, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
            if board[i][j] != 0:
                pygame.draw.rect(screen, COLORS[board[i][j] - 1],
                                 (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def game_loop():
    clock = pygame.time.Clock()
    running = True
    fall_speed = 0.3
    fall_time = 0
    current_tetromino = create_tetromino()
    next_tetromino = create_tetromino()

    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_tetromino.y += 1
            if not valid_space(current_tetromino, board):
                current_tetromino.y -= 1
                lock_position(current_tetromino, board)
                if check_game_over(board):
                    print("Игра окончена")
                    running = False
                    break
                current_tetromino = next_tetromino
                next_tetromino = create_tetromino()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if not valid_space(current_tetromino, board):
                        current_tetromino.x += 1
                if event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if not valid_space(current_tetromino, board):
                        current_tetromino.x -= 1
                if event.key == pygame.K_DOWN:
                    current_tetromino.y += 1
                    if not valid_space(current_tetromino, board):
                        current_tetromino.y -= 1
                if event.key == pygame.K_UP:
                    original_shape = current_tetromino.shape
                    current_tetromino.shape = rotate_shape(current_tetromino.shape)
                    if not valid_space(current_tetromino, board):

                        current_tetromino.shape = original_shape


        draw_window(screen, board)
        current_tetromino.draw(screen)
        clear_rows(board)
        pygame.display.update()


game_loop()
pygame.quit()
