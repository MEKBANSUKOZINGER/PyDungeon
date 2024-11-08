import pygame
import asyncio
import sys
import random

# 파이게임 초기화
pygame.init()


# General Settings
gravity = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("턴전")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Player :
    def __init__(self, player_posX, player_posY, player_size, player_velocity) :
        self.playerPos = [player_posX, player_posY] #[x, y]
        self.playerSize = player_size
        self.playerVelocity = player_velocity
        self.isJumping = False
        self.jumpCount = 10
        self.fallSpeed = 0

        self.canCollide = True

        self.isDashing = False
        self.acceleration = 5
        self.dashDirection = 1

        self.isAttacking = False

    async def Draw(self) :
        pygame.draw.rect(screen, BLUE, (self.playerPos[0], self.playerPos[1], self.playerSize, self.playerSize))
        await asyncio.sleep(0)

    async def Update(self) :
        #print(self.playerPos)
        # 중력 설정
        self.playerPos[1] += self.fallSpeed
        self.fallSpeed += gravity
    
        # 대쉬 업데이트
        if self.isDashing :
            print("ImDashing")
            # 대쉬 방향 결정
            if self.playerPos[0] < 0 :
                self.dashDirection = 1
            elif self.playerPos[0] > SCREEN_WIDTH - self.playerSize:
                self.dashDirection = -1
            
            # 가속도가 0이 되면 (보다 작아지면) 대쉬 종료
            if self.acceleration <= 0 :
                self.isDashing = False
            
            # 대쉬 실행
            else :
                self.playerPos[0] += self.acceleration * self.dashDirection
                self.acceleration -= 0.4
        
        # 점프 업데이트
        if self.isJumping :
            print("ImJumping")
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount <= 0:
                    neg = -1
                if self.jumpCount <= 7 :
                    self.canCollide = True
                else :
                    self.canCollide = False
                self.playerPos[1] -= (self.jumpCount ** 2) * 0.4 * neg
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = 30

        await asyncio.sleep(0)

    async def BoxCollider(self, _platforms) :
        # 바닥 상시 체크
        if self.playerPos[1] >= 550 :
            self.playerPos[1] = 550 - self.playerSize
            self.fallSpeed = 0
        
        # 플랫퐄 체크
        for platform in _platforms:
            if platform.colliderect(pygame.Rect(self.playerPos[0], self.playerPos[1], self.playerSize, self.playerSize)):
                # 캐릭터가 플랫폼 위에 있을 때
                if self.canCollide:
                    self.playerPos[1] = platform.top - self.playerSize
                    self.fallSpeed = 0
                    self.isJumping = False
                    #self.jumpCount = 30
            await asyncio.sleep(0)
        await asyncio.sleep(0)
    
    async def Attack(self, attackType) :
        if attackType == "Dash_E":
            self.fallSpeed = 0
            self.isDashing = True
            self.dashDirection = 1
            self.acceleration = 25  # 초기 대쉬 속도 설정
        elif attackType == "Jump" :
            self.isJumping = True
            self.fallSpeed = 0
            self.jumpCount = 11
            self.canCollide = False
        elif attackType == "Dash_Q":
            self.fallSpeed = 0
            self.isDashing = True
            self.dashDirection = -1
            self.acceleration = 25  # 초기 대쉬 속도 설정
        await asyncio.sleep(0)

class EnemyContainer :
    def __init__(self, attacker, player) :
        self.container = []
        self.attacker = attacker
        self.player = player
        self.isCleared = True

    async def Update(self) :
        for enemy in self.container :
            await enemy.Update()
        await self.checkClear()
    
    async def Draw(self) :
        for enemy in self.container :
            await enemy.Draw()
            #print(enemy.enemyPos)

    async def generateEnemies(self) :
        for _ in range(5) :
            enemy = Enemy()
            #print(enemy.enemyPos)
            self.container.append(enemy)
            await asyncio.sleep(0)
        await asyncio.sleep(0)
    
    async def nextMap(self) :
        if self.isCleared :
            await self.generateEnemies()
            self.attacker.randomMapGenerate()
            self.isCleared = False
        await asyncio.sleep(0)

    async def checkClear(self) :
        if len(self.container) == 0 :
            self.isCleared = True
            await asyncio.sleep(0)
        else :
            self.isCleared = False
            await asyncio.sleep(0)

        for i in range(len(self.container)) :
            print("Done")
            if i < len(self.container) and self.container[i].checkDie(self.player) :
                print("Pop!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n\n\n\n\n")
                self.container.pop(i)
            await asyncio.sleep(0)
        await asyncio.sleep(0)

    async def BoxCollider(self, _platforms) :
        for enemy in self.container :
            await enemy.BoxCollider(_platforms)

class Enemy :
    def __init__(self) :
        self.enemyPos = [random.randint(0,SCREEN_WIDTH // 10) * 10, -10]
        #print(self.enemyPos)
        self.enemySize = 30
        self.fallSpeed = 0

    async def Draw(self) :
        #print("Drawn")
        pygame.draw.rect(screen, RED, (self.enemyPos[0], self.enemyPos[1], self.enemySize, self.enemySize))
        await asyncio.sleep(0)

    async def Update(self) :
        # 중력 설정
        self.enemyPos[1] += self.fallSpeed
        self.fallSpeed += gravity
        #print(self.enemyPos)
        await asyncio.sleep(0)

    async def BoxCollider(self, _platforms) :
        # 바닥 상시 체크
        if self.enemyPos[1] >= 550 :
            self.enemyPos[1] = 550 - self.enemySize
            self.fallSpeed = 0
        
        # 플랫퐄 체크
        for platform in _platforms:
            if platform.colliderect(pygame.Rect(self.enemyPos[0], self.enemyPos[1], self.enemySize, self.enemySize)):
                # 캐릭터가 플랫폼 위에 있을 때
                self.enemyPos[1] = platform.top - self.enemySize
                self.fallSpeed = 0
            await asyncio.sleep(0)
        await asyncio.sleep(0)

    def checkDie(self, player) :
        if (abs(self.enemyPos[0] - player.playerPos[0]) <= 100) and (abs(self.enemyPos[1] - player.playerPos[1]) <= 100) :
            print("Dead")
            return True
        else :
            return False


class Attacker :
    def __init__(self) :
        self.attackNodes = []
        self.width = 205
        self.height = 30
        self.posY = 10
        self.isLarge = False
        self.isAttacking = False

        self.attackCooltime = 500

        self.randomMap = random.randint(0,len(platformContainer) - 1)

    def randomMapGenerate(self) : random.randint(0,len(platformContainer) - 1)

    async def Draw(self) :
        pygame.draw.rect(screen, BLUE, ((SCREEN_WIDTH - self.width) // 2, self.posY, self.width, self.height))
        for i in range(len(self.attackNodes)) :
            if self.isLarge :
                await self.attackNodes[i].Draw((SCREEN_WIDTH - self.width) // 2 + 10 + 70 * (i), self.posY + 10, 60, 60)
            else :
                await self.attackNodes[i].Draw((SCREEN_WIDTH - self.width) // 2 + 5 + 25 * (i), self.posY + 5, 20, 20)
            await asyncio.sleep(0)
        await asyncio.sleep(0)



    async def EnableSelf(self) :
        self.isLarge = not self.isLarge
        if self.isLarge : 
            self.width, self.height = 570, 80  # 큰 네모 크기
            self.posY = 200  # 아래로 이동
        else :
            self.width, self.height = 205, 30  # 작은 네모 크기
            self.posY = 10  # 원래 위치
        await asyncio.sleep(0)

    async def AttackInput(self, _nodeType) :
        if not self.isLarge :
            return
        if len(self.attackNodes) == 8 :
            print("Full!")
            return
        self.attackNodes.append(Node(_nodeType))
        await asyncio.sleep(0)

    async def DeleteAttackNode(self) :
        if len(self.attackNodes) == 0 :
            return
        self.attackNodes.pop()
        await asyncio.sleep(0)

    async def AttackCoroutine(self, player) :
        currentIndex = 0
        currentTime = pygame.time.get_ticks()
        self.isAttacking = True
        self.isLarge = True
        await attacker.EnableSelf()
        for node in self.attackNodes :
            await player.Attack(node.GetType())
            await asyncio.sleep(0.25)
        self.isAttacking = False
        await asyncio.sleep(0)


class Node :
    def __init__(self, nodeType) :
        self.type = nodeType

    def GetType(self) : return self.type

    async def Draw(self, posX, posY, width, height) :
        pygame.draw.rect(screen, WHITE, (posX, posY, width, height))
        await asyncio.sleep(0)



# 플랫폼 설정
floor = pygame.Rect(0, 550, SCREEN_WIDTH, 50)

platformContainer = [
        [   
        pygame.Rect(0, 550, SCREEN_WIDTH, 50),
        pygame.Rect(300, 450, 200, 30),  # 공중 플랫폼
        pygame.Rect(600, 400, 300, 30),
        pygame.Rect(0, 100, 250, 30),
        pygame.Rect(100, 320, 300, 30),
        pygame.Rect(170, 200, 130, 30),
        pygame.Rect(490, 160, 240, 30),
    ], 
        [   
        pygame.Rect(0, 550, SCREEN_WIDTH, 50),
        pygame.Rect(400, 250, 100, 30),  # 공중 플랫폼
        pygame.Rect(100, 400, 200, 30),
        pygame.Rect(350, 350, 350, 30),
        pygame.Rect(520, 470, 100, 30),
        pygame.Rect(80, 100, 50, 30),
        pygame.Rect(290, 160, 140, 30),
        pygame.Rect(0, 260, 140, 30),
    ]
]

player = Player(100, 500, 30, 0.5)

attacker = Attacker()

enemyContainer = EnemyContainer(attacker, player)
# 메인 루프

clock = pygame.time.Clock()


async def main():
    running = True
    attack_task = None  # 공격 태스크 초기화

    while running:
        tick = clock.tick(360)
        pygame.time.delay(25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not attacker.isAttacking and (not player.isDashing or not player.isJumping) :
                    if event.key == pygame.K_a:
                        await attacker.EnableSelf()
                    if event.key == pygame.K_q:
                        await attacker.AttackInput("Dash_Q")
                    if event.key == pygame.K_w:
                        await attacker.AttackInput("Jump")
                    if event.key == pygame.K_e:
                        await attacker.AttackInput("Dash_E")
                    if event.key == pygame.K_RETURN:
                        # 새로운 공격 태스크를 실행
                        if attack_task is None or attack_task.done():
                            attack_task = asyncio.create_task(attacker.AttackCoroutine(player))
                    if event.key == pygame.K_BACKSPACE:
                        await attacker.DeleteAttackNode()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            # 저장 기능 (된다면)
            running = False

        # 중력 적용
        await enemyContainer.nextMap()

        await enemyContainer.Update()

        await player.Update()

        # 바닥 충돌 처리
        #await player.BoxCollider(floor)

        await player.BoxCollider(platformContainer[attacker.randomMap])

        await enemyContainer.BoxCollider(platformContainer[attacker.randomMap])

        # 화면 업데이트
        screen.fill(WHITE)

        # 플랫폼 그리기
        pygame.draw.rect(screen, GREEN, floor)
        for platform in platformContainer[attacker.randomMap]:
            pygame.draw.rect(screen, GREEN, platform)

        # 캐릭터 그리기
        await player.Draw()

        # 어택 노드 그리기
        await attacker.Draw()

        
        await enemyContainer.Draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# asyncio 루프 실행
asyncio.run(main())