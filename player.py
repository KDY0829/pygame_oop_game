# 플레이어의 입력 처리 (마우스 드래그)
# - 빈칸도 클릭/드래그로 선택 가능하도록 변경
# - 하이라이트는 사과가 있는 칸에만 표시(빈칸은 시각 강조 없음)
# - 점수는 실제 제거된 "사과 개수"만 증가 (빈칸은 0점)

class Player:
    def __init__(self):
        self.dragging = False
        self.selected = [] # 드래그로 선택된 셀 좌표
        self.start = None # 드래그 시작 셀
        self.curr = None # 현재 마우스 셀

    def start_drag(self, pos, board):
        gx, gy = board.cell_from_pos(pos)
        if gx is None:
            return
        self.dragging = True
        self.start = (gx, gy)
        self.curr = (gx, gy)
        self.selected = [(gx, gy)]

        it = board.grid[gy][gx]
        if it is not None:
            it.highlight = True    

    def drag(self, pos, board):
        if not self.dragging:
            return
        gx, gy = board.cell_from_pos(pos)
        if gx is None:
            return
        self.curr = (gx, gy)

        if (gx, gy) not in self.selected:
            self.selected.append((gx, gy))
            it = board.grid[gy][gx]
            if it is not None:
                it.highlight = True

    def end_drag(self, board):
        if not self.dragging:
            return 0
        self.dragging = False

        # 드래그 사각형이 없으면 종료
        if not (self.start and self.curr):
            board.clear_highlights()
            self.selected.clear()
            self.start = None
            self.curr = None
            return 0

        # 드래그 시작/현재 셀로 사각형 내부 좌표 전부 선정 (포함 범위)
        x1, y1 = self.start
        x2, y2 = self.curr
        gx0, gx1 = (x1, x2) if x1 <= x2 else (x2, x1)
        gy0, gy1 = (y1, y2) if y1 <= y2 else (y2, y1)
        cells = [(x, y) for y in range(gy0, gy1 + 1) for x in range(gx0, gx1 + 1)]

        # 합이 10이면 제거(보드는 사과가 있는 칸만 합산/제거)
        score = board.remove_if_sum10(cells)

        # 흔적/하이라이트 초기화
        board.clear_highlights()
        self.selected.clear()
        self.start = None
        self.curr = None
        return score
    
    def drag_box(self):
        if not (self.start and self.curr):
            return None
        x1, y1 = self.start
        x2, y2 = self.curr
        return min(x1, x2), min(y1, y2), abs(x2 - x1) + 1, abs(y2 - y1) + 1