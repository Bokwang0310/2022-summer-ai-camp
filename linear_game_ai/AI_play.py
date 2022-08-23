import numpy as np
import pygame
import random
from datetime import datetime
from keras.models import load_model

quit = 0

while(quit == 0):
    # 1. 게임 초기화
    pygame.init()

    data = [0, 0, 0]

    model = load_model('dino.h5')

    # 2. 게임창 옵션 설정
    size = [300, 600]
    screen = pygame.display.set_mode(size)

    title = "shoot Game"
    pygame.display.set_caption(title)

    # 3. 게임 내 필요한 설정
    clock = pygame.time.Clock()

    class obj:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.move = 0

        def put_img(self, address):
            if address[-3:] == "png":
                self.img = pygame.image.load(address).convert_alpha()
            else:
                self.img = pygame.image.load(address)
            self.sx, self.sy = self.img.get_size()

        def change_size(self, sx, sy):
            self.img = pygame.transform.scale(self.img, (sx, sy))
            self.sx, self.sy = self.img.get_size()

        def show(self):
            screen.blit(self.img, (self.x, self.y))

    def crash(a, b):
        if (a.x-b.sx <= b.x) and (b.x <= a.x+a.sx):
            if (a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
                return True
            else:
                return False
        else:
            return False

    ss = obj()
    ss.put_img("./resource/dealrocket.png")
    ss.change_size(50, 80)
    ss.x = round(size[0]/2 - ss.sx/2)
    ss.y = size[1] - ss.sy - 15
    ss.move = 5

    left_go = False
    right_go = False
    space_go = False

    m_list = []
    a_list = []

    black = (0, 0, 0)
    white = (255, 255, 255)

    GO = 0
    kill = 0
    loss = 0
    score = 0

    # 4-0. 게임 시작 대기 화면
    SB = 0
    while SB == 0:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SB = 1
        screen.fill(black)
        font = pygame.font.Font("./resource/BMJUA_ttf.ttf", 15)
        text = font.render(
            "PRESS SPACE KEY TO START THE GAME", True, (255, 255, 255))
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
        pygame.display.flip()

    # 4. 메인 이벤트
    start_time = datetime.now()
    SB = 0
    while SB == 0:

        # 4-1. FPS 설정
        clock.tick(60)

        left_down_event = pygame.event.Event(pygame.KEYDOWN, {
            'unicode': '', 'key': 1073741904, 'mod': 0, 'scancode': 80, 'window': None})
        right_down_event = pygame.event.Event(pygame.KEYDOWN, {
            'unicode': '', 'key': 1073741903, 'mod': 0, 'scancode': 79, 'window': None})
        left_up_event = pygame.event.Event(pygame.KEYUP, {
            'unicode': '', 'key': 1073741904, 'mod': 0, 'scancode': 80, 'window': None})
        right_up_event = pygame.event.Event(pygame.KEYUP, {
            'unicode': '', 'key': 1073741903, 'mod': 0, 'scancode': 79, 'window': None})

        result = model.predict(np.expand_dims(data, axis=0))

        print(result)

        # result[0][0], result[0][1] = result[0][1], result[0][0]

        try:
            pygame.event.post(left_up_event)
            pygame.event.post(right_up_event)
            if result[0][0] > result[0][1]:
                pygame.event.post(left_down_event)
                # pygame.event.post(left_up_event)
            else:
                pygame.event.post(right_down_event)
                # pygame.event.post(right_up_event)
        except:
            pass

        # 4-2. 각종 입력 감지
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SB = 1
                quit = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_go = True
                elif event.key == pygame.K_RIGHT:
                    right_go = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_go = False
                elif event.key == pygame.K_RIGHT:
                    right_go = False

        # 4-3. 입력, 시간에 따른 변화
        now_time = datetime.now()
        delta_time = round((now_time - start_time).total_seconds())

        if left_go == True:
            ss.x -= ss.move
            if ss.x <= 0:
                ss.x = 0
        elif right_go == True:
            ss.x += ss.move
            if ss.x >= size[0] - ss.sx:
                ss.x = size[0] - ss.sx

        if random.random() > 0.98:
            aa = obj()
            aa.put_img("./resource/coin.png")
            aa.change_size(40, 40)
            aa.x = random.randrange(0, size[0]-aa.sx-round(ss.sx/2))
            aa.y = 10
            aa.move = 5
            a_list.append(aa)

        d_list = []
        for i in range(len(a_list)):
            a = a_list[i]
            a.y += a.move
            if a.y >= size[1]:
                d_list.append(i)
        d_list.reverse()
        for d in d_list:
            del a_list[d]
            loss += 1

        dd_list = []
        for i in range(len(a_list)):
            a = a_list[i]
            if crash(a, ss) == True:
                dd_list.append(i)
        dd_list.reverse()
        for dd in dd_list:
            del a_list[dd]
            score += 1

        try:
            real_a = a_list[0]
            data[0] = real_a.x
            data[1] = real_a.y
            data[1] = ss.x
        except:
            data[0] = 0
            data[1] = 0
            data[2] = 0

        # 4-4. 그리기
        screen.fill(black)
        ss.show()
        for a in a_list:
            a.show()

        font = pygame.font.Font("./resource/BMJUA_ttf.ttf", 20)
        text_kill = font.render("score : {} loss : {}".format(
            score, loss), True, (255, 255, 0))
        screen.blit(text_kill, (10, 5))

        text_time = font.render("time : {}".format(
            delta_time), True, (255, 255, 255))
        screen.blit(text_time, (size[0]-100, 5))

        # 4-5. 업데이트
        pygame.display.flip()

    # 5. 게임 종료
    if GO == 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GO = 0
        font = pygame.font.Font("./resource/BMJUA_ttf.ttf", 40)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
        pygame.display.flip()

    pygame.quit()
