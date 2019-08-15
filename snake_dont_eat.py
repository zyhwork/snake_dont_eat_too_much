

import random
import sys
import time

import pygame
from pygame.locals import *
from START import START
from CHOICE import CHOICE


FPS = 10 # 屏幕刷新率（在这里相当于贪吃蛇的速度）
WINDOWWIDTH = 640 # 屏幕宽度
WINDOWHEIGHT = 480 # 屏幕高度
CELLSIZE = 10 # 小方格的大小
flag=0
# 断言，屏幕的宽和高必须能被方块大小整除
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

# 横向和纵向的方格数
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)


# 定义几个常用的颜色
# R G B
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BULE =(0,0,255)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
BGCOLOR = BLACK

# 定义贪吃蛇的动作
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# 贪吃蛇的头（）
HEAD = 0 # syntactic sugar: index of the worm's head
apple_list=[]


def main():
    # 定义全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init() # 初始化pygame
    FPSCLOCK = pygame.time.Clock() # 获得pygame时钟
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # 设置屏幕宽高
    pygame.display.set_caption("snake_dont_eat_too_much")
    BASICFONT = pygame.font.SysFont("arial", 18) # BASICFONT

    start_interface = START(WINDOWWIDTH, WINDOWHEIGHT)
    start_interface.update(DISPLAYSURF)
    showStartScreen() # 显示开始画面
    
    pygame.mixer.music.load('./resource/audios/bgm.mp3')
    pygame.mixer.music.play(-1, 0.0)
    while True: 
        choice_interface = CHOICE(WINDOWWIDTH, WINDOWHEIGHT)
        difficulty_type=choice_interface.update(DISPLAYSURF)
        time_start=time.time()
        global flag
        flag=0
        global apple_list
        apple_list=[]
        # 这里一直循环于开始游戏和显示游戏结束画面之间，
        # 运行游戏里有一个循环，显示游戏结束画面也有一个循环
        # 两个循环都有相应的return，这样就可以达到切换这两个模块的效果
        #start()
        runGame(time_start,difficulty_type) # 运行游戏
        
        showGameOverScreen() # 显示游戏结束画面
        
        
def runGame(time_start,difficulty_type):
    # 随机初始化设置一个点作为贪吃蛇的起点
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    flag_move=1
    # 以这个点为起点，建立一个长度为3格的贪吃蛇（数组）
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty},
                  {'x': startx - 3, 'y': starty}]


    direction = RIGHT # 初始化一个运动的方向

    # 随机一个apple的位置
    apple_list.append(getRandomLocation())
    food=getRandomLocation()
    time_1=time.time()
    flag_eat=0
    while True: # 游戏主循环
        i=0
        for event in pygame.event.get(): # 事件处理
            if event.type == QUIT: # 退出事件
                terminate()
            elif event.type == KEYDOWN: # 按键事件

                #如果按下的是左键或a键，且当前的方向不是向右，就改变方向，以此类推
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                    i=1
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                    i=1
                  
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                    i=1
                
                   
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                    i=1
                  
                    #newHead = {'x': wormCoords[HEAD]['x'] , 'y': wormCoords[HEAD]['y']+ 1}
                    #wormCoords.append (newHead)
                elif event.key == K_ESCAPE:
                    terminate()


        # 检查贪吃蛇是否撞到撞到边界
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
          
            return # game over
        
        # 检查贪吃蛇是否撞到自己
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
            
                return # game over


        for index in range(len(apple_list)):

            if wormCoords[HEAD]['x'] == apple_list[index]['x'] and wormCoords[HEAD]['y'] == apple_list[index]['y']:
                global flag 
                flag+=1
                del apple_list[index]
                flag_eat=1
                time_1=time.time()
                # 不移除蛇的最后一个尾巴格
                apple_list.append ( getRandomLocation()) # 重新随机生成一个apple
                apple_list.append(getRandomLocation())
                i=1
            else:
                i=1
                flag_move+=1 
        if i==0 or (flag_move % difficulty_type)==0:
            del wormCoords[-1] 
        
        #检查是否撑死
        if flag>2:
          
            return #game over

        #检测是否吃到消食片
        if wormCoords[HEAD]['x'] == food['x'] and wormCoords[HEAD]['y'] == food['y']:
            del wormCoords[-1] # 移除蛇的最后一个尾巴格
           
            flag-=1
            if(flag<0):
                flag=0

            #移除蛇的倒数第二个尾巴格
            # 移除蛇的最后一个尾巴格
            food = getRandomLocation() # 重新随机生成一个apple

        #检测是否饿死
        time_2=time.time()
        if flag_eat==0 and (time_2-time_1)>10:
         
            return
        flag_eat=0

       
            
        # 根据方向，添加一个新的蛇头，以这种方式来移动贪吃蛇
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
            
        # 插入新的蛇头在数组的最前面
        wormCoords.insert(0, newHead)
        
        # 绘制背景
        DISPLAYSURF.fill(BGCOLOR)
        

        
        # 绘制贪吃蛇
        drawWorm(wormCoords,direction)
        
        # 绘制apple
        drawApple(apple_list)

        #绘制food
        drawFood(food)
        
        # 绘制分数（分数为贪吃蛇存活时间）
        time_end=time.time()
        drawScore(round(time_end-time_start,1))
    
        #绘制血量
        drawLife(flag)

        #绘制饿死时间
        drawtime(round(time_2-time_1,1))
        # 更新屏幕
        pygame.display.update()
        
        # 设置帧率
        FPSCLOCK.tick(FPS)
      
# 绘制提示消息        
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True,GREEN)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)   
       

# 检查按键是否有按键事件
def checkForKeyPress():
   
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

# 显示开始画面
def showStartScreen():
    
    DISPLAYSURF.fill(BGCOLOR)
    
    titleFont = pygame.font.SysFont("arial", 100)
    
    titleSurf = titleFont.render('Wormy!', True, GREEN)
    
    titleRect = titleSurf.get_rect()
    titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    drawPressKeyMsg()
    
    pygame.display.update()
    
    while True:
        
        if checkForKeyPress():
            pygame.event.get() # clear event queue
           
            return
        

# 退出
def terminate():
    pygame.quit()
    sys.exit()

# 随机生成一个坐标位置    
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

# 显示游戏结束画面
def showGameOverScreen():
    gameOverFont = pygame.font.SysFont("arial", 50)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2-gameRect.height-10)
    overRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        
# 绘制分数        
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

#绘制血量
def drawLife(flag):
    lifeSurf = BASICFONT.render('LIFE: %s' % (flag), True, WHITE)
    lifeRect = lifeSurf.get_rect()
    lifeRect.topleft = (120, 10)
    DISPLAYSURF.blit(lifeSurf, lifeRect)


#绘制时间
def drawtime(time):
    timeSurf = BASICFONT.render('TIME: %s' % (time), True, WHITE)
    timeRect = timeSurf.get_rect()
    timeRect.topleft = (240, 10)
    DISPLAYSURF.blit(timeSurf, timeRect)
# 根据 wormCoords 数组绘制贪吃蛇
def drawWorm(wormCoords,direction):
    x = wormCoords[0]['x'] * CELLSIZE
    y = wormCoords[0]['y'] * CELLSIZE
    wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    if direction== UP:
        image=pygame.image.load('./resource/imgs/head_up.png')
    elif direction == RIGHT:
        image=pygame.image.load('./resource/imgs/head_right.png')
    elif direction == DOWN:
        image=pygame.image.load('./resource/imgs/head_down.png')
    elif direction == LEFT:
        image=pygame.image.load('./resource/imgs/head_left.png')
    image1=pygame.transform.scale(image,(15,15))
    DISPLAYSURF.blit(image1,(x-3,y-3))
    


    for coord in wormCoords[1:]:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        image=pygame.image.load('./resource/imgs/body.png')
        image1=pygame.transform.scale(image,(10,10))
        DISPLAYSURF.blit(image1,(x,y))


# 根据 coord 绘制 apple 
def drawApple(coord):
    for index in range(len(apple_list)):
        x = coord[index]['x'] * CELLSIZE
        y = coord[index]['y'] * CELLSIZE
        appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, RED, appleRect)

        image=pygame.image.load('./resource/imgs/apple.png')
        image1=pygame.transform.scale(image,(15,15))
        DISPLAYSURF.blit(image1,(x-3,y-3))
def drawFood(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    foodRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    image=pygame.image.load('./resource/imgs/food.png')
    image1=pygame.transform.scale(image,(15,15))
    DISPLAYSURF.blit(image1,(x-3,y-3))
    

if __name__ == '__main__':
    main()