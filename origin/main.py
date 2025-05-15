import random
import sys
import pygame

pygame.init()
size = width, height = 400, 600  # 初始化屏幕

speed: list[int] = [0, 0]  # 小球运动速度
speed1 = [0, 0]  # 挡板向上移动速度
speed2 = [0, 0]  # 挡板向下移动速度
speed3 = [0, 0]  # 障碍物0移动速度
speed4 = [0, 0]  # 障碍物1移动速度
speed5 = [0, 0]  # 障碍物2移动速度
speed6 = [0, 0]  # 障碍物3移动速度


speedx = [0, 0]  # 缓存各对象速度
speed1x = [0, 0]
speed2x = [0, 0]
speed3x = [0, 0]
speed4x = [0, 0]
speed5x = [0, 0]
speed6x = [0, 0]

active: int = 0  # 游戏运行参数 0：游戏第一次开始等待 1：游戏运行 2：游戏暂停 3：游戏结束重新开始等待
case = 0    # 缓冲参数初始化

WHITE = 255, 255, 255  # 字体颜色
m: int = 0  # 当前帧数
z =0

c = 0  # 初始化道具效果随机数
last = 0  # 上一次碰撞板子
gamemap = 1   # 游戏地图序号
speedmode = 1  # 速度模式
myfont = pygame.font.Font(None, 30)  # 设置字体以及大小
long_press = {'up': False, 'down': False}  # 实现连续移动
long_press2 = {'up': False, 'down': False}
bg = pygame.image.load("../resources/img/page/game.png")  # 设置背景图片

score1 = 0  # 设置初始得分
score2 = 0

mi = True
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)  # 全屏
a = screen.get_width()  # 获取屏幕宽度
b = screen.get_height()  # 获取屏幕高度
pygame.display.set_caption("双人弹球")  # 标题名
fps: int = 100  # 刷新速度
# 生成 surface对象以及rect对象
ball = pygame.image.load("../resources/img/component/ball/ball_0.png")    # 小球运动动图
ballrect = ball.get_rect()
ball1 = pygame.image.load("../resources/img/component/ball/ball_1.png")
ball2 = pygame.image.load("../resources/img/component/ball/ball_2.png")
ball3 = pygame.image.load("../resources/img/component/ball/ball_3.png")
ball4= pygame.image.load("../resources/img/component/ball/ball_4.png")

win1 = pygame.image.load("../resources/img/component/win/player1_win.png")
win2 = pygame.image.load("../resources/img/component/win/player2_win.png")
start = pygame.image.load("../resources/img/page/start.png")
banzi1 = pygame.image.load("../resources/img/component/paddle/paddle.png")
banzi1rect = banzi1.get_rect()
banzi2 = pygame.image.load("../resources/img/component/paddle/paddle.png")
banzi2rect = banzi2.get_rect()
redball = pygame.image.load("../resources/img/component/red_prop/red_prop_1.png")
redballrect = redball.get_rect()

barrier = pygame.image.load("../resources/img/component/barrier/barrier_v.png")
barrierrect = barrier.get_rect()
barrier1 = pygame.image.load("../resources/img/component/barrier/barrier_v.png")
barrier1rect = barrier1.get_rect()
barrier2 = pygame.image.load("../resources/img/component/barrier/barrier_h.png")
barrier2rect = barrier2.get_rect()
barrier3 = pygame.image.load("../resources/img/component/barrier/barrier_h.png")
barrier3rect = barrier3.get_rect()

jiantouleft = pygame.image.load("../resources/img/component/tip/left.png")
jiantouright = pygame.image.load("../resources/img/component/tip/right.png")
xuanzhong = pygame.image.load("../resources/img/component/tip/selected.png")
map1 = pygame.image.load("../resources/img/component/map/map1.png")
map2 = pygame.image.load("../resources/img/component/map/map2.png")
map3= pygame.image.load("../resources/img/component/map/map3.png")


banzi2rect = banzi2rect.move(a - 8, 500)  # 确认各对象初始位置
banzi1rect = banzi1rect.move(0, 500)
redballrect = redballrect.move(100, 100)
ballrect = ballrect.move(a / 2, 10)
fclock = pygame.time.Clock()  # 计时

pygame.mixer.init()  # 初始化音频文件

music = pygame.mixer.music.load("../resources/audio/bgm/main_bgm_1.mp3")      # 加载音乐文件
pygame.mixer.music.set_volume(0.01)  # 控制背景音乐声音大小
pygame.mixer.music.play()  # 开始播放音乐流
bang = pygame.mixer.Sound("../resources/audio/sound_effect/hit.wav")
pop = pygame.mixer.Sound("../resources/audio/sound_effect/pop.wav")
shao = pygame.mixer.Sound("../resources/audio/sound_effect/whistle.wav")
huanhu = pygame.mixer.Sound("../resources/audio/sound_effect/cheer.wav")
anjian = pygame.mixer.Sound("../resources/audio/sound_effect/click.wav")

while True:
    if pygame.mixer.music.get_busy() == False:  # 检查是否正在播放音乐
        pygame.mixer.music.play()  # 开始播放音乐流
    for i in pygame.event.get():
        if i.type == pygame.QUIT:    # 退出
            sys.exit()

        elif i.type == pygame.KEYDOWN:  # 挡板连续移动
            if i.key == pygame.K_UP:
                long_press['up'] = True
            if i.key == pygame.K_DOWN:
                long_press['down'] = True
            if i.key == pygame.K_w:
                long_press2['up'] = True
            if i.key == pygame.K_s:
                long_press2['down'] = True

            if i.key == pygame.K_h:   # 选择速度模式
                if active == 0:
                    speedmode = 3
                    anjian.play()
            if i.key == pygame.K_m:
                if active == 0:
                    speedmode = 2
                    anjian.play()
            if i.key == pygame.K_l:
                if active == 0:
                    speedmode = 1
                    anjian.play()

            if i.key == pygame.K_RETURN:  # 按下回车开始游戏
                if active != 1:
                    anjian.play()
                if active == 0:
                    if speedmode == 1:
                        speed = [1, 1]  # 小球运动速度
                        speed1 = [0, -2]  # 挡板向上移动速度
                        speed2 = [0, 2]  # 挡板向下移动速度
                        speed3 = [0, 2]  # 障碍物0移动速度
                        speed4 = [0, -2]  # 障碍物1移动速度
                        speed5 = [2, 0]   # 障碍物2移动速度
                        speed6 = [-2, 0]  # 障碍物3移动速度
                    elif speedmode == 2:
                        speed = [2, 2]  # 小球运动速度
                        speed1 = [0, -3]  # 挡板向上移动速度
                        speed2 = [0, 3]  # 挡板向下移动速度
                        speed3 = [0, 3]  # 障碍物0移动速度
                        speed4 = [0, -3]  # 障碍物1移动速度
                        speed5 = [3, 0]  # 障碍物2移动速度
                        speed6 = [-3, 0]  # 障碍物3移动速度
                    elif speedmode == 3:
                        speed = [3, 3]  # 小球运动速度
                        speed1 = [0, -4]  # 挡板向上移动速度
                        speed2 = [0, 4]  # 挡板向下移动速度
                        speed3 = [0, 4]  # 障碍物0移动速度
                        speed4 = [0, -4]  # 障碍物1移动速度
                        speed5 = [4, 0]  # 障碍物2移动速度
                        speed6 = [-4, 0]  # 障碍物3移动速度
                    active = 1      # 进入游戏运行状态
                elif active == 3:
                    score1 = 0
                    score2 = 0
                    speed = [0, 0]
                    speed1 = [0, 0]
                    speed2 = [0, 0]
                    speed3 = [0, 0]
                    speed4 = [0, 0]
                    speed5 = [0, 0]
                    speed6 = [0, 0]
                    active = 0   # 游戏结束后回到开始界面

            if i.key == pygame.K_SPACE:    # 游戏运行时按下空格暂停，再次按下继续
                anjian.play()
                if active == 1:
                    speedx = speed.copy()
                    speed1x = speed1.copy()
                    speed2x = speed2.copy()
                    speed3x = speed3.copy()
                    speed4x = speed4.copy()
                    speed5x = speed5.copy()
                    speed6x = speed6.copy()
                    speed = [0, 0]
                    speed1 = [0, 0]
                    speed2 = [0, 0]
                    speed3 = [0, 0]
                    speed4 = [0, 0]
                    speed5 = [0, 0]
                    speed6 = [0, 0]
                    active = 2
                elif active == 2:
                    speed = speedx.copy()
                    speed1 = speed1x.copy()
                    speed2 = speed2x.copy()
                    speed3 = speed3x.copy()
                    speed4 = speed4x.copy()
                    speed5 = speed5x.copy()
                    speed6 = speed6x.copy()
                    active = 1

            if i.key == pygame.K_1 or i.key == pygame.K_KP1:  # 选择地图
                if active == 0:
                    anjian.play()
                    gamemap = 1
            if i.key == pygame.K_2 or i.key == pygame.K_KP2:
                if active == 0:
                    anjian.play()
                    gamemap = 2
            if i.key == pygame.K_3 or i.key == pygame.K_KP3:
                if active == 0:
                    anjian.play()
                    gamemap = 3

            elif i.key == pygame.K_ESCAPE:
                sys.exit()
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_UP:
                long_press['up'] = False
            if i.key == pygame.K_DOWN:
                long_press['down'] = False
            if i.key == pygame.K_w:
                long_press2['up'] = False
            if i.key == pygame.K_s:
                long_press2['down'] = False

    if long_press['up']:
        banzi2rect = banzi2rect.move(speed1)
    if long_press['down']:
        banzi2rect = banzi2rect.move(speed2)
    if long_press2['up']:
        banzi1rect = banzi1rect.move(speed1)
    if long_press2['down']:
        banzi1rect = banzi1rect.move(speed2)

    if banzi1rect.top < 0:   # 限制挡板高度
        banzi1rect.top = 0
    if banzi1rect.bottom > height:
        banzi1rect.bottom = height
    if banzi2rect.top < 0:
        banzi2rect.top = 0
    if banzi2rect.bottom > height:
        banzi2rect.bottom = height

    if active == 0:      # 初始化地图
        if gamemap == 1:       # 地图1
            barrierrect.x = a / 2 - 100
            barrierrect.y = b / 2
            barrier1rect.x = a / 2 + 100
            barrier1rect.y = b / 2
        if gamemap == 2:       # 地图2
            barrier2rect.x = 200
            barrier2rect.y = 200
            barrier3rect.x = 550
            barrier3rect.y = 400
        if gamemap == 3:
            barrierrect.x = a / 2 - 100
            barrierrect.y = b / 2
            barrier1rect.x = a / 2 + 100
            barrier1rect.y = b / 2
            barrier2rect.x = 200
            barrier2rect.y = 200
            barrier3rect.x = 550
            barrier3rect.y = 400

    if active == 1:    # 设置不同地图障碍物运行规律以及球与障碍物碰撞效果
        if gamemap == 1:
            barrierrect = barrierrect.move(speed3)  # 障碍物上下移动
            barrier1rect = barrier1rect.move(speed4)
            if barrierrect.top < 0 or barrierrect.bottom > b:
                speed3[1] = -speed3[1]
            if barrier1rect.top < 0 or barrier1rect.bottom > b:
                speed4[1] = -speed4[1]
            f = ballrect.colliderect(barrierrect)
            v = ballrect.colliderect(barrier1rect)
            if f:
                if speed[0] > 0:
                    ballrect.right = barrierrect.left
                    bang.play()
                    speed[0] = - speed[0]
                elif speed[0] < 0:
                    ballrect.left = barrierrect.right
                    bang.play()
                    speed[0] = - speed[0]
            if v:
                if speed[0] > 0:
                    ballrect.right = barrier1rect.left
                    bang.play()
                    speed[0] = - speed[0]
                elif speed[0] < 0:
                    ballrect.left = barrier1rect.right
                    bang.play()
                    speed[0] = - speed[0]



        if gamemap == 2:
            barrier2rect = barrier2rect.move(speed5)  # 障碍物左右移动
            barrier3rect = barrier3rect.move(speed6)
            if barrier2rect.left < 200 or barrier2rect.right > 600:
                speed5[0] = -speed5[0]
            if barrier3rect.left < 200 or barrier3rect.right > 600:
                speed6[0] = -speed6[0]
            f1 = ballrect.colliderect(barrier2rect)
            v1 = ballrect.colliderect(barrier3rect)
            if f1:
                if speed[1] > 0:
                    ballrect.bottom = barrier2rect.top
                    bang.play()
                    speed[1] = - speed[1]
                elif speed[1] < 0:
                    ballrect.top = barrier2rect.bottom
                    bang.play()
                    speed[1] = - speed[1]
            if v1:
                if speed[1] > 0:
                    ballrect.bottom = barrier3rect.top
                    bang.play()
                    speed[1] = - speed[1]
                elif speed[1] < 0:
                    ballrect.top = barrier3rect.bottom
                    bang.play()
                    speed[1] = - speed[1]

        if gamemap == 3:
            barrierrect = barrierrect.move(speed3)  # 障碍物上下移动
            barrier1rect = barrier1rect.move(speed4)
            barrier2rect = barrier2rect.move(speed5)  # 障碍物左右移动
            barrier3rect = barrier3rect.move(speed6)
            if barrierrect.top < 0 or barrierrect.bottom > b:
                speed3[1] = -speed3[1]
            if barrier1rect.top < 0 or barrier1rect.bottom > b:
                speed4[1] = -speed4[1]
            if barrier2rect.left < 200 or barrier2rect.right > 600:
                speed5[0] = -speed5[0]
            if barrier3rect.left < 200 or barrier3rect.right > 600:
                speed6[0] = -speed6[0]
            f = ballrect.colliderect(barrierrect)
            v = ballrect.colliderect(barrier1rect)
            f1 = ballrect.colliderect(barrier2rect)
            v1 = ballrect.colliderect(barrier3rect)
            if f:
                if speed[0] > 0:
                    ballrect.right = barrierrect.left
                    bang.play()
                    speed[0] = - speed[0]
                elif speed[0] < 0:
                    ballrect.left = barrierrect.right
                    bang.play()
                    speed[0] = - speed[0]
            if v:
                if speed[0] > 0:
                    ballrect.right = barrier1rect.left
                    bang.play()
                    speed[0] = - speed[0]
                elif speed[0] < 0:
                    ballrect.left = barrier1rect.right
                    bang.play()
                    speed[0] = - speed[0]
            if f1:
                if speed[1]>0:
                    ballrect.bottom=barrier2rect.top
                    bang.play()
                    speed[1] = - speed[1]
                elif speed[1]<0:
                    ballrect.top = barrier2rect.bottom
                    bang.play()
                    speed[1] = - speed[1]
            if v1:
                if speed[1] > 0:
                    ballrect.bottom = barrier3rect.top
                    bang.play()
                    speed[1] = - speed[1]
                elif speed[1] < 0:
                    ballrect.top = barrier3rect.bottom
                    bang.play()
                    speed[1] = - speed[1]

    screen.blit(bg, (0, 0))   # 绘制背景
    if active == 0:             # 绘制开始界面
        screen.blit(start, (0, 0))

        if speedmode == 1:         # 绘制选中速度效果
            screen.blit(xuanzhong, (52, 335))
        elif speedmode == 2:
            screen.blit(xuanzhong, (201, 335))
        elif speedmode == 3:
            screen.blit(xuanzhong, (346, 335))

        if gamemap == 1:         # 绘制选中地图效果
            screen.blit(xuanzhong, (49, 459))
            screen.blit(map1, (475, 316))
        elif gamemap == 2:
            screen.blit(xuanzhong, (201, 459))
            screen.blit(map2, (475, 316))
        elif gamemap == 3:
            screen.blit(xuanzhong, (346, 459))
            screen.blit(map3, (475, 316))

    if ballrect.right < 0:  # 小球得分判定
        score2 = score2 + 1
    if ballrect.left > a:
        score1 = score1 + 1
    wenzi1 = str(score1)
    wenzi2 = str(score2)
    textImage1 = myfont.render("playerA:" + wenzi1, True, WHITE)
    textImage2 = myfont.render("playerB:" + wenzi2, True, WHITE)

    m = m + 1  # 记录帧数

    if ballrect.right < 0 or ballrect.left > a:  # 小球出界后重新发球

        ballrect.top = 10
        ballrect.left = a / 2+10
        last = 0
        speed = [0, 0]
        z = random.randint(1, 2)
        if active != 3:
            shao.play()
        case = 1
    if m % 400 != 0 and case == 1:  # 预告小球发球方向
        if z == 1:
            screen.blit(jiantouright, (450, 300))
        if z == 2:
            screen.blit(jiantouleft, (310, 300))
    if m % 400 == 0 and case == 1:  # 小球出界后缓冲后并以随机速度及方向发出
        case = 0
        bang.play()
        if z == 1:
            if speedmode == 1:
                speed[0] = random.randint(1, 2)
                speed[1] = random.randint(1, 2)
            elif speedmode == 2:
                speed[0] = random.randint(2, 3)
                speed[1] = random.randint(2, 3)
            elif speedmode == 3:
                speed[0] = random.randint(3, 4)
                speed[1] = random.randint(3, 4)

        elif z == 2:
            if speedmode == 1:
                speed[0] = random.randint(-2, -1)
                speed[1] = random.randint(1, 2)
            elif speedmode == 2:
                speed[0] = random.randint(-3, -2)
                speed[1] = random.randint(2, 3)
            elif speedmode == 3:
                speed[0] = random.randint(-4, -3)
                speed[1] = random.randint(3, 4)

    ballrect = ballrect.move(speed)  # 小球运动
    if ballrect.top < 0 or ballrect.bottom > height:  # 小球上下运动反弹
        speed[1] = - speed[1]
        bang.play()

    # 球与两边挡板撞击效果
    t = ballrect.colliderect(banzi1rect)
    k = ballrect.colliderect(banzi2rect)
    if t:
        ballrect.left = banzi1rect.right
        speed[0] = - speed[0]
        last = 1
        bang.play()

    if k:
        ballrect.right = banzi2rect.left
        speed[0] = - speed[0]
        last = 2
        bang.play()

    f = ballrect.colliderect(redballrect)  # 红色小球被吃掉效果
    if f == True:
        mi = False
        pop.play()
    if mi == False:
        redballrect.left = 2 * a
        redballrect.top = 2 * b  # 小球被吃掉后移出屏幕产生消失效果
        c = random.randint(1, 2)  # 生成随机数c,产生相应效果

    if c == 1:  # 道具效果1：让球上一次碰撞挡板一方加分
        if last == 1:
            score1 = score1 + 5
        if last == 2:
            score2 = score2 + 5

    if c == 2:   # 道具效果2：让球速度最大
        if speed[0] > 0:
            speed[0] = 4
        if speed[0] < 0:
            speed[0] = -4
        if speed[1] > 0:
            speed[1] = 4
        if speed[1] < 0:
            speed[1] = -4

    c = 0  # 重置道具效果

    if m % 2000 == 0:  # 小球位置随机
        x = random.randint(200, 300)
        y = random.randint(200, 300)
        redballrect.left = x
        redballrect.top = y

    if int(m / 1000) % 2 == 0 and active == 1:  # 红色小球周期性出现
        mi = True
        screen.blit(redball, redballrect)
    else:
        redballrect.left = 2 * a
        redballrect.top = 2 * b


    if active == 1 or active == 2:
        if m % 5 == 0:    # 实现小球滚动
            screen.blit(ball, ballrect)
        elif m % 5 == 1:
            screen.blit(ball1, ballrect)
        elif m % 5 == 2:
            screen.blit(ball2, ballrect)
        elif m % 5== 3:
            screen.blit(ball3, ballrect)
        elif m % 5 == 4:
            screen.blit(ball4, ballrect)
        if gamemap == 1:
            screen.blit(barrier, barrierrect)
            screen.blit(barrier1, barrier1rect)
        if gamemap == 2:
            screen.blit(barrier2, barrier2rect)
            screen.blit(barrier3, barrier3rect)
        if gamemap == 3:
            screen.blit(barrier, barrierrect)
            screen.blit(barrier1, barrier1rect)
            screen.blit(barrier2, barrier2rect)
            screen.blit(barrier3, barrier3rect)

        screen.blit(banzi1, banzi1rect)
        screen.blit(banzi2, banzi2rect)
        screen.blit(textImage1, (100, 100))  # 显示字体，确定出现位置
        screen.blit(textImage2, (a - 200, 100))

    if score1 >= 5:  # 游戏结束判定 绘制结束图像
        screen.blit(win1,(300,200))
        active = 3
    if score2 >= 5:
        screen.blit(win2, (300, 200))
        active = 3
    if active == 3:   # 一方获胜暂停游戏
        speed = [0, 0]
        speed1 = [0, 0]
        speed2 = [0, 0]
        speed3 = [0, 0]
        speed4 = [0, 0]
    pygame.display.update()
    fclock.tick(fps)