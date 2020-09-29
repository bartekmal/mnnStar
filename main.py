#!/usr/bin/env python

import os
import sys

import pygame
import pygame_menu

import textwrap
import random

# --> config part
nrOfQuestionsToAsk = 20
# <-- end of config

# get run-time path (needed to run both uncompiled / compiled versions)
frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(bundle_dir, 'src'))

# --> input paths
pathFontGame = os.path.join(
    bundle_dir, 'src', 'resources', 'fonts', 'freesansbold.ttf')
pathFontMenu = os.path.join(
    bundle_dir, 'src', 'resources', 'fonts', 'opensans_regular.ttf')
pathQuestions = os.path.join(bundle_dir, 'input', 'questions.yml')
pathAnimations = os.path.join(bundle_dir, 'src', 'resources', 'animations')
# <-- end of input paths

# prepare and validate a list of questions
from QuestionsHelper import *

questionsList = getRandomisedQuestionsList(pathQuestions)
if not questionsList or (len(questionsList) < nrOfQuestionsToAsk):
    print("Lista pytań jest zbyt krótka.")
    sys.exit(1)

# prepare the game display
pygame.init()
screen = pygame.display.set_mode((1500, 800))

intro = True
name = 'Nieznajomy!'
Zero25 = ["Poddający się – nigdy nie wygrywa, a wygrywający – nigdy się nie poddaje. ~ Napoleon Hill",
                "Potykając się, można zajść daleko, nie wolno tylko upaść i nie podnieść się. ~ Johan Wolfgang Goethe",
                "Musisz wierzyć w siebie wtedy, gdy nikt inny w Ciebie nie wierzy – to czyni Cię wygranym już na początku. ~ Venus Williams"]

Zero50 = ["Każde wielkie osiągnięcie zaczyna się decyzja by spróbować. ~ Anthony Robbins",
                 "Kto ma cierpliwość, będzie miał, co zechce. ~ Abraham Lincoln",
                 "Być zwyciężonym i nie ulec to zwycięstwo, zwyciężyć i osiąść na laurach to klęska. ~ Marszałek Józef Piłsudski"]

Zero75 = ["Zadaj sobie pytanie: Czy mogę dać z siebie więcej? Odpowiedź brzmi zwykle: Tak. ~ Paul Tergat",
                 "Możesz zrobić wszystko, co chcesz jeśli tylko trzymasz się tego celu wystarczająco długo. ~ Helen Keller",
                 "Cokolwiek umysł jest w stanie sobie wyobrazić jest to w stanie osiągnąć. ~ Napoleon Hill"]

Jeden = ["Najważniejszym i największym triumfem człowieka jest zwycięstwo nad samym sobą. ~ Platon",
         "Ten, kto przeniósł górę, zaczął od małych kamyków.",
         "Sukces to suma niewielkiego wysiłku powtarzanego z dnia na dzień. ~ Robert Collier"]
quotation = random.randint(0, 2)

menupic = [os.path.join(pathAnimations, 'menu{}.png'.format(i))
           for i in range(1, 7)]
answergif = [os.path.join(pathAnimations, 'odp{}.png'.format(i))
             for i in range(1, 3)]
currentQuestionNr = 0
ani1 = start_ticks = pygame.time.get_ticks()
ani2 = start_ticks = pygame.time.get_ticks()

scaleFactor = 100/nrOfQuestionsToAsk
i = 0
i2 = 0

userAnswerId = None
score = 0

game = False


def add_text(string, position, size=20, max_line_length=100, max_nr_of_lines=3):

    # scale the font size properly
    nr_of_lines = len(string) // max_line_length + 1
    if nr_of_lines > max_nr_of_lines:
        size = int(size * max_nr_of_lines / nr_of_lines)
    factor_for_line_splitting = 1.1
    font = pygame.font.Font(pathFontGame, size)

    # split the text into lines
    lines = textwrap.wrap(string, max_line_length, break_long_words=False)

    for i in range(len(lines)):
        text = font.render(lines[i], True, (255, 255, 255))
        # place the text with a proper offset in Y
        text_rect = text.get_rect(
            center=(position[0], position[1] + int(size * factor_for_line_splitting * (i - (nr_of_lines-1)/2))))
        screen.blit(text, text_rect)


def set_name(player_name):
    global name
    name = player_name + "!"


def button(msg, x, y, w, h, ic, ac, action=None, answerId=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            global userAnswerId
            userAnswerId = answerId
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    add_text(msg, (int(x+(w/2)), int(y+(h/2))),
             max_line_length=40, max_nr_of_lines=3)


def endIntro():
    global intro
    global game
    intro = False
    game = True
    screen.fill((40, 41, 35))


def exitGame():
    pygame.quit()
    sys.exit(0)


def animation1(scaleX=100, scaleY=100, PosX=1200, PosY=200):
    for i in range(len(menupic)):
        pic = pygame.image.load(menupic[i])
        pic_rect = pic.get_rect(center=(int(PosX), int(PosY)))
        pic = pygame.transform.scale(pic, (int(scaleX), int(scaleY)))
        pic_rect_scaled = pic.get_rect(center=(int(PosX), int(PosY)))
        screen.blit(pic, pic_rect)
        pygame.display.update()
        pygame.time.delay(100)
        pygame.draw.rect(screen, (40, 41, 35), (870, 0, 700, 650))


def animation2():
    global i2
    if i2 == 2:
        i2 = 0
    pic = pygame.image.load(answergif[i2])
    screen.blit(pic, (680, 150))
    pygame.display.update()
    pygame.time.delay(200)
    pygame.draw.rect(screen, (40, 41, 35), (680, 150, 150, 150))
    i2 += 1


def restart():
    global score
    global intro
    global game
    global userAnswerId
    score = 0
    intro = True
    game = False
    userAnswerId = None
    menu.enable()


def processAnswer():
    global currentQuestionNr
    global score

    # update the score and mark that a question was asked
    if questionsList[currentQuestionNr].checkAnswer(userAnswerId):
        score += 1
    currentQuestionNr += 1

    # check if the required nr of questions was already asked
    if currentQuestionNr >= nrOfQuestionsToAsk:
        global game
        game = False

    pygame.time.delay(100)


def start_the_game():
    menu.disable()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        clock = pygame.time.Clock()

        # show intro
        if intro:
            font = pygame.font.Font(pathFontGame, 50)
            text = font.render("Witaj", True, (255, 255, 255))
            text1 = font.render(name, True, (255, 255, 255))
            screen.fill((40, 41, 35))
            screen.blit(text, (0, 0))
            screen.blit(text1, (150, 0))
            add_text("Pomóż mi stać się większą gwiazdą!", (370, 80), 35)
            add_text("Odpowiadaj poprawnie na pytania, a urosnę!", (445, 120), 35)
            button("Graj!", 650, 400, 200, 100,
                   (24, 199, 24), (0, 255, 0), endIntro)
            animation1()

        # show game (questions)
        if game:
            screen.fill((40, 41, 35))

            # print the current question number and score
            add_text("Nr pytania: "+str(currentQuestionNr+1) +
                     " / " + str(nrOfQuestionsToAsk), (740, 660), 30)
            add_text("Zdobyte punkty: "+str(score), (740, 700), 30)

            # print the current question
            currentQuestionEntry = questionsList[currentQuestionNr]
            add_text(currentQuestionEntry.question, (750, 80),
                     30, max_line_length=85, max_nr_of_lines=3)
            button(currentQuestionEntry.answers[0], 100, 300, 600, 100, (24,
                                                                         199, 24), (0, 255, 0), processAnswer, 0)
            button(currentQuestionEntry.answers[1], 800, 300, 600, 100, (24,
                                                                         199, 24), (0, 255, 0), processAnswer, 1)
            button(currentQuestionEntry.answers[2], 100, 500, 600, 100, (24,
                                                                         199, 24), (0, 255, 0), processAnswer, 2)
            button(currentQuestionEntry.answers[3], 800, 500, 600, 100, (24,
                                                                         199, 24), (0, 255, 0), processAnswer, 3)

            if ani2 >= 100:
                animation2()

        # show summary and exit
        if game == False and intro == False:
            screen.fill((40, 41, 35))
            text = font.render("Dzięki", True, (255, 255, 255))
            text1 = font.render(name, True, (255, 255, 255))
            screen.blit(text, (0, 0))
            screen.blit(text1, (200, 0))
            add_text("Zdobyłeś: ", (110, 400), 40)
            add_text(str(score) + " pkt!", (400, 400), 40)
            proc = score/nrOfQuestionsToAsk
            if proc <= 0.205:
                add_text(Zero25[quotation], (750, 700))

            elif proc >= 0.206 and proc <= 0.50:
                add_text(Zero50[quotation], (750, 700))

            elif proc >= 0.501 and proc <= 0.75:
                add_text(Zero75[quotation], (750, 700))

            else:
                add_text(Jeden[quotation], (750, 700))

            button("Wyjdź", 650, 500, 200, 100,
                   (24, 199, 24), (0, 255, 0), exitGame)
            animation1((scaleFactor * nrOfQuestionsToAsk) + (score * 15), (scaleFactor *
                                                                           nrOfQuestionsToAsk) + (score * 15))

        pygame.display.update()
        clock.tick(60)


menu_theme = pygame_menu.themes.THEME_DARK.copy()
menu_theme.widget_font = pathFontMenu
menu_theme.title_font = pathFontMenu

menu = pygame_menu.Menu(800, 1500, 'Quiz', theme=menu_theme)
menu.add_text_input('Imię: ', onchange=set_name)
menu.add_vertical_margin(100)
menu.add_button('Graj!', start_the_game)
menu.add_vertical_margin(10)
menu.add_button('Wyjdź', pygame_menu.events.EXIT)

menu.mainloop(screen)
