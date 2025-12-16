# main.py 파일 수정 (이제 시작 파일 역할만 남습니다)

import pygame
# ⭐️ 중요: manager.py 파일에서 Game 클래스를 GameManager로 불러오기
from manager import Game as GameManager 

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gong Jang Game")

# ⭐️ 수정: Game 클래스 대신 GameManager 클래스 사용
game = GameManager(screen) 
clock = pygame.time.Clock()
running = True

while running:
    # ⭐️ 이벤트 처리 및 게임 루프는 그대로 둠
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ... 키 입력 처리 등 다른 이벤트 처리도 그대로 둠 ...

    game.run() # Game 클래스(이제 GameManager)의 run 함수 호출
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()