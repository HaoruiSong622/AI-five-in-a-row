from board import Board
from board import Zobrist
from board import AI
from game import Game
import config
import pygame
from pygame import MOUSEBUTTONUP
from pygame import MOUSEBUTTONDOWN
from pygame.locals import *
from sys import exit
import math


# if __name__ == '__main__':
#     g = Game()
#     while True:
#         x = int(input("please input the x position of the chessman: "))
#         y = int(input("please input the y position of the chessman: "))
#         g.set(x, y, config.hum)
#         temp = g.check()
#         if temp == 1:
#             print("computer wins!")
#             break
#         elif temp == 2:
#             print("human wins!")
#             break
#         comPoint = g.begin()
#         print("computer put the chessman on the position: ", comPoint.x, comPoint.y)
#         temp = g.check()
#         if temp == 1:
#             print("computer wins!")
#             break
#         elif temp == 2:
#             print("human wins!")
#             break
#         for i in g.board.allsteps:
#             print(i.x, i.y, i.role)
#
#         # print(g.board.board)

background_image_filename = 'asset/board.jpg'
black_image_filename = 'asset/black.png'
white_image_filename = 'asset/white.png'
aifirst_not_selected_image_filename = 'asset/aifirst-not-selected.png'
aifirst_selected_image_filename = 'asset/aifirst-selected.png'
youfirst_not_selected_image_filename = 'asset/youfirst-not-selected.png'
youfirst_selected_image_filename = 'asset/youfirst-selected.png'
easy_not_selected_image_filename = 'asset/easy-not-selected.png'
easy_selected_image_filename = 'asset/easy-selected.png'
hard_not_selected_image_filename = 'asset/hard-not-selected.png'
hard_selected_image_filename = 'asset/hard-selected.png'
start_normal_image_filename = 'asset/normal-start.png'
start_press_image_filename = 'asset/press-start.png'
start_pass_image_filename = 'asset/pass-start.png'
warning_choose_image_filename = 'asset/warning-choose.png'
warning_notstart_image_filename = 'asset/warning-notstart.png'
black_dot_image_filename = 'asset/black-dot.png'
white_dot_image_filename = 'asset/white-dot.png'
youwin_image_filename = 'asset/youwin.png'
youlose_image_filename = 'asset/youlose.png'
drawgame_image_filename = 'asset/drawgame.png'

# load the pictures
background = pygame.image.load(background_image_filename)
black = pygame.image.load(black_image_filename)
white = pygame.image.load(white_image_filename)
aifirst_not_selected = pygame.image.load(aifirst_not_selected_image_filename)
aifirst_selected = pygame.image.load(aifirst_selected_image_filename)
youfirst_not_selected = pygame.image.load(youfirst_not_selected_image_filename)
youfirst_selected = pygame.image.load(youfirst_selected_image_filename)
easy_not_selected = pygame.image.load(easy_not_selected_image_filename)
easy_selected = pygame.image.load(easy_selected_image_filename)
hard_not_selected = pygame.image.load(hard_not_selected_image_filename)
hard_selected = pygame.image.load(hard_selected_image_filename)
start_normal = pygame.image.load(start_normal_image_filename)
start_press = pygame.image.load(start_press_image_filename)
start_pass = pygame.image.load(start_pass_image_filename)
warning_choose = pygame.image.load(warning_choose_image_filename)
warning_notstart = pygame.image.load(warning_notstart_image_filename)
black_dot = pygame.image.load(black_dot_image_filename)
white_dot = pygame.image.load(white_dot_image_filename)
youwin = pygame.image.load(youwin_image_filename)
youlose = pygame.image.load(youlose_image_filename)
drawgame = pygame.image.load(drawgame_image_filename)


def draw_start(screen, situation):
    if situation == 'press':
        screen.blit(start_press, (600, 500))
    elif situation == 'normal':
        screen.blit(start_normal, (600, 500))
    elif situation == 'pass':
        screen.blit(start_pass, (600, 500))

def draw_first(screen, first):
    if first == 'you':
        screen.blit(youfirst_selected, (600, 170))
    else:
        screen.blit(youfirst_not_selected, (600, 170))

    if first == 'ai':
        screen.blit(aifirst_selected, (600, 240))
    else:
        screen.blit(aifirst_not_selected, (600, 240))

def draw_mode(screen, mode):
    if mode == 'easy':
        screen.blit(easy_selected, (600, 320))
    else:
        screen.blit(easy_not_selected, (600, 320))

    if mode == 'hard':
        screen.blit(hard_selected, (600, 390))
    else:
        screen.blit(hard_not_selected, (600, 390))


def draw_backconfig(screen):
    screen.blit(background, (0, 0))


def get_chessman_pos(pos):
    return (math.floor((pos[0] - 55) / 35 + 0.5) * 35 + 55 - 16, math.floor((pos[1] - 55) / 35 + 0.5) * 35 + 55 - 16)


def set_first(who):
    draw_first(screen, who)
    global first
    first = who


def set_mode(mode_):
    draw_mode(screen, mode_)
    global mode
    mode = mode_
    if mode == 'easy':
        config.searchdeep = 2
    elif mode == 'hard':
        config.searchdeep = 4


def draw_chessman(player, pos):
    '''
    :param player: you/ai
    :param pos: the position after calculated by the get_chessman_pos func
    :return: none
    '''
    if player == first:
        screen.blit(black, pos)
    else:
        screen.blit(white, pos)

def draw_dot_chessman(player, pos):
    if player == first:
        screen.blit(black_dot, pos)
    else:
        screen.blit(white_dot, pos)


def normalize_xy(x, y):
    return x * 35 + 55 - 16, y * 35 + 55 - 16


def draw_warning(screen, type):
    if type == 'choose':
        screen.blit(warning_choose, (200, 150))
    elif type == 'notstart':
        screen.blit(warning_notstart, (200, 150))


def draw_announcement(screen, is_winer):
    if is_winer:
        screen.blit(youwin, (265, 540))
    else:
        screen.blit(youlose, (265, 540))


def draw_drawgame(screen):
    screen.blit(drawgame, (250, 525))

g = Game()
pygame.init()

# build a window
screen = pygame.display.set_mode((800, 600), 0, 32)

# set the title of the window
pygame.display.set_caption("AI五子棋")

# draw the background and buttons
draw_backconfig(screen)
draw_first(screen, '')
draw_mode(screen, '')
draw_start(screen, 'normal')
pygame.display.update()

# record the last situations
last_sit = 'normal'
last_down_x = -1
last_down_y = -1
last_up_x = -1
last_up_y = -1
last_pos_x = -1
last_pos_y = -1

# the first player (ai or  you) and the difficulty of the game
first = ''
mode = ''
player_map = {1: 'ai', 2: 'you'}
player_reverse = {'ai': 'you', 'you': 'ai'}

game_start = False
warning = False
announcing_result = False
turn = ''  # you or ai

while True:
    if turn == 'ai' and game_start:
        point = g.begin()
        y, x = point.x, point.y  # the x and y are reversed
        if last_pos_x != -1 and last_pos_y != -1:
            draw_chessman('you', (last_pos_x, last_pos_y))
        # print(last_pos_x, last_pos_y)
        x, y = normalize_xy(x, y)
        draw_dot_chessman('ai', (x, y))
        pygame.display.update()
        if g.check() == 1:
            print('ai wins')
            announcing_result = True
            draw_announcement(screen, False)
            pygame.display.update()
            game_start = False
        elif g.board.counter == 225:
            print('draw')
            announcing_result = True
            draw_drawgame(screen)
            pygame.display.update()
            game_start = False
        last_pos_x = x
        last_pos_y = y
        turn = 'you'
        pygame.event.clear()

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()


        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            last_down_x, last_down_y = pos
            if not warning and 600 < pos[0] < 600 + 175 and 500 < pos[1] < 70 + 500:
                last_sit = 'press'
                draw_start(screen, last_sit)
                pygame.display.update()



        elif event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            last_up_x, last_up_y = pos
            if warning:
                draw_backconfig(screen)
                draw_first(screen, first)
                draw_mode(screen, mode)
                draw_start(screen, 'normal')
                pygame.display.update()
                warning = False

            if announcing_result:
                turn = ''
                last_pos_x = -1
                last_pos_y = -1
                first = ''
                mode = ''
                draw_backconfig(screen)
                draw_first(screen, first)
                draw_mode(screen, mode)
                draw_start(screen, 'normal')
                pygame.display.update()
                announcing_result = False

            # press the start button
            elif 600 < pos[0] < 600 + 175 and 500 < pos[1] < 70 + 500 and \
                    600 < last_down_x < 600 + 175 and 500 < last_down_y < 500 + 70:
                # last_sit = 'normal'
                # draw_start(screen, last_sit)
                # pygame.display.update()
                if not game_start and (first == 'you' or first == 'ai') and (mode == 'easy' or mode == 'hard'):
                    game_start = True
                    g.start()
                    turn = first
                    last_sit = 'press'
                    draw_start(screen, last_sit)
                    pygame.display.update()

                elif game_start:
                    # restart the game
                    last_sit = 'normal'
                    draw_start(screen, last_sit)
                    pygame.display.update()

                    game_start = False
                    draw_backconfig(screen)
                    draw_first(screen, '')
                    draw_mode(screen, '')
                    draw_start(screen, 'normal')
                    pygame.display.update()
                    first = ''
                    mode = ''
                    turn = ''
                    g.start()
                    last_pos_x = -1
                    last_pos_y = -1
                else:
                    last_sit = 'normal'
                    draw_start(screen, last_sit)
                    pygame.display.update()
                    draw_warning(screen, 'choose')
                    pygame.display.update()
                    warning = True

            # press the board
            elif 55 - 17 <= pos[0] <= 55 + 490 + 17 and\
                55 - 17 <= pos[1] <= 55 + 490 + 17:
                if get_chessman_pos(pos) == get_chessman_pos((last_down_x, last_down_y)):
                    if game_start:
                        if g.board.board[int((pos[1] + 16 - 55) / 35), int((pos[0] + 16 - 55) / 35)] != config.empty:
                            continue

                        if last_pos_x != -1 and last_pos_y != -1:
                            draw_chessman('ai', (last_pos_x, last_pos_y))
                            # print(last_pos_x, last_pos_y)
                        draw_dot_chessman('you', get_chessman_pos(pos))
                        last_pos_x, last_pos_y = get_chessman_pos(pos)
                        # the x versus y plane is opposite with the board
                        g.set(int((last_pos_y + 16 - 55) / 35), int((last_pos_x + 16 - 55) / 35), config.hum)
                        turn = 'ai'
                        pygame.display.update()
                        if g.check() == 2:
                            print('you win')
                            announcing_result = True
                            draw_announcement(screen, True)
                            pygame.display.update()
                            game_start = False

                        elif g.board.counter == 225:
                            print('draw')
                            announcing_result = True
                            draw_drawgame(screen)
                            pygame.display.update()
                            game_start = False
                    else:
                        draw_warning(screen, 'notstart')
                        pygame.display.update()
                        warning = True


            # press mode or first
            elif 600 <= pos[0] <= 600 + 170 and 170 <= pos[1] <= 170 + 60 and \
                    600 <= last_down_x <= 600 + 170 and 170 <= last_down_y <= 170 + 60 and \
                    not game_start:
                set_first('you')
                pygame.display.update()
            elif 600 <= pos[0] <= 600 + 170 and 240 <= pos[1] <= 240 + 60 and \
                    600 <= last_down_x <= 600 + 170 and 240 <= last_down_y <= 240 + 60 and \
                    not game_start:
                set_first('ai')
                pygame.display.update()
            elif 600 <= pos[0] <= 600 + 170 and 320 <= pos[1] <= 320 + 60 and \
                    600 <= last_down_x <= 600 + 170 and 320 <= last_down_y <= 320 + 60 and \
                    not game_start:
                set_mode('easy')
                pygame.display.update()
            elif 600 <= pos[0] <= 600 + 170 and 390 <= pos[1] <= 390 + 60 and \
                    600 <= last_down_x <= 600 + 170 and 390 <= last_down_y <= 390 + 60 and \
                    not game_start:
                set_mode('hard')
                pygame.display.update()



    # adjust the condition of the start icon
    x, y = pygame.mouse.get_pos()
    if 600 < x < 600 + 175 and 500 < y < 70 + 500:
        if last_sit == 'normal':
            last_sit = 'pass'
            draw_start(screen, last_sit)
            pygame.display.update()
    else:
        if last_sit == 'pass':
            last_sit = 'normal'
            draw_start(screen, last_sit)
            pygame.display.update()

