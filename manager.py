import pygame
# ⭐️ 중요: 다른 화면 클래스들을 불러옵니다.
from factory_screen import Game as FactoryScreen
from map_screen import MapScreen  

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        
        # ⭐️ 초기 상태 설정: 맵 화면에서 시작
        self.current_state = "MAP"  # "MAP" 또는 "FACTORY"

        # ⭐️ 각 화면 객체를 초기화합니다.
        # self를 넘겨서, 각 화면이 manager.change_state()를 호출할 수 있도록 합니다.
        self.factory_screen = FactoryScreen(screen, self)
        self.map_screen = MapScreen(screen, self)
        
        # 참고: 전역적으로 관리할 데이터(자원, 기술 등)는 여기에 정의합니다.
        # self.resources = {'Iron': 100, 'Oil': 50} 


    def handle_event(self, event):
        """ 이벤트를 현재 활성화된 화면으로 전달합니다. """
        
        # ⭐️ 현재 상태에 따라 해당 화면의 이벤트 핸들러를 호출
        if self.current_state == "FACTORY":
            self.factory_screen.handle_event(event) 
        elif self.current_state == "MAP":
            self.map_screen.handle_event(event)

    def run(self):
        """ 현재 화면의 로직 업데이트 및 화면 그리기 함수를 호출합니다. """
        
        # ⭐️ 현재 상태에 따라 해당 화면의 run 함수를 실행
        if self.current_state == "FACTORY":
            self.factory_screen.run()
        elif self.current_state == "MAP":
            self.map_screen.run()

    def change_state(self, new_state):
        """ 다른 화면에서 이 함수를 호출하여 화면 전환을 요청합니다. """
        
        # ⭐️ 유효한 상태인지 확인 후 변경
        if new_state in ["MAP", "FACTORY"]:
            self.current_state = new_state
            print(f"화면 상태가 {new_state}로 변경되었습니다.") 
        else:
            print(f"경고: 알 수 없는 화면 상태 '{new_state}' 요청됨")