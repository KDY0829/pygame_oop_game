# 메인 게임 루프

import sys
import pygame
from config import (
    WIDTH, HEIGHT, FPS, GAME_TIME,
    DRAG_FILL, DRAG_BORDER, CELL, BG
)
from background import Background
from board import Board
from player import Player

# 게임 상태 상수
INTRO, PLAYING, GAME_OVER = 0, 1, 2


class Game:
    def __init__(self):
        #  pygame 전체 초기화
        pygame.init()

        #  창(display), 타이틀, 시계(time)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🍎 Sum 10 - 사과 퍼즐")
        self.clock = pygame.time.Clock()


        self.bg = Background()   # 버튼/텍스트 UI
        self.board = Board()     # 17×10 그리드 + 사과 이미지
        self.player = Player()   # 드래그 선택 상태


        self.state = INTRO
        self.score = 0
        self.start_ticks = 0     # PLAYING 시작 시각(ms)
        self.time_left = GAME_TIME
        self.running = True

        self.hover = False


    def reset(self):
        self.board = Board()
        self.player = Player()
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.time_left = GAME_TIME
        self.state = PLAYING


    def run(self):
        while self.running:
            self.handle_events()     # 입력 처리 (event)
            self.update()            # 시간/상태 갱신 (time)
            self.render()            # 화면 그리기 (display/image)
            self.clock.tick(FPS)     # FPS 고정
        pygame.quit()
        sys.exit()


    def handle_events(self):
        ui_x = self.board.rect.right + 20
        hover_rect = pygame.Rect(ui_x, 400, 140, 48)
        self.hover = hover_rect.collidepoint(pygame.mouse.get_pos())

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.running = False

            if self.state == INTRO:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self.reset()

            elif self.state == PLAYING:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if self.hover:
                        self.reset()
                    else:
                        self.player.start_drag(e.pos, self.board)
                elif e.type == pygame.MOUSEMOTION:
                    self.player.drag(e.pos, self.board)
                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    self.score += self.player.end_drag(self.board)

            elif self.state == GAME_OVER:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.hover:
                    self.reset()

    def update(self):
        if self.state == PLAYING:
            elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000.0
            self.time_left = GAME_TIME - elapsed
            if self.time_left <= 0:
                self.state = GAME_OVER

    def render(self):
        ui_x = self.board.rect.right + 20
        self.screen.fill(BG)

        if self.state == INTRO:
            self.bg.draw_intro(self.screen)

        elif self.state == PLAYING:
            self.board.draw(self.screen)
            self._draw_drag_box()
            self.bg.draw_play(self.screen, self.score, self.time_left, self.hover, ui_x)

        else:  # GAME_OVER
            self.bg.draw_gameover(self.screen, self.score, self.hover, ui_x)

        pygame.display.flip()

    def _draw_drag_box(self):
        info = self.player.drag_box()
        if not info:
            return
        gx, gy, gw, gh = info
        # 격자 좌표 → 픽셀 좌표
        x = self.board.rect.x + gx * CELL
        y = self.board.rect.y + gy * CELL
        w = gw * CELL
        h = gh * CELL

        # 반투명 채움 Surface를 만들어 붙이기(blit)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill(DRAG_FILL)  # (r,g,b,a)
        self.screen.blit(s, (x, y))

        # 테두리
        pygame.draw.rect(self.screen, DRAG_BORDER, (x, y, w, h), width=3, border_radius=6)
