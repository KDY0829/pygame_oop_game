import pygame, random, os
from entities import Item
from config import BOARD_W, BOARD_H, CELL, MARGIN, GRID

class Board:
    def __init__(self):
        # 보드 영역 설정
        self.rect = pygame.Rect(MARGIN, MARGIN, BOARD_W*CELL, BOARD_H*CELL)

        # 2차원 배열
        self.grid = [[None for _ in range(BOARD_W)] for _ in range(BOARD_H)]

        self.apple_img = self._load_apple_img()

    def _load_apple_img(self):
        path = os.path.join('./images/apple.png')
        if not os.path.exists(path):
            return None
        try:
            img = pygame.image.load(path).convert_alpha()
            size = CELL - 6
            return pygame.transform.smoothscale(img, (size, size))
        except Exception:
            return None
        
    # 1~9까지 랜덤으로 보드 채우기
    def fill_board(self):
        for y in range(BOARD_H):
            for x in range(BOARD_W):
                self.grid[y][x] = Item(x, y, random.randint(1, 9), self.apple_img)

    # 마우스 좌표 > 보드 격자 좌표
    def cell_from_pos(self, pos):
        px, py = pos
        if not self.rect.collidepoint(px, py):
            return None, None
        gx = (px - self.rect.x) // CELL
        gy = (py - self.rect.y) // CELL
        return int(gx), int(gy)
        