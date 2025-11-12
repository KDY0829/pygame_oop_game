import pygame
from config import RED, TEXT, SELECT, CELL

BLACK = (0, 0, 0)
_num_font = None

def _font():
    global _num_font
    if _num_font is None:
        _num_font = pygame.font.Font(None, 24)
    return _num_font

# 보드의 한 칸(사과 셀)을 표현하는 클래스
class Item:
    """
    gx, gy : 보드 내 위치 (격자 좌표)
    value  : 사과의 숫자 (1~9)
    removed: 제거 여부 (True면 빈칸)
    highlight: 드래그 중 선택 표시
    apple_img: 사과 이미지 (없으면 원형 그림)
    """
    def __init__(self, gx, gy, value, apple_img=None):
        self.gx, self.gy = gx, gy
        self.value = value
        self.removed = False
        self.highlight = False
        self.apple_img = apple_img

    def draw(self, surf, rect):
        if self.removed:
            return
        # 배경
        if self.apple_img:
            surf.blit(self.apple_img, self.apple_img.get_rect(center = rect.center))
        else:
            color = SELECT if self.highlight else RED
            pygame.draw.circle(surf, color, rect.center, CELL // 2 - 5)

        # 숫자
        num = _font().render(str(self.value), True, BLACK)
        surf.blit(num, num.get_rect(center=rect.center))

        if self.highlight and self.apple_img:
            pygame.draw.rect(surf, SELECT, rect, width=2, border_radius=8)