import pygame
import sys

GRAY = (177, 177, 177)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 20
block_size = 10
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800


class GameOfLife:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Life')
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.SCREEN.fill(WHITE)
        self.clock = pygame.time.Clock()
        self.board = [[0 for _ in range(int(WINDOW_HEIGHT / block_size))] for _ in range(int(WINDOW_WIDTH / block_size))]
        self.draw_grid()
        self.drawing_screen()
        self.game()

    def count_neighbors(self, i, j):
        count = 0
        for row in [-1, 0, 1]: 
            if i + row == -1 or i + row == len(self.board): # Don't check the upper and lower neighbors if the cell is in in upper / lower boundaries
                continue
            for col in [-1, 0, 1]:
                if j + col == -1 or j + col == len(self.board[0]) : # Don't check the left and right neighbors if the cell is in left / right boundaries
                    continue
                if row == 0 and col == 0: # Don't check the index itself
                    continue
                if self.board[i + row][j + col] == 1 or self.board[i + row][j + col] == -1:
                    count = count + 1
        return count

    def check(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                neighbors = self.count_neighbors(i, j)
                if self.board[i][j] == 0 and neighbors == 3:
                    self.board[i][j] = 2
                if self.board[i][j] == 1 and (neighbors < 2 or neighbors > 3):
                    self.board[i][j] = -1
        # Update the board to the final satate
        for i in range(len(self.board)): # Row
            for j in range(len(self.board[0])): # Column
                if self.board[i][j] == 2:
                    self.board[i][j] = 1
                if self.board[i][j] == -1:
                    self.board[i][j] = 0

    def draw_grid(self):
        self.SCREEN.fill(WHITE)
        for x in range(0, WINDOW_WIDTH, block_size):
            for y in range(0, WINDOW_HEIGHT, block_size):
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(self.SCREEN, GRAY, rect, 1)
        self.draw_all_cells()

    def draw_cell(self, mouseposition):
        x = mouseposition[0] // block_size
        y = mouseposition[1] // block_size
        if (mouseposition[1] < WINDOW_HEIGHT and mouseposition[0] < WINDOW_WIDTH):
            if self.board[x][y] == 0:
                self.board[x][y] = 1
                rectangle = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
                pygame.draw.rect(self.SCREEN, BLACK, rectangle)

            else:
                self.board[x][y] = 0
                rectangle = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
                pygame.draw.rect(self.SCREEN, WHITE, rectangle)
        self.draw_grid()

    def draw_all_cells(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 1:
                    rectangle = pygame.Rect(i * block_size, j * block_size, block_size, block_size)
                    pygame.draw.rect(self.SCREEN, BLACK, rectangle)

    def drawing_screen(self):
        loop = True
        font = pygame.font.SysFont('bahnschrift', 40)
        label = font.render("Press SPACE to start after drawing the pattern", 1, (0, 0, 0))
        text_rect = label.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.SCREEN.blit(label, text_rect)
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseposition =	pygame.mouse.get_pos()
                    self.draw_cell(mouseposition)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        loop = False
            pygame.display.update()
        self.draw_grid()
        
    def game(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.check()
            self.draw_grid()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.SCREEN.fill(WHITE) 
                        self.draw_grid()
                        self.drawing_screen()
            pygame.display.update()

if __name__ == "__main__":
    Game = GameOfLife()
    