import os
import pygame
from config import BG, TEXT, BUTTON, BUTTON_HOVER, WIDTH, HEIGHT, SIDE_W, MARGIN

def _kfont(size: int) -> pygame.font.Font:
    win = os.environ.get("WINDIR", r"C:\Windows")
    candidates = [
        os.path.join(win, "Fonts", "malgun.ttf"),      # 맑은 고딕 Regular
        os.path.join(win, "Fonts", "malgunbd.ttf"),    # 맑은 고딕 Bold
        os.path.join(win, "Fonts", "gulim.ttc"),       # 굴림(대체)
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except Exception:
                pass
    # 최후 폴백(라틴만 가능)—한글 안나오면 빈칸이므로 위 후보가 반드시 선택되게 경로 확인 필요
    return pygame.font.SysFont("arial", size)

class Background:
    def __init__(self):
        self.font_big = _kfont(36)
        self.font_small = _kfont(22)
        self.btn_rect = pygame.Rect(0, 0, 140, 48)

    def draw_play(self, surf, score, time_left, hover, ui_x):
        right_rect = pygame.Rect(ui_x - 20, 0, SIDE_W, HEIGHT)
        pygame.draw.rect(surf, (220, 240, 225), right_rect)
        s = self.font_small.render(f"점수: {score}", True, TEXT)
        t = self.font_small.render(f"남은 시간: {int(time_left)}", True, TEXT)
        surf.blit(s, (ui_x, 60))
        surf.blit(t, (ui_x, 100))
        self.btn_rect.topleft = (ui_x, HEIGHT - 100)
        self._button(surf, "다시 시작", hover)

    def draw_intro(self, surf):
        surf.fill(BG)
        txt = self.font_big.render("클릭해서 시작!", True, TEXT)
        surf.blit(txt, txt.get_rect(center=surf.get_rect().center))

    def draw_gameover(self, surf, score, hover, ui_x):
        surf.fill(BG)
        txt = self.font_big.render(f"시간 종료! 점수: {score}", True, TEXT)
        surf.blit(txt, txt.get_rect(center=surf.get_rect().center))
        self.btn_rect.topleft = (ui_x, HEIGHT - 100)
        self._button(surf, "다시 시작", hover)

    def _button(self, surf, text, hover):
        c = BUTTON_HOVER if hover else BUTTON
        pygame.draw.rect(surf, c, self.btn_rect, border_radius=8)
        pygame.draw.rect(surf, TEXT, self.btn_rect, 2, border_radius=8)
        label = self.font_small.render(text, True, TEXT)
        surf.blit(label, label.get_rect(center=self.btn_rect.center))
