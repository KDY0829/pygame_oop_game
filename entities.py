import pygame
from config import RED, TEXT, SELECT, CELL

# pygame.font.SysFont()는 호출할 때마다 새 폰트 객체를 만듭니다.
# 매번 만들면 성능이 떨어지므로, 한 번만 생성 후 재사용하기 위해 캐싱

num_font = None

# 내부 전용 폰트 생성 함수
def _font():
    global num_font

    if num_font is None:
        num_font = pygame.font.SysFont('malgungothic', 22)

    return num_font

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
        num = _font().render(str(self.value), True, TEXT)
        surf.blit(num, num.get_rect(center=rect.center))

        if self.highlight and self.apple_img:
            pygame.draw.rect(surf, SELECT, rect, width=2, border_radius=8)