# manager.py 파일

# ⭐️ 나중에 구현할 화면들을 미리 불러옵니다.
from factory_screen import Game as FactoryScreen # Game 클래스가 factory_screen으로 옮겨갔다고 가정
# from map_screen import MapScreen # 나중에 만들 파일

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_state = "FACTORY"  # 시작은 공장 화면으로 설정 (MAP 또는 FACTORY)
        
        # ⭐️ 각 화면 객체를 초기화합니다.
        self.factory_screen = FactoryScreen(screen, self) # 자신(manager)의 객체를 전달하여 화면 전환 요청을 받게 함
        # self.map_screen = MapScreen(screen, self) # MapScreen은 아직 없으므로 주석 처리

    def run(self):
        # ⭐️ 현재 상태에 따라 해당 화면을 실행
        if self.current_state == "FACTORY":
            self.factory_screen.run()
        # elif self.current_state == "MAP":
            # self.map_screen.run() # MapScreen은 나중에 구현

    def change_state(self, new_state):
        """ 다른 화면에서 이 함수를 호출하여 화면 전환을 요청합니다. """
        self.current_state = new_state
        print(f"화면 상태가 {new_state}로 변경되었습니다.") # 확인용

# ⭐️ 기존 app.py에 있던 모든 import 문들은 factory_screen.py로 옮겨졌는지 확인하세요!