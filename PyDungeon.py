import pygame
import sys

# 파이게임 초기화
pygame.init()


# General Settings
gravity = 2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

        self.canCollide = True

    def Draw(self) :
        pygame.draw.rect(screen, BLUE, (self.playerPos[0], self.playerPos[1], self.playerSize, self.playerSize))

    def Move(self, tick) :
        if keys[pygame.K_LEFT] and self.playerPos[0] > 0:
            self.playerPos[0] -= self.playerVelocity * tick
        if keys[pygame.K_RIGHT] and self.playerPos[0] < SCREEN_WIDTH - self.playerSize:
            self.playerPos[0] += self.playerVelocity * tick
        if not self.isJumping:
            if keys[pygame.K_SPACE]:
                self.isJumping = True
        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount <= 0:
                    neg = -1
                if self.jumpCount <= 5 :
                    self.canCollide = True
                else :
                    self.canCollide = False
                self.playerPos[1] -= (self.jumpCount ** 2) * 0.015 * neg * tick
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
                if self.playerPos[1] + self.playerSize <= platform.top + self.fallSpeed and self.canCollide:
                    self.playerPos[1] = platform.top - self.playerSize
                    self.fallSpeed = 0
                    self.isJumping = False
                    self.jumpCount = 10

class Attacker :
    def __init__(self) :
        self.attackNodes = []
        self.width = 50
        self.height = 50
        self.posY = 10
        self.isLarge = False
    
    def Draw(self) :
        pygame.draw.rect(screen, BLUE, ((SCREEN_WIDTH - self.width) // 2, self.posY, self.width, self.height))
        for node in self.attackNodes :
            node.Draw()


    def EnableSelf(self) :
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a :
                self.isLarge = not self.isLarge
                if self.isLarge : 
                    self.width, self.height = 100, 100  # 큰 네모 크기
                    self.posY = 200  # 아래로 이동
                else :
                    self.width, self.height = 50, 50  # 작은 네모 크기
                    self.posY = 10  # 원래 위치

    def AttackInput(self) :
        if self.isLarge :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q :
                    self.attackNodes.append(Node("Attack", 30, 30))
                elif event.key == pygame.K_w :
                    self.attackNodes.append(Node("Jump", 30, 30))
                elif event.key == pygame.K_e :
                    self.attackNodes.append(Node("Dash", 30, 30))
                elif event.key == pygame.K_q :
                    self.attackNodes.append(Node("Jump", 30, 30))

class Node :
    def __init__(self, nodeType, node_width, node_height) :
        self.type = nodeType
        self.width = node_width
        self.height = node_height


# 플랫폼 설정
platforms = [
    pygame.Rect(0, 550, SCREEN_WIDTH, 50),  # 바닥 플랫폼
    pygame.Rect(300, 450, 200, 20),  # 공중 플랫폼
    pygame.Rect(600, 400, 150, 20)   # 또 다른 공중 플랫폼
]

player = Player(100, 500, 30, 0.5)

attacker = Attacker()

# 메인 루프

clock = pygame.time.Clock()

running = True
while running:
    tick = clock.tick(144)
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a :
                attacker.EnableSelf()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE] :
        # 여기에서 꺼질 때 상호작용 추가 할 수 있음
        running = False
    
    # 캐릭터 이동
    player.Move(tick)

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

    #어택 노드 그리기
    attacker.Draw()

    pygame.display.flip()

# 파이게임 종료
pygame.quit()
sys.exit()
