import pygame
import sys

# 파이게임 초기화
pygame.init()


# General Settings
gravity = 2

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("턴전")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Player :
    def __init__(self, player_posX, player_posY, player_size, player_velocity) :
        self.playerPos = [player_posX, player_posY] #[x, y]
        self.playerSize = player_size
        self.playerVelocity = player_velocity
        self.isJumping = False
        self.jumpCount = 10
        self.fallSpeed = 0

    def Draw(self) :
        pygame.draw.rect(screen, BLUE, (self.playerPos[0], self.playerPos[1], self.playerSize, self.playerSize))

    def Move(self) :
        if keys[pygame.K_LEFT] and self.playerPos[0] > 0:
            self.playerPos[0] -= self.playerVelocity
        if keys[pygame.K_RIGHT] and self.playerPos[0] < screen_width - self.playerSize:
            self.playerPos[0] += self.playerVelocity
        if not self.isJumping:
            if keys[pygame.K_SPACE]:
                self.isJumping = True
        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.playerPos[1] -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = 10

    def Gravity(self) :
        self.playerPos[1] += self.fallSpeed
        self.fallSpeed += gravity
    
    def BoxCollider(self, _platforms) :
        for platform in _platforms:
            if platform.colliderect(pygame.Rect(self.playerPos[0], self.playerPos[1], self.playerSize, self.playerSize)):
                # 캐릭터가 플랫폼 위에 있을 때
                if self.playerPos[1] + self.playerSize <= platform.top + self.fallSpeed:
                    self.playerPos[1] = platform.top - self.playerSize
                    self.fallSpeed = 0
                    self.isJumping = False
                    self.jumpCount = 10

# 플랫폼 설정
platforms = [
    pygame.Rect(0, 550, screen_width, 50),  # 바닥 플랫폼
    pygame.Rect(300, 450, 200, 20),  # 공중 플랫폼
    pygame.Rect(600, 400, 150, 20)   # 또 다른 공중 플랫폼
]

player = Player(100, 500, 30, 15)

# 메인 루프
running = True
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE] :
        # 여기에서 꺼질 때 상호작용 추가 할 수 있음
        running = False
    
    # 캐릭터 이동
    player.Move()

    # 중력 적용
    player.Gravity()

    # 바닥 충돌 처리
    player.BoxCollider(platforms)

    # 화면 업데이트
    screen.fill(WHITE)

    # 플랫폼 그리기
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # 캐릭터 그리기
    player.Draw()

    pygame.display.flip()

# 파이게임 종료
pygame.quit()
sys.exit()
