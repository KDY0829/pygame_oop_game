# 🍎 Sum 10 – 사과 퍼즐 (Pygame)

> **사과를 드래그해 합이 10이 되면 사과가 사라지는 미니 퍼즐 게임**  
> Pygame으로 제작된 간단한 집중력 & 계산력 트레이닝 게임입니다.

---

## 🎮 게임 소개

- 17 × 10 격자 위에 무작위 숫자(1–9)의 **사과 타일**이 배치됩니다.
- **드래그로 여러 사과를 선택**하여, 합이 **10**이 되면 선택한 사과들이 사라집니다.
- 사라진 자리에는 아무것도 채워지지 않습니다 (빈칸 유지).
- **100초** 동안 가능한 한 많은 조합을 만들어 **점수를 올리세요!**

---

## 🕹️ 조작 방법

| 조작              | 설명                    |
| ----------------- | ----------------------- |
| 🖱️ 드래그         | 사과 선택               |
| 🖱️ 드래그 해제    | 합계 확인 → 10이면 제거 |
| 🔁 다시 시작 버튼 | 새 게임 시작            |
| ⎋ ESC             | 게임 종료               |

---

## 🧩 주요 특징

- 객체지향(OOP) 구조
  - `Game`, `Board`, `Player`, `Background`, `Item` 클래스로 분리
- 상태 기반 로직
  - `INTRO`, `PLAYING`, `GAME_OVER` 세 가지 상태 전환
- 효과음 & 배경음
  - **Candy Theme (BGM)** – Pixabay
  - **Chewing Sound Effect** – Mixkit (“chewing something crunchy”)
- 마우스 기반 UI
  - 드래그 영역 반투명 표시, 버튼 hover 효과

---

## 📁 파일 구조

```text
MINIGAME/
├─ images/
│  └─ apple.png
├─ sounds/
│  └─ chew_crunch.wav
├─ music/
│  └─ candy_theme.mp3
├─ background.py
├─ board.py
├─ player.py
├─ entities.py
├─ config.py
├─ game.py
├─ main.py
└─ requirements.txt
```
---

## ⚙️ 실행 방법

pip install -r requirements.txt

- 게임 실행
  python main.py
