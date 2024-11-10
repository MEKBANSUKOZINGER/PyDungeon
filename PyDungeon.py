import pygame
import asyncio
import sys
import random

# 파이게임 초기화
pygame.init()


# General Settings
gravity = 2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("턴전")

BLACK = (0, 0, 0)
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

bgm = pygame.mixer.music.load("./Music/BGM/GreenHillZone.mp3")


jumpSFX = pygame.mixer.Sound("./Music/SFX/Jump.wav")
ringSFX = pygame.mixer.Sound("./Music/SFX/Ring.wav")
enemyHitSFX = pygame.mixer.Sound("./Music/SFX/EnemyHit.wav")
sonicHitSFX = pygame.mixer.Sound("./Music/SFX/SonicHit.wav")

class GameManager :
    def __init__(self) :
        self.galmuriFont_30 = pygame.font.Font("./Fonts/Galmuri9.ttf", 30)
        self.galmuriFont_10 = pygame.font.Font("./Fonts/Galmuri9.ttf", 10)
        self.score = 0
        self.prevPlayerHp = 100
        self.minusBlitting = False
        self.minusAlpha = 250
        self.minusPos = 60

        self.plusBlitting = False
        self.plusAlpha = 250
        self.plusPos = 60

    def RenderScore(self) :
        scoreText = self.galmuriFont_30.render(" Score : " +  str(self.score) + " ", False, BLACK)
        screen.blit(scoreText, (20, 20))

    def RenderInfo(self, attacker, player) :
        if not attacker.isLarge and not player.isDashing and not player.isJumping:
            infoText = self.galmuriFont_10.render(" Press A to input skills ", False, BLACK)
            screen.blit(infoText, (343, 43))
        elif (player.isDashing or player.isJumping) and attacker.isAttacking  : 
            infoText = self.galmuriFont_10.render(" ...Doing... ", False, BLACK)
            screen.blit(infoText, (373, 43))
        elif (player.isDashing or player.isJumping) and not attacker.isAttacking : 
            infoText = self.galmuriFont_10.render(" Done! ", False, BLACK)
            screen.blit(infoText, (388, 43))
        
        energyText = self.galmuriFont_30.render(" Energy : " + str(player.hp) + "% ", False, BLACK)
        screen.blit(energyText, (550, 20))
    
    def RenderMinusFX(self, player) :
        if self.minusBlitting :
            minusText = self.galmuriFont_10.render("-" + str(self.prevPlayerHp - player.hp), False, BLACK)
            if self.minusAlpha == 0 :
                self.minusBlitting = False
                self.prevPlayerHp = player.hp
            else :
                if self.minusAlpha == 250 :
                    sonicHitSFX.play()
                #print(self.minusPos)
                minusText.set_alpha(self.minusAlpha)
                screen.blit(minusText, (700, self.minusPos))
                self.minusPos += 1
                self.minusAlpha -= 10
        elif self.prevPlayerHp != player.hp:
            self.minusBlitting = True
            self.minusAlpha = 250
            self.minusPos = 60

    def RenderPlusFX(self) :
        if self.plusBlitting :
            plusText = self.galmuriFont_10.render("+1", False, BLACK)
            if self.plusAlpha == 0 :
                self.plusBlitting = False
            else :
                #print(self.plusPos)
                plusText.set_alpha(self.plusAlpha)
                screen.blit(plusText, (155, self.plusPos))
                self.plusPos += 1
                self.plusAlpha -= 10

    def ScorePlus(self) :
        ringSFX.play()
        self.plusBlitting = True
        self.plusAlpha = 250
        self.plusPos = 60
        self.score += 1


    def Update(self, attacker, player) :
        self.RenderScore()
        self.RenderInfo(attacker, player)
        self.RenderMinusFX(player)
        self.RenderPlusFX()


class Player :
    def __init__(self, player_posX, player_posY, player_size, player_velocity, hp) :
        self.hp = hp

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
        self.prevNode = "None"

        self.drawImg = playerIdleImg
        self.runIndex = 0

    async def Draw(self) :
        if self.runIndex == 4 :
            self.runIndex = 0
            
        screen.blit(self.drawImg[self.runIndex], (self.playerPos[0], self.playerPos[1]))
        self.runIndex += 1
        await asyncio.sleep(0)

    async def Update(self) :
        #print(self.hp)
        #print(self.isAttacking)
        #print(self.playerPos)
        # 중력 설정
        prevPos = self.playerPos[:]
        self.playerPos[1] += self.fallSpeed
        self.fallSpeed += gravity

        if self.fallSpeed > 4 :
            self.drawImg = playerJumpImages
        elif self.fallSpeed <= 4 and self.isDashing  : 
            self.drawImg = playerRunImages
        else :
            self.drawImg = playerIdleImages
    
        # 대쉬 업데이트
        if self.isDashing :
            #print("ImDashing")
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
            #print("ImJumping")
            if self.playerPos[1] <= 0 :
                self.jumpCount = 0
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount <= 0:
                    neg = -1
                    self.canCollide = True
                else :
                    self.canCollide = False
                self.playerPos[1] -= (self.jumpCount ** 2) * 0.4 * neg
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = 30
                
        if prevPos == self.playerPos :
            self.isAttacking = False
        else :
            self.isAttacking = True

        await asyncio.sleep(0)

    async def BoxCollider(self, _platforms) :
        # 바닥 상시 체크
        if self.playerPos[1] >= 550 :
            self.playerPos[1] = 550 - self.playerSize
            self.fallSpeed = 0
        
        # 플랫퐄 체크
        for platform in _platforms:
            if platform.colliderect(pygame.Rect(self.playerPos[0], self.playerPos[1], 10, self.playerSize)):
                # 캐릭터가 플랫폼 위에 있을 때
                #print(platform.y, self.playerPos[1])
                if self.canCollide and platform.y <= self.playerPos[1] + self.playerSize:
                    self.playerPos[1] = platform.top - self.playerSize
                    self.fallSpeed = 0
                    self.isJumping = False
                    #self.jumpCount = 30
            await asyncio.sleep(0)
        await asyncio.sleep(0)
    
    async def Attack(self, attackType) :
        if attackType == "Dash_E":
            if self.prevNode == "Jump" :
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
            self.prevNode = "Dash"
        elif attackType == "Jump" :
            jumpSFX.play()
            self.isJumping = True
            self.fallSpeed = 0
            self.jumpCount = 11
            self.canCollide = False
            self.prevNode = "Jump"
        elif attackType == "Dash_Q":
            if self.prevNode == "Jump" :
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
            self.prevNode = "Dash"

        await asyncio.sleep(0)

class EnemyContainer :
    def __init__(self) :
        self.container = []
        self.isCleared = True
        self.attacked = False

    async def Update(self, attacker, player, gameManager) :
        await self.checkClear(attacker, player, gameManager)
        for enemy in self.container :
            await enemy.Update()

    
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
    
    async def nextMap(self, attacker) :
        if self.isCleared :
            await self.generateEnemies()
            attacker.randomMapGenerate()
            self.isCleared = False
        await asyncio.sleep(0)

    async def checkClear(self, attacker, player, gameManager) :
        if self.attacked and not player.isAttacking :
            player.hp -= 2 * len(self.container)
            self.attacked = False
        elif len(self.container) == 0 and not attacker.isAttacking and not player.isAttacking :
            self.isCleared = True
            await asyncio.sleep(0)
        else :
            self.isCleared = False
            await asyncio.sleep(0)

        if player.isDashing or player.isJumping : 
            self.attacked = True

        for i in range(len(self.container)) :
            #print("Done")
            if i < len(self.container) and self.container[i].checkDie(player, gameManager) :
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
        screen.blit(enemyImages[self.enemyIndex], (self.enemyPos[0]-10, self.enemyPos[1]-15))
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

    def checkDie(self, player, gameManager) :
        if (abs(self.enemyPos[0] - player.playerPos[0]) <= 60) and (abs(self.enemyPos[1] - player.playerPos[1]) <= 60) :
            #print("Dead")
            enemyHitSFX.play()
            gameManager.ScorePlus()
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

    def randomMapGenerate(self) : 
        self.randomMap = random.randint(0,len(platformContainer) - 1)
        print(self.randomMap)

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
        await asyncio.sleep(0.25)
        #self.attackNodes.clear()
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
        pygame.Rect(100, 450, 200, 10),
        pygame.Rect(350, 350, 300, 10),
        pygame.Rect(530, 450, 200, 10),
        pygame.Rect(150, 60, 200, 10),
        pygame.Rect(250, 160, 200, 10),
        pygame.Rect(0, 260, 200, 10),
    ]
]

# 메인 루프

clock = pygame.time.Clock()

player = Player(100, 500, 60, 0.5, 100)

attacker = Attacker()

enemyContainer = EnemyContainer()

gameManager = GameManager()
async def main():
    titleLogo = pygame.image.load("./Images/UI/logo.png")
    titleLogo = pygame.transform.scale(titleLogo, (627, 398))

    titleBG = pygame.image.load("./Images/UI/titleBG.png")
    titleBG = pygame.transform.scale(titleBG, (800, 600))

    titleRun = True
    playTextAlpha = 255
    alphaType = "Decrease"
    while titleRun :
        screen.fill(WHITE)
        screen.blit(titleBG, (0, 0))
        screen.blit(titleLogo, (85, 50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN :
                titleRun = False

        playFont = pygame.font.Font("./Fonts/Galmuri9.ttf", 50)
        playText = playFont.render("Press any key to start", False, BLACK)

        if playTextAlpha == 255 : 
            alphaType = "Decrease"
        elif playTextAlpha == 0 :
            alphaType = "Increase"
        
        if alphaType == "Decrease" : 
            playTextAlpha -= 1
        elif alphaType == "Increase" : 
            playTextAlpha += 1
        playText.set_alpha(playTextAlpha)

        screen.blit(playText, (115, 450))
        pygame.display.flip()
        
    while True:


        running = True
        attack_task = None  # 공격 태스크 초기화

        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        while running:
            tick = clock.tick(360)
            pygame.time.delay(25)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #print("ESC?")
                    pygame.quit()
                    sys.exit()
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
                            # 새로운 공격 태스크를 실행\
                            #print("erer")
                            if (attack_task is None or attack_task.done()) and (not player.isDashing and not player.isJumping and not attacker.isAttacking):
                                attack_task = asyncio.create_task(attacker.AttackCoroutine(player))
                        if event.key == pygame.K_BACKSPACE:
                            await attacker.DeleteAttackNode()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                running = False

            # 중력 적용
            await enemyContainer.nextMap(attacker)

            await enemyContainer.Update(attacker, player, gameManager)

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
            #print(attacker.randomMap)
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

            await attacker.Draw()
            # 어택 노드 그리기

            gameManager.Update(attacker, player)

            pygame.display.flip()

        pygame.mixer.music.pause()
        gameOverFont = pygame.font.Font("./Fonts/Galmuri9.ttf", 120)
        gameOverSubFont = pygame.font.Font("./Fonts/Galmuri9.ttf", 50)
        gameOverScoreFont = pygame.font.Font("./Fonts/Galmuri9.ttf", 40)

        gameOverBG = pygame.image.load("./Images/UI/gameOverBG.png")
        gameOverBG = pygame.transform.scale(gameOverBG, (800, 600))

        #print("eSC")
        gameOverRunning = True
        while gameOverRunning :
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print(event.key)
                    if event.key == pygame.K_q :
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE :
                        print("hi")
                        gameManager.score = 0
                        player.hp = 100
                        attacker.attackNodes.clear()
                        gameManager.prevPlayerHp = 100
                        enemyContainer.container.clear()
                        enemyContainer.isCleared = True
                        enemyContainer.nextMap(attacker)
                        gameOverRunning = False
                        #asyncio.run(main())

            screen.fill(WHITE)

            screen.blit(gameOverBG, (0, 0))

            gameOver = gameOverFont.render("Game Over", False, WHITE)
            screen.blit(gameOver, (90, 100))

            score = gameOverScoreFont.render("Your Score : " + str(gameManager.score), False, WHITE)
            screen.blit(score, (255, 260))

            gameOverSubRetry = gameOverSubFont.render("Press Space bar to retry", False, WHITE)
            screen.blit(gameOverSubRetry, (90, 350))

            gameOverSubQuit = gameOverSubFont.render("Press Q to quit", False, WHITE)
            screen.blit(gameOverSubQuit, (225, 420))
            #print("Done")
            pygame.display.flip()


# asyncio 루프 실행
asyncio.run(main())