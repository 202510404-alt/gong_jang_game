"""
간단한 2D 공장 기본 화면 (Pygame)
- 화면: 1280x720
- 요소: 격자 배경, 상단 자원 바, 좌측 패널(기계 배치 더미)

실행: python main.py
필수: pip install pygame
"""

import sys
import pygame

# 화면 설정
WIDTH, HEIGHT = 1280, 720
FPS = 60

# 색상 팔레트
BG_COLOR = (24, 28, 34)
GRID_COLOR = (48, 55, 66)
TOP_BAR_COLOR = (32, 38, 46)
LEFT_PANEL_COLOR = (36, 42, 52)
TEXT_COLOR = (220, 230, 240)
HINT_COLOR = (120, 170, 255)
BUTTON_BG = (52, 60, 72)
BUTTON_ACTIVE_BG = (80, 110, 160)
BUTTON_BORDER = (70, 80, 95)

GRID_SIZE = 40
TOP_BAR_HEIGHT = 72
LEFT_PANEL_WIDTH = 220

MODE_FACTORY = "factory_edit"
MODE_COMPANY = "company_mgmt"


def get_font(size: int) -> pygame.font.Font:
    """한국어 글꼴 우선 시도 후 기본 폰트로 폴백."""
    candidates = [
        "Noto Sans CJK KR",
        "Noto Sans KR",
        "NanumGothic",
        "Malgun Gothic",
        None,  # 시스템 기본
    ]
    for name in candidates:
        try:
            return pygame.font.SysFont(name, size)
        except Exception:
            continue
    # 최종 폴백
    return pygame.font.Font(None, size)


class Button:
    """좌측 패널 버튼(라벨+클릭 영역)."""

    def __init__(self, rect: pygame.Rect, label: str, action) -> None:
        self.rect = rect
        self.label = label
        self.action = action

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, active: bool) -> None:
        bg = BUTTON_ACTIVE_BG if active else BUTTON_BG
        pygame.draw.rect(screen, bg, self.rect, border_radius=6)
        pygame.draw.rect(screen, BUTTON_BORDER, self.rect, width=1, border_radius=6)
        text_surf = font.render(self.label, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_click(self, pos: tuple[int, int]) -> None:
        if self.rect.collidepoint(pos):
            self.action()


class UIState:
    """간단한 상태 저장: 돈, 자원, 선택 도구 등."""

    def __init__(self) -> None:
        self.money = 1_000_000
        self.steel = 120
        self.battery = 40
        self.mode = MODE_FACTORY
        self.selected_tool = "컨베이어"
        self.buttons: dict[str, list[Button]] = {MODE_FACTORY: [], MODE_COMPANY: []}


class FactoryView:
    """공장 캔버스와 UI 영역을 그리는 책임."""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        self.screen = screen
        self.font = font

    def draw_grid(self) -> None:
        # 격자: 공장 영역만 (상단바/좌측 패널 제외)
        start_x = LEFT_PANEL_WIDTH
        start_y = TOP_BAR_HEIGHT
        for x in range(start_x, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, start_y), (x, HEIGHT))
        for y in range(start_y, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (start_x, y), (WIDTH, y))

    def draw_top_bar(self, state: UIState) -> None:
        pygame.draw.rect(self.screen, TOP_BAR_COLOR, (0, 0, WIDTH, TOP_BAR_HEIGHT))
        text_items = [
            f"자금: ${state.money:,}",
            f"강철: {state.steel}",
            f"배터리: {state.battery}",
        ]
        x = 16
        for item in text_items:
            surf = self.font.render(item, True, TEXT_COLOR)
            self.screen.blit(surf, (x, 20))
            x += surf.get_width() + 40

    def draw_left_panel(self, state: UIState) -> None:
        pygame.draw.rect(
            self.screen, LEFT_PANEL_COLOR, (0, TOP_BAR_HEIGHT, LEFT_PANEL_WIDTH, HEIGHT)
        )
        title = self.font.render("메뉴", True, TEXT_COLOR)
        self.screen.blit(title, (16, TOP_BAR_HEIGHT + 12))

        # 모드 전환 버튼
        mode_buttons = state.buttons.get("modes", [])
        for btn in mode_buttons:
            btn.draw(self.screen, self.font, active=(state.mode in btn.label))

        # 모드별 패널
        if state.mode == MODE_FACTORY:
            self._draw_factory_panel(state)
        else:
            self._draw_company_panel(state)

    def _draw_factory_panel(self, state: UIState) -> None:
        label = self.font.render("공장 편집", True, HINT_COLOR)
        self.screen.blit(label, (16, TOP_BAR_HEIGHT + 70))
        tool_buttons = state.buttons.get(MODE_FACTORY, [])
        for btn in tool_buttons:
            btn.draw(self.screen, self.font, active=(btn.label == state.selected_tool))

        hint_lines = [
            "도구 선택 후 격자에 배치(예정)",
            "ESC 또는 창 닫기: 종료",
        ]
        y = TOP_BAR_HEIGHT + 70 + 6 * 12
        for line in hint_lines:
            surf = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(surf, (16, y))
            y += 26

    def _draw_company_panel(self, state: UIState) -> None:
        label = self.font.render("회사 관리", True, HINT_COLOR)
        self.screen.blit(label, (16, TOP_BAR_HEIGHT + 70))
        info_lines = [
            "- 계약/이미지/전략 (더미)",
            "- 공장 선택 시 해당 화면 이동 예정",
            "- AI 회사 계약/경쟁은 이후 단계",
        ]
        y = TOP_BAR_HEIGHT + 100
        for line in info_lines:
            surf = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(surf, (16, y))
            y += 26


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("간단한 공장 화면 (MVP)")
    clock = pygame.time.Clock()
    font = get_font(20)

    state = UIState()
    view = FactoryView(screen, font)

    # 버튼 구성
    modes_buttons: list[Button] = []

    def set_mode_factory() -> None:
        state.mode = MODE_FACTORY

    def set_mode_company() -> None:
        state.mode = MODE_COMPANY

    modes_buttons.append(
        Button(
            pygame.Rect(16, TOP_BAR_HEIGHT + 30, LEFT_PANEL_WIDTH - 32, 28),
            "공장 편집",
            set_mode_factory,
        )
    )
    modes_buttons.append(
        Button(
            pygame.Rect(16, TOP_BAR_HEIGHT + 30 + 32, LEFT_PANEL_WIDTH - 32, 28),
            "회사 관리",
            set_mode_company,
        )
    )

    factory_tools = ["컨베이어", "기계", "직원", "특수 장비"]
    tool_buttons: list[Button] = []

    def make_tool_setter(name: str):
        return lambda: setattr(state, "selected_tool", name)

    start_y = TOP_BAR_HEIGHT + 100
    for idx, tool_name in enumerate(factory_tools):
        y = start_y + idx * 34
        btn = Button(
            pygame.Rect(16, y, LEFT_PANEL_WIDTH - 32, 30),
            tool_name,
            make_tool_setter(tool_name),
        )
        tool_buttons.append(btn)

    state.buttons["modes"] = modes_buttons
    state.buttons[MODE_FACTORY] = tool_buttons

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for btn in state.buttons.get("modes", []):
                    btn.handle_click(pos)
                for btn in state.buttons.get(state.mode, []):
                    btn.handle_click(pos)

        screen.fill(BG_COLOR)
        view.draw_top_bar(state)
        view.draw_left_panel(state)
        view.draw_grid()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

