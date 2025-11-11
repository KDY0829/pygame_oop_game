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
        self._ensure_filled()

    def _ensure_filled(self):
        filled = sum(1 for row in self.grid for c in row if c is not None)
        if filled == 0:
            self.fill_board()

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
    
    # 격자 좌표 > 화면 rect 변환
    def cell_rect(self, gx, gy):
        return pygame.Rect(self.rect.x + gx*CELL, self.rect.y + gy*CELL, CELL, CELL)
    
    # 보드 전체
    def draw(self, surf):
        pygame.draw.rect(surf, GRID, self.rect)
        for y in range(BOARD_H):
            for x in range(BOARD_W):
                r = self.cell_rect(x, y)
                pygame.draw.rect(surf, (235, 240, 235), r, 0, border_radius=6)
                pygame.draw.rect(surf, (190, 210, 190), r, 1, border_radius=6)
                it = self.grid[y][x]
                if it:
                    it.draw(surf, r)
                else:
                    pygame.draw.rect(surf, (245, 245, 245), r, 0, border_radius=6)


    # 선택된 숫자들의 총합이 10이면 제거
    def remove_if_sum10(self, cells):
        items = [self.grid[y][x] for (x, y) in cells if self._valid_xy(x, y) and self.grid[y][x] and not self.grid[y][x].removed]
        total = sum(i.value for i in items)

        if total == 10 and items:
            for (x, y) in cells:
                self.grid[y][x] = None
            return len(items)
        return 0
    
    # 드래그 종료 시 하이라이트 해제
    def clear_highlights(self):
        for row in self.grid:
            for it in row:
                if it:
                    it.highlight = False

    def _valid_xy(self, x, y):
        return 0 <= x < BOARD_W and 0 <= y < BOARD_H
    

