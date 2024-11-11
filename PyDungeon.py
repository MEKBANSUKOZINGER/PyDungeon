'''
소프트웨어융합학과 2023105438 신동준
게임 프로그래밍 입문 Project #2
'''

import pygame
import asyncio
import sys
import random

# 파이게임 초기화
pygame.init()


# 중력 설정
gravity = 2

# 기본 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sonic The Hedgehog (해적판)")

# 색 선언
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#이미지 불러오기
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

# 사운드 불러오기
bgm = pygame.mixer.music.load("./Music/BGM/GreenHillZone.mp3")

jumpSFX = pygame.mixer.Sound("./Music/SFX/Jump.wav")
ringSFX = pygame.mixer.Sound("./Music/SFX/Ring.wav")
enemyHitSFX = pygame.mixer.Sound("./Music/SFX/EnemyHit.wav")
sonicHitSFX = pygame.mixer.Sound("./Music/SFX/SonicHit.wav")

# UI와 UI 애니메이션, 점수를 관리하는 게임매니저 클래스
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

    # 화면에 점수 출력
    def RenderScore(self) :
        scoreText = self.galmuriFont_30.render(" Score : " +  str(self.score) + " ", False, BLACK)
        screen.blit(scoreText, (20, 20))

    # 화면에 도움말 출력
    def RenderInfo(self, attacker, player) :
        '''
        상태에 따라 출력문구 변경
        - 기본 상태 (공격을 안하고 있는 상태) : "Press A to input skills"
        - 공격 상태 (공격 노드가 실행되고 있는 상태) : "...Doing..."
        - 소강 상태 (공격 노드가 모두 실행되었지만 플레이어가 멈추지 않았을 떄 : "Done!"
        '''
        if not attacker.isLarge and not player.isDashing and not player.isJumping:
            infoText = self.galmuriFont_10.render(" Press A to input skills ", False, BLACK)
            screen.blit(infoText, (343, 43))
        elif (player.isDashing or player.isJumping) and attacker.isAttacking  : 
            infoText = self.galmuriFont_10.render(" ...Doing... ", False, BLACK)
            screen.blit(infoText, (373, 43))
        elif (player.isDashing or player.isJumping) and not attacker.isAttacking : 
            infoText = self.galmuriFont_10.render(" Done! ", False, BLACK)
            screen.blit(infoText, (388, 43))
        
        # 플레이어 hp 출력
        energyText = self.galmuriFont_30.render(" Energy : " + str(player.hp) + "% ", False, BLACK)
        screen.blit(energyText, (550, 20))
    
    # 플레이어 hp가 깎이는 UI 애니메이션 - 서서히 내려가기, 페이드 아웃
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

    # 점수가 올라가는 UI 애니메이션 - 서서히 내려가기, 페이드 아웃
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

    # 점수 올라가는 함수
    def ScorePlus(self) :
        ringSFX.play()
        self.plusBlitting = True
        self.plusAlpha = 250
        self.plusPos = 60
        self.score += 1

    # 상태 업데이트
    def Update(self, attacker, player) :
        self.RenderScore()
        self.RenderInfo(attacker, player)
        self.RenderMinusFX(player)
        self.RenderPlusFX()

# 직접 플레이 할 플레이어 클래스
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

    # 플레이어 애니메이션 - 게임 프레임당 다른 이미지 출력
    async def Draw(self) :
        if self.runIndex == 4 :
            self.runIndex = 0
            
        screen.blit(self.drawImg[self.runIndex], (self.playerPos[0], self.playerPos[1]))
        self.runIndex += 1
        await asyncio.sleep(0)

    # 상태 업데이트
    async def Update(self) :
        self.canCollide = True

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
            # self.dashDirection : -1 - 왼쪽 / 1 - 오른쪽
            # 벽에 부딪혔다면 이미지 반전
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
            # 천장 뚫기 방지
            if self.playerPos[1] <= 0 :
                self.jumpCount = -1
            
            # 점프 중이라면
            if self.jumpCount >= -10:
                neg = 1
                # 점프 완료 후 내려갈 때
                if self.jumpCount <= 0:
                    neg = -1
                    # 콜리전 활성화
                    self.canCollide = True
                else :
                    # 올라갈 때에는 콜리전 비활성화
                    self.canCollide = False
                self.playerPos[1] -= (self.jumpCount ** 2) * 0.4 * neg
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = 30
                
        # 움직이고 있는 경우 처리 (UI 상태를 위해)
        if prevPos == self.playerPos :
            self.isAttacking = False
        else :
            self.isAttacking = True

        await asyncio.sleep(0)

    # 충돌 제어
    async def BoxCollider(self, _platforms) :
        # 바닥 상시 체크
        if self.playerPos[1] >= 550 :
            self.playerPos[1] = 550 - self.playerSize
            self.fallSpeed = 0
        
        # 플랫폼 체크
        for platform in _platforms:
            # AABB 기술을 이용하여 충돌 감지
            if platform.colliderect(pygame.Rect(self.playerPos[0], self.playerPos[1], 10, self.playerSize)):
                # 캐릭터가 플랫폼 위에 있고, 콜리전이 켜져있을 때
                if self.canCollide and platform.y <= self.playerPos[1] + self.playerSize:
                    # 플랫폼 위로 플레이어 위치 고정
                    self.playerPos[1] = platform.top - self.playerSize
                    self.fallSpeed = 0
                    self.isJumping = False
                    #self.jumpCount = 30
            await asyncio.sleep(0)
        await asyncio.sleep(0)
    
    # 공격 함수
    async def Attack(self, attackType) :
        # 오른쪽 대쉬
        if attackType == "Dash_E":
            # 점프중이었다면, 오른쪽으로 플레이어 발사
            if self.prevNode == "Jump" :
                self.fallSpeed = 0
            self.isDashing = True

            # 왼쪽으로 이동중이었다면 이미지 반전
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
        
        # 점프
        elif attackType == "Jump" :
            jumpSFX.play()
            self.isJumping = True
            self.fallSpeed = 0
            self.jumpCount = 11
            self.canCollide = False
            self.prevNode = "Jump"

        # 왼쪽 대쉬
        elif attackType == "Dash_Q":
            # 점프중이었다면, 왼쪽으로 플레이어 발사
            if self.prevNode == "Jump" :
                self.fallSpeed = 0
            self.isDashing = True

            # 오른쪽으로 이동중이었다면 이미지 반전
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

# 적들을 관리하는 클래스
class EnemyContainer :
    def __init__(self) :
        self.container = []
        self.isCleared = True
        self.attacked = False

    async def Update(self, attacker, player, gameManager) : 
        # 한 웨이브 클리어 상시 감지
        await self.checkClear(attacker, player, gameManager)
        for enemy in self.container :
            await enemy.Update()

    
    async def Draw(self) :
        for enemy in self.container :
            await enemy.Draw()
            #print(enemy.enemyPos)

    # 적 생성 함수
    async def generateEnemies(self) :
        # 5명의 적을 생성해 컨테이너 리스트에 추가
        for _ in range(5) :
            enemy = Enemy()
            #print(enemy.enemyPos)
            self.container.append(enemy)
            await asyncio.sleep(0)
        await asyncio.sleep(0)
    
    # 다음 맵 불러오는 함수
    async def nextMap(self, attacker) :
        if self.isCleared :
            await self.generateEnemies()
            attacker.randomMapGenerate()
            self.isCleared = False
        await asyncio.sleep(0)

    # 클리어 감지 함수
    async def checkClear(self, attacker, player, gameManager) :
        # 모든 노드가 실행되었고, 플레이어도 멈췄는데 적이 남아있다면 (적들을 한 번에 죽이지 못했다면) 플레이어에게 (2 * 적의 수) 만큼 데미지
        if self.attacked and not player.isAttacking :
            player.hp -= 2 * len(self.container)
            self.attacked = False
        
        # 모든 적이 죽었다면 웨이브 클리어
        elif len(self.container) == 0 and not attacker.isAttacking and not player.isAttacking :
            self.isCleared = True
            await asyncio.sleep(0)
        else :
            self.isCleared = False
            await asyncio.sleep(0)

        if player.isDashing or player.isJumping : 
            self.attacked = True

        # 적이 죽었는지 상시 감지
        for i in range(len(self.container)) :
            # 죽었다면 리스트에서 제거
            if i < len(self.container) and self.container[i].checkDie(player, gameManager) :
                self.container.pop(i)
            await asyncio.sleep(0)
        await asyncio.sleep(0)

    # 적들 충돌 감지
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
        await asyncio.sleep(0)

    async def BoxCollider(self, _platforms) :
        # 바닥 상시 체크
        if self.enemyPos[1] >= 550 :
            self.enemyPos[1] = 550 - self.enemySize
            self.fallSpeed = 0
        
        # 플랫폼 체크
        for platform in _platforms:
            # AABB 기술을 활용하여 충돌 감지
            if platform.colliderect(pygame.Rect(self.enemyPos[0], self.enemyPos[1], self.enemySize, self.enemySize)):
                # 캐릭터가 플랫폼 위에 있을 때
                self.enemyPos[1] = platform.top - self.enemySize
                self.fallSpeed = 0
            await asyncio.sleep(0)
        await asyncio.sleep(0)

    # 죽었는지 확인
    def checkDie(self, player, gameManager) :
        # 플레이어와의 좌표 차이를 계산하여 60 이내라면 죽음
        if (abs(self.enemyPos[0] - player.playerPos[0]) <= 60) and (abs(self.enemyPos[1] - player.playerPos[1]) <= 60) :
            #print("Dead")
            enemyHitSFX.play()
            gameManager.ScorePlus()
            return True
        else :
            return False

# 공격 노드를 관리하고 실행하는 클래스
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

    # 랜덤한 맵의 인덱스를 설정
    def randomMapGenerate(self) : 
        self.randomMap = random.randint(0,len(platformContainer) - 1)

    # 커졌을 떄와 작아졌을 때의 크기를 다르게 하여 화면에 출력
    async def Draw(self) :
        screen.blit(self.image, ((SCREEN_WIDTH - self.width) // 2, self.posY))
        # 노드도 같이 크기 조정
        for i in range(len(self.attackNodes)) :
            if self.isLarge :
                await self.attackNodes[i].Draw((SCREEN_WIDTH - self.width) // 2 + 10 + 70 * (i), self.posY + 10, 60, 60)
            else :
                await self.attackNodes[i].Draw((SCREEN_WIDTH - self.width) // 2 + 5 + 25 * (i), self.posY + 5, 20, 20)
            await asyncio.sleep(0)
        await asyncio.sleep(0)


    # 활성화 / 비활성화 함수
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

    # 호출되면 리스트에 노드 추가
    async def AttackInput(self, _nodeType) :
        # 비활성화 상태면 아무 동작도 하지 않음
        if not self.isLarge :
            return
    
        # 노드는 최대 8개까지
        if len(self.attackNodes) == 8 :
            print("Full!")
            return
        self.attackNodes.append(Node(_nodeType))
        await asyncio.sleep(0)

    # 노드를 지우는 함수
    async def DeleteAttackNode(self) :
        if len(self.attackNodes) == 0 :
            return
        self.attackNodes.pop()
        await asyncio.sleep(0)

    # 노드를 토대로 플레이어에게 동작 명령을 내리는 함수
    async def AttackCoroutine(self, player) :
        # 노드가 8개 미만이라면 아무 동작도 하지 않음
        if len(self.attackNodes) < 8 :
            return
        currentIndex = 0
        currentTime = pygame.time.get_ticks()
        self.isAttacking = True

        # 비활성화 상태로 전환
        self.isLarge = True
        await attacker.EnableSelf()

        # 노드 리스트를 돌며 플레이어에게 텀을 두고 공격 명령
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

    # 노드 타입과 Attacker의 활성화 / 비활성화 여부에 맞춰 화면에 출력
    async def Draw(self, posX, posY, width, height) :
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



# 바닥 플랫폼
floor = pygame.Rect(0, 550, SCREEN_WIDTH, 50)

# 랜덤 플랫폼 리스트
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
        pygame.Rect(150, 80, 200, 10),
        pygame.Rect(250, 180, 200, 10),
        pygame.Rect(0, 260, 200, 10),
    ],
        [   
        pygame.Rect(0, 550, SCREEN_WIDTH, 50),
        pygame.Rect(100, 450, 200, 10),  # 공중 플랫폼
        pygame.Rect(150, 400, 300, 10),
        pygame.Rect(250, 100, 200, 10),
        pygame.Rect(200, 310, 300, 10),
        pygame.Rect(490, 200, 200, 10),
        pygame.Rect(100, 160, 300, 10),
    ], 
        [   
        pygame.Rect(0, 550, SCREEN_WIDTH, 50),
        pygame.Rect(400, 250, 300, 10),  # 공중 플랫폼
        pygame.Rect(100, 450, 200, 10),
        pygame.Rect(150, 350, 300, 10),
        pygame.Rect(330, 450, 200, 10),
        pygame.Rect(150, 100, 300, 10),
        pygame.Rect(450, 160, 200, 10),
        pygame.Rect(0, 260, 200, 10),
    ],
]

clock = pygame.time.Clock()

# 객체 생성
player = Player(100, 500, 60, 0.5, 100)
attacker = Attacker()
enemyContainer = EnemyContainer()
gameManager = GameManager()

# 메인 루프
async def main():

    # 타이틀 화면
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

        # 타이틀 화면의 Press any key ~ 문구 Breathing(숨쉬기) 애니메이션
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
        
    # 메인 플로우 루프
    while True:
        running = True
        attack_task = None  # 공격 태스크 초기화

        # BGM 재생
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # 게임 루프
        while running:
            tick = clock.tick(360)
            pygame.time.delay(25)

            # 입력 이벤트에 따라 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # 플레이어가 공격 실행중이 아니고 멈춰있다면
                    if not attacker.isAttacking and (not player.isDashing or not player.isJumping) :
                        # Attacker 활성화
                        if event.key == pygame.K_a:
                            await attacker.EnableSelf()
                        # 왼쪽 대쉬 노드 추가
                        if event.key == pygame.K_q:
                            await attacker.AttackInput("Dash_Q")
                        # 점프 노드 추가
                        if event.key == pygame.K_w:
                            await attacker.AttackInput("Jump")
                        # 오른쪽 대쉬 노드 추가
                        if event.key == pygame.K_e:
                            await attacker.AttackInput("Dash_E")
                        # 공격 수행 명령
                        if event.key == pygame.K_RETURN:
                            # 비동기로 공격 명령 제공
                            # 다른 공격 명령이 실행되고있지 않을 때
                            if (attack_task is None or attack_task.done()) and (not player.isDashing and not player.isJumping and not attacker.isAttacking):
                                attack_task = asyncio.create_task(attacker.AttackCoroutine(player))
                        # 노드 삭제
                        if event.key == pygame.K_BACKSPACE:
                            await attacker.DeleteAttackNode()

            keys = pygame.key.get_pressed()

            # 개발자 기능 : 강제 게임 오버
            if keys[pygame.K_ESCAPE]:
                running = False

            # 플레이어가 죽었다면 게임 오버
            if player.hp <= 0 :
                running = False

            # 업데이트 요소들 처리
            await enemyContainer.nextMap(attacker)

            await enemyContainer.Update(attacker, player, gameManager)

            await player.Update()

            await player.BoxCollider(platformContainer[attacker.randomMap])

            await enemyContainer.BoxCollider(platformContainer[attacker.randomMap])

            # 화면 업데이트
            screen.fill(WHITE)

            # 배경 이미지 출력
            screen.blit(backGround, (0, 0))

            # 플랫폼 그리기
            for platform in platformContainer[attacker.randomMap]:
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
    
            # 적 그리기
            await enemyContainer.Draw()

            # 공격 노드 그리기
            await attacker.Draw()

            # UI 상황 업데이트
            gameManager.Update(attacker, player)

            pygame.display.flip()
        
        # 게임 오버 상황
        # 음악 멈추기
        pygame.mixer.music.pause()

        # 폰트 선언
        gameOverFont = pygame.font.Font("./Fonts/Galmuri9.ttf", 120)
        gameOverSubFont = pygame.font.Font("./Fonts/Galmuri9.ttf", 50)
        gameOverScoreFont = pygame.font.Font("./Fonts/Galmuri9.ttf", 40)

        gameOverBG = pygame.image.load("./Images/UI/gameOverBG.png")
        gameOverBG = pygame.transform.scale(gameOverBG, (800, 600))

        # 게임 오버 루프
        gameOverRunning = True
        while gameOverRunning :
            # 입력 처리
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Q를 누르면 게임 나가기
                    if event.key == pygame.K_q :
                        pygame.quit()
                        sys.exit()
                    
                    # 스페이스 바를 누르면 게임 리셋 후 재시작
                    if event.key == pygame.K_SPACE :
                        gameManager.score = 0
                        player.hp = 100
                        attacker.attackNodes.clear()
                        gameManager.prevPlayerHp = 100
                        enemyContainer.container.clear()
                        enemyContainer.isCleared = True
                        enemyContainer.nextMap(attacker)
                        gameOverRunning = False

            screen.fill(WHITE)

            screen.blit(gameOverBG, (0, 0))

            # 텍스트 화면에 출력
            gameOver = gameOverFont.render("Game Over", False, WHITE)
            screen.blit(gameOver, (90, 100))

            score = gameOverScoreFont.render("Your Score : " + str(gameManager.score), False, WHITE)
            screen.blit(score, (255, 260))

            gameOverSubRetry = gameOverSubFont.render("Press Space bar to retry", False, WHITE)
            screen.blit(gameOverSubRetry, (90, 350))

            gameOverSubQuit = gameOverSubFont.render("Press Q to quit", False, WHITE)
            screen.blit(gameOverSubQuit, (225, 420))

            pygame.display.flip()


# 비동기로 메인 루프 실행
asyncio.run(main())