# game.py — 메인 게임 루프 (효과음 추가 완성판)

import sys
import os
import pygame
from config import (
    WIDTH, HEIGHT, FPS, GAME_TIME,
    DRAG_FILL, DRAG_BORDER, CELL, BG,
    BGM_PATH, SFX_REMOVE_PATH, SFX_REMOVE_VOLUME
)
from background import Background
from board import Board
from player import Player

# 게임 상태 상수
INTRO, PLAYING, GAME_OVER = 0, 1, 2


# 오디오 초기화 함수
def safe_audio_init():
    """소리 장치 유무에 따라 자동으로 mixer 초기화 (없으면 무음)"""
    candidates = ["wasapi", "directsound", "winmm", "xaudio2", "dsound", "dummy"]
    for drv in candidates:
        os.environ["SDL_AUDIODRIVER"] = drv
        try:
            pygame.mixer.quit()
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            print(f"[AUDIO] Driver initialized: {drv}")
            return drv
        except pygame.error:
            continue
    print("[AUDIO] No usable driver found. Running silently.")
    return "dummy"


class Game:
    def __init__(self):
        pygame.init()

        # 오디오 초기화 (장치 없으면 dummy로)
        driver = safe_audio_init()

        # 배경음 로드 및 반복재생
        try:
            if driver != "dummy":
                pygame.mixer.music.load(BGM_PATH)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
            else:
                print("[INFO] 오디오 장치 없음 — 무음으로 실행합니다.")
        except Exception as e:
            print(f"[WARN] BGM 로드 실패: {e}")

        # 효과음 로드
        self.sfx_remove = None
        try:
            if driver != "dummy":
                self.sfx_remove = pygame.mixer.Sound(SFX_REMOVE_PATH)
                self.sfx_remove.set_volume(SFX_REMOVE_VOLUME)
        except Exception as e:
            print(f"[WARN] SFX 로드 실패: {e}")

        # 디스플레이 설정
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🍎 Sum 10 - 사과 퍼즐")
        self.clock = pygame.time.Clock()

        # 구성 요소 초기화
        self.bg = Background()
        self.board = Board()
        self.player = Player()

        self.state = INTRO
        self.score = 0
        self.start_ticks = 0
        self.time_left = GAME_TIME
        self.running = True
        self.hover = False

    # 게임 재시작
    def reset(self):
        self.board = Board()
        self.player = Player()
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.time_left = GAME_TIME
        self.state = PLAYING

    # 메인 루프
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    # 이벤트 처리
    def handle_events(self):
        ui_x = self.board.rect.right + 20
        btn_y = HEIGHT - 100 if self.state != INTRO else 400
        hover_rect = pygame.Rect(ui_x, btn_y, 140, 48)
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
                    gained = self.player.end_drag(self.board)
                    if gained > 0 and self.sfx_remove:  # ✅ 제거 성공 시 효과음
                        self.sfx_remove.play()
                    self.score += gained

            elif self.state == GAME_OVER:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.hover:
                    self.reset()

    # 시간 갱신
    def update(self):
        if self.state == PLAYING:
            elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000.0
            self.time_left = GAME_TIME - elapsed
            if self.time_left <= 0:
                self.state = GAME_OVER

    # 화면 렌더링
    def render(self):
        ui_x = self.board.rect.right + 20
        self.screen.fill(BG)

        if self.state == INTRO:
            self.bg.draw_intro(self.screen)
        elif self.state == PLAYING:
            self.board.draw(self.screen)
            self._draw_drag_box()
            self.bg.draw_play(self.screen, self.score, self.time_left, self.hover, ui_x)
        else:
            self.bg.draw_gameover(self.screen, self.score, self.hover, ui_x)

        pygame.display.flip()

    # 드래그 박스 (드래그 중만 표시)
    def _draw_drag_box(self):
        if not self.player.dragging:
            return
        info = self.player.drag_box()
        if not info:
            return
        gx, gy, gw, gh = info
        x = self.board.rect.x + gx * CELL
        y = self.board.rect.y + gy * CELL
        w = gw * CELL
        h = gh * CELL

        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill(DRAG_FILL)
        self.screen.blit(s, (x, y))
        pygame.draw.rect(self.screen, DRAG_BORDER, (x, y, w, h), width=3, border_radius=6)
