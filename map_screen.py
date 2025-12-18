# map_screen.py 파일
import pygame

class MapScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        # ⭐️ 맵 관련 변수들을 여기에 넣을 것입니다.
        # 예: self.tiles = [] 
    
    def handle_event(self, event):
        """ 이벤트 처리 (마우스 클릭, 키보드 입력 등) """
        
        # ⭐️ 공장 화면으로 전환하는 키(예: 'F')를 여기에 구현합니다.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # F 키를 누르면
                self.manager.change_state("FACTORY")
        pass

    def run(self):
        """ 맵 화면의 로직 업데이트 및 화면 그리기 """
        
        # 1. 로직 업데이트 (군대 이동, 자원 생산 등)
        # 2. 화면 그리기 (육각형 타일, 군대 아이콘 등)
        
        self.screen.fill((50, 50, 150)) # 임시로 파란색 배경 채우기