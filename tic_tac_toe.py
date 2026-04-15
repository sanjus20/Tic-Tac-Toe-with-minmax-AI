import pygame
import math
import sys

# Configuration
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 600
LINE_WIDTH = 8
CELL_SIZE = BOARD_SIZE // 3
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 12
SPACE = 40

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
TEXT_COLOR = (255, 255, 255)

HUMAN = 'X'
AI = 'O'
EMPTY = ' '

nodes_explored = 0


# Game Logic
def create_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]

def is_moves_left(board):
    for row in board:
        if EMPTY in row:
            return True
    return False

def check_winner(board):
    # Rows
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]

    # Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None

def evaluate(board):
    winner = check_winner(board)
    if winner == AI:
        return 10
    elif winner == HUMAN:
        return -10
    return 0

def minimax(board, depth, is_max, alpha, beta):
    global nodes_explored
    nodes_explored += 1

    score = evaluate(board)

    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    value = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = EMPTY
                    best = max(best, value)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        return best
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    value = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = EMPTY
                    best = min(best, value)
                    beta = min(beta, best)
                    if beta <= alpha:
                        return best
        return best

def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)

    global nodes_explored
    nodes_explored = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = EMPTY

                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    return best_move

# Pygame Drawing
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 32)

def draw_lines():
    screen.fill(BG_COLOR)
    # horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (BOARD_SIZE, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * CELL_SIZE), (BOARD_SIZE, 2 * CELL_SIZE), LINE_WIDTH)
    # vertical
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, BOARD_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, BOARD_SIZE), LINE_WIDTH)

def draw_figures(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == HUMAN:
                pygame.draw.line(
                    screen, CROSS_COLOR,
                    (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE),
                    (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE),
                    CROSS_WIDTH
                )
                pygame.draw.line(
                    screen, CROSS_COLOR,
                    (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE),
                    (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE),
                    CROSS_WIDTH
                )
            elif board[row][col] == AI:
                pygame.draw.circle(
                    screen, CIRCLE_COLOR,
                    (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                    CIRCLE_RADIUS, CIRCLE_WIDTH
                )

def draw_status(message):
    pygame.draw.rect(screen, (20, 20, 20), (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE))
    text = font.render(message, True, TEXT_COLOR)
    screen.blit(text, (20, BOARD_SIZE + 20))

def restart_button():
    button_rect = pygame.Rect(380, BOARD_SIZE + 15, 180, 50)
    pygame.draw.rect(screen, (60, 60, 60), button_rect, border_radius=10)
    txt = small_font.render("Restart", True, TEXT_COLOR)
    screen.blit(txt, (430, BOARD_SIZE + 28))
    return button_rect

def mark_square(board, row, col, player):
    board[row][col] = player

def available_square(board, row, col):
    return board[row][col] == EMPTY

# Main Game Loop
board = create_board()
draw_lines()
game_over = False
player_turn = HUMAN
status = "Your Turn (X)"

while True:
    draw_lines()
    draw_figures(board)

    winner = check_winner(board)
    if winner == HUMAN:
        status = "You Win!"
        game_over = True
    elif winner == AI:
        status = "AI Wins!"
        game_over = True
    elif not is_moves_left(board):
        status = "It's a Draw!"
        game_over = True

    draw_status(status)
    btn = restart_button()
    pygame.display.update()

    if not game_over and player_turn == AI:
        row, col = find_best_move(board)
        if row != -1 and col != -1:
            mark_square(board, row, col, AI)
        player_turn = HUMAN
        status = f"Your Turn (X) | AI searched {nodes_explored} nodes"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos

            if btn.collidepoint(mouseX, mouseY):
                board = create_board()
                game_over = False
                player_turn = HUMAN
                status = "Your Turn (X)"
                continue

            if mouseY < BOARD_SIZE and not game_over and player_turn == HUMAN:
                clicked_row = mouseY // CELL_SIZE
                clicked_col = mouseX // CELL_SIZE

                if available_square(board, clicked_row, clicked_col):
                    mark_square(board, clicked_row, clicked_col, HUMAN)
                    player_turn = AI
                    status = "AI Thinking..."