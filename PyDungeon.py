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

playerIdleImg = pygame.image.load("./Images/Sonic/Sonic_Idle.png")
playerIdleImg = pygame.transform.scale(playerIdleImg, (60, 60))

playerIdleImages = [playerIdleImg, playerIdleImg, playerIdleImg, playerIdleImg]

playerRunImage1 = pygame.image.load("./Images/Sonic/Sonic_Run1.png")
playerRunImage1 = pygame.transform.scale(playerRunImage1, (60, 60))
playerRunImage2 = pygame.image.load("./Images/Sonic/Sonic_Run2.png")
playerRunImage2 = pygame.transform.scale(playerRunImage2, (60, 60))
playerRunImage3 = pygame.image.load("./Images/Sonic/Sonic_Run3.png")
playerRunImage3 = pygame.transform.scale(playerRunImage3, (60, 60))
playerRunImage4 = pygame.image.load("./Images/Sonic/Sonic_Run4.png")
playerRunImage4 = pygame.transform.scale(playerRunImage4, (60, 60))

playerRunImages = [playerRunImage1, playerRunImage2, playerRunImage3, playerRunImage4]

playerJumpImage = pygame.image.load("./Images/Sonic/Sonic_Jump.png")
playerJumpImage = pygame.transform.scale(playerJumpImage, (60, 60))

playerJumpImages = [playerJumpImage, playerJumpImage, playerJumpImage, playerJumpImage]

motoBugImage = pygame.image.load("./Images/Enemies/motobug.png")
motoBugImage = pygame.transform.scale(motoBugImage, (50, 50))

eggmanImage = pygame.image.load("./Images/Enemies/eggman.png")
eggmanImage = pygame.transform.scale(eggmanImage, (50, 50))

enemyImages = [motoBugImage, eggmanImage]

gr_200_50 = pygame.image.load("./Images/Platform/200_50_GR.png")
gr_200_50 = pygame.transform.scale(gr_200_50, (200, 30))

gr_200_50_forGround = pygame.image.load("./Images/Platform/200_50_GRR.png")
gr_200_50_forGround = pygame.transform.scale(gr_200_50_forGround, (200, 50))

gr_300_50 = pygame.image.load("./Images/Platform/300_50_GR.png")
gr_300_50 = pygame.transform.scale(gr_300_50, (300, 30))

backGround = pygame.image.load("./Images/BackGround/background.png")
backGround = pygame.transform.scale(backGround, (SCREEN_WIDTH, SCREEN_HEIGHT))

attacker_B = pygame.image.load("./Images/UI/AttackContainer_B.png")
attacker_B = pygame.transform.scale(attacker_B, (570, 80))

attacker_S = pygame.image.load("./Images/UI/AttackContainer_S.png")
attacker_S = pygame.transform.scale(attacker_S, (205, 30))

rightNode_B = pygame.image.load("./Images/UI/rightNode_B.png")
rightNode_B = pygame.transform.scale(rightNode_B, (60, 60))

leftNode_B = pygame.image.load("./Images/UI/leftNode_B.png")
leftNode_B = pygame.transform.scale(leftNode_B, (60, 60))

jumpNode_B = pygame.image.load("./Images/UI/jumpNode_B.png")
jumpNode_B = pygame.transform.scale(jumpNode_B, (60, 60))

rightNode_S = pygame.image.load("./Images/UI/rightNode_S.png")
rightNode_S = pygame.transform.scale(rightNode_S, (20, 20))

leftNode_S = pygame.image.load("./Images/UI/leftNode_S.png")
leftNode_S = pygame.transform.scale(leftNode_S, (20, 20))

jumpNode_S = pygame.image.load("./Images/UI/jumpNode_S.png")
jumpNode_S = pygame.transform.scale(jumpNode_S, (20, 20))

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

        self.drawImg = playerIdleImg
        self.runIndex = 0

    async def Draw(self) :
        if self.runIndex == 4 :
            self.runIndex = 0
            
        screen.blit(self.drawImg[self.runIndex], (self.playerPos[0], self.playerPos[1]))
        self.runIndex += 1
        await asyncio.sleep(0)

    async def Update(self) :
        #print(self.playerPos)
        # 중력 설정
        self.playerPos[1] += self.fallSpeed
        self.fallSpeed += gravity


        if self.fallSpeed > 2 :
            self.drawImg = playerJumpImages
        elif self.fallSpeed <= 2 and self.isDashing  : 
            self.drawImg = playerRunImages
        else :
            self.drawImg = playerIdleImages
    
        # 대쉬 업데이트
        if self.isDashing :
            print("ImDashing")
            # 대쉬 방향 결정
            if self.playerPos[0] < 0 :
                self.dashDirection = 1
                for i in range(len(playerIdleImages)) :
                    playerIdleImages[i] = pygame.transform.flip(playerIdleImages[i], True, False )
                for i in range(len(playerRunImages)) :
                    playerRunImages[i] = pygame.transform.flip(playerRunImages[i], True, False )
                for i in range(len(playerJumpImages)) :
                    playerJumpImages[i] = pygame.transform.flip(playerJumpImages[i], True, False )
            elif self.playerPos[0] > SCREEN_WIDTH - self.playerSize:
                self.dashDirection = -1
                for i in range(len(playerIdleImages)) :
                    playerIdleImages[i] = pygame.transform.flip(playerIdleImages[i], True, False )
                for i in range(len(playerRunImages)) :
                    playerRunImages[i] = pygame.transform.flip(playerRunImages[i], True, False )
                for i in range(len(playerJumpImages)) :
                    playerJumpImages[i] = pygame.transform.flip(playerJumpImages[i], True, False )
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
                if self.jumpCount <= 5 :
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
            if self.dashDirection == -1 :
                for i in range(len(playerIdleImages)) :
                    playerIdleImages[i] = pygame.transform.flip(playerIdleImages[i], True, False )
                for i in range(len(playerRunImages)) :
                    playerRunImages[i] = pygame.transform.flip(playerRunImages[i], True, False )
                for i in range(len(playerJumpImages)) :
                    playerJumpImages[i] = pygame.transform.flip(playerJumpImages[i], True, False )
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
            if self.dashDirection == 1 :
                for i in range(len(playerIdleImages)) :
                    playerIdleImages[i] = pygame.transform.flip(playerIdleImages[i], True, False )
                for i in range(len(playerRunImages)) :
                    playerRunImages[i] = pygame.transform.flip(playerRunImages[i], True, False )
                for i in range(len(playerJumpImages)) :
                    playerJumpImages[i] = pygame.transform.flip(playerJumpImages[i], True, False )
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
            #print("Done")
            if i < len(self.container) and self.container[i].checkDie(self.player) :
                #print("Pop!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n\n\n\n\n")
                self.container.pop(i)
            await asyncio.sleep(0)
        await asyncio.sleep(0)

    async def BoxCollider(self, _platforms) :
        for enemy in self.container :
            await enemy.BoxCollider(_platforms)

class Enemy :
    def __init__(self) :
        self.enemyPos = [random.randint(0,SCREEN_WIDTH // 10) * 10, random.randint(-10, 300)]
        #print(self.enemyPos)
        self.enemySize = 30
        self.fallSpeed = 0
        self.enemyIndex = random.randint(0, len(enemyImages) - 1)

    async def Draw(self) :
        #print("Drawn")
        #pygame.draw.rect(screen, RED, (self.enemyPos[0], self.enemyPos[1], self.enemySize, self.enemySize))
        screen.blit(enemyImages[self.enemyIndex], (self.enemyPos[0]-30, self.enemyPos[1]-15))
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
        if (abs(self.enemyPos[0] - player.playerPos[0]) <= 60) and (abs(self.enemyPos[1] - player.playerPos[1]) <= 60) :
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

        self.image = attacker_S

    def randomMapGenerate(self) : random.randint(0,len(platformContainer) - 1)

    async def Draw(self) :
        #pygame.draw.rect(screen, BLUE, ((SCREEN_WIDTH - self.width) // 2, self.posY, self.width, self.height))
        screen.blit(self.image, ((SCREEN_WIDTH - self.width) // 2, self.posY))
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
            self.image = attacker_B
            self.width, self.height = 570, 80  # 큰 네모 크기
            self.posY = 200  # 아래로 이동
        else :
            self.image = attacker_S
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
        if len(self.attackNodes) < 8 :
            return
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
        #pygame.draw.rect(screen, WHITE, (posX, posY, width, height))
        #print(width, height)
        if width == 20 and height == 20 :
            if self.type == "Dash_Q" :
                screen.blit(leftNode_S, (posX, posY))
            elif self.type == "Dash_E" :
                screen.blit(rightNode_S, (posX, posY))
            elif self.type == "Jump" :
                screen.blit(jumpNode_S, (posX, posY))
        if width == 60 and height == 60 :
            if self.type == "Dash_Q" :
                screen.blit(leftNode_B, (posX, posY))
            elif self.type == "Dash_E" :
                screen.blit(rightNode_B, (posX, posY))
            elif self.type == "Jump" :
                screen.blit(jumpNode_B, (posX, posY))
        await asyncio.sleep(0)



# 플랫폼 설정
floor = pygame.Rect(0, 550, SCREEN_WIDTH, 50)

platformContainer = [
        [   
        pygame.Rect(0, 550, SCREEN_WIDTH, 50),
        pygame.Rect(300, 450, 200, 10),  # 공중 플랫폼
        pygame.Rect(600, 400, 300, 10),
        pygame.Rect(0, 100, 200, 10),
        pygame.Rect(100, 320, 300, 10),
        pygame.Rect(170, 200, 200, 10),
        pygame.Rect(490, 160, 300, 10),
    ], 
        [   
        pygame.Rect(0, 550, SCREEN_WIDTH, 50),
        pygame.Rect(400, 250, 300, 10),  # 공중 플랫폼
        pygame.Rect(100, 400, 200, 10),
        pygame.Rect(350, 350, 300, 10),
        pygame.Rect(530, 450, 200, 10),
        pygame.Rect(150, 100, 200, 10),
        pygame.Rect(250, 160, 200, 10),
        pygame.Rect(0, 260, 200, 10),
    ]
]

player = Player(100, 500, 60, 0.5)

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

        screen.blit(backGround, (0, 0))

        # 플랫폼 그리기
        pygame.draw.rect(screen, GREEN, floor)
        for platform in platformContainer[attacker.randomMap]:
            #pygame.draw.rect(screen, GREEN, platform)
            if platform.width == 200 :
                screen.blit(gr_200_50, (platform.x, platform.y))
            elif platform.width == 300 :
                screen.blit(gr_300_50, (platform.x, platform.y))
            elif platform.width == SCREEN_WIDTH :
                screen.blit(gr_200_50_forGround, (0, 550))
                screen.blit(gr_200_50_forGround, (200, 550))
                screen.blit(gr_200_50_forGround, (400, 550))
                screen.blit(gr_200_50_forGround, (600, 550))

        # 캐릭터 그리기
        await player.Draw()
 
        
        await enemyContainer.Draw()
        # 어택 노드 그리기
        await attacker.Draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# asyncio 루프 실행
asyncio.run(main())