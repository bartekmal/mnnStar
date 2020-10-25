#!/usr/bin/env python

import os
import sys

import pygame
import pygame_menu

import textwrap
import random

# --> config part
nrOfQuestionsToAsk = 10

# buttons
nrOfPossibleAnswers = 4
buttonsConfig = {
    'positions' : [
        (100, 300, 600, 100),
        (800, 300, 600, 100),
        (100, 500, 600, 100),
        (800, 500, 600, 100)
    ],
    'colorWhenIdle' : (24, 199, 24),
    'colorWhenActive' : (0, 255, 0)
}

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
Zero25 = ["Poddający się – nigdy nie wygrywa, a wygrywający – nigdy się nie poddaje. (Napoleon Hill)",
                "Potykając się, można zajść daleko, nie wolno tylko upaść i nie podnieść się. (Johan Wolfgang Goethe)",
                "Musisz wierzyć w siebie wtedy, gdy nikt inny w Ciebie nie wierzy – to czyni Cię wygranym już na początku. (Venus Williams)"]

Zero50 = ["Każde wielkie osiągnięcie zaczyna się decyzja by spróbować. (Anthony Robbins)",
                 "Kto ma cierpliwość, będzie miał, co zechce. (Abraham Lincoln)",
                 "Być zwyciężonym i nie ulec to zwycięstwo, zwyciężyć i osiąść na laurach to klęska. (Marszałek Józef Piłsudski)"]

Zero75 = ["Zadaj sobie pytanie: Czy mogę dać z siebie więcej? Odpowiedź brzmi zwykle: Tak. (Paul Tergat)",
                 "Możesz zrobić wszystko, co chcesz jeśli tylko trzymasz się tego celu wystarczająco długo. (Helen Keller)",
                 "Cokolwiek umysł jest w stanie sobie wyobrazić jest to w stanie osiągnąć. (Napoleon Hill)"]

Jeden = ["Najważniejszym i największym triumfem człowieka jest zwycięstwo nad samym sobą. (Platon)",
         "Ten, kto przeniósł górę, zaczął od małych kamyków. (autor nieznany)",
         "Sukces to suma niewielkiego wysiłku powtarzanego z dnia na dzień. (Robert Collier)"]
quotation = random.randint(0, 2)

menupic = [os.path.join(pathAnimations, 'menu{}.png'.format(i))
           for i in range(1, 7)]
answergif = [os.path.join(pathAnimations, 'odp{}.png'.format(i))
             for i in range(1, 3)]
currentQuestionNr = 0

scaleFactor = 100/nrOfQuestionsToAsk
i = 0
i2 = 0

flagShowAnwers = False
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

    # if hovering
    if x+w > mouse[0] > x and y+h > mouse[1] > y:

        pygame.draw.rect(screen, ac, (x, y, w, h))

        # if clicked and was some action
        if click[0] == 1 and action != None:
            # special case for the answer buttons
            if action != processAnswer:
                action()
            else:
                # get and process the current user answer
                global userAnswerId
                userAnswerId = answerId
                action()
                # set the global flag to show the correct/wrong answers
                global flagShowAnwers 
                flagShowAnwers = True

    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    # print text
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
    global i
    
    pic = pygame.image.load(menupic[i])
    pic = pygame.transform.scale(pic, (int(scaleX), int(scaleY)))
    pic_rect = pic.get_rect(center=(int(PosX), int(PosY)))
    screen.blit(pic, pic_rect)

    # check if that was the last available index (reset or increment)
    if i == len(menupic) - 1:
        i = 0
    else:
        i += 1

def animation2():
    global i2
    
    pic = pygame.image.load(answergif[i2])
    screen.blit(pic, (680, 150))
   
    # check if that was the last available index (reset or increment)
    if i2 == len(answergif) - 1:
        i2 = 0
    else:
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

# process answer and return info if it was right
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
            screen.fill((40, 41, 35))
            font = pygame.font.Font(pathFontGame, 50)
            text = font.render("Witaj", True, (255, 255, 255))
            text1 = font.render(name, True, (255, 255, 255))
            screen.blit(text, (500, 50))
            screen.blit(text1, (650, 50))
            add_text("Ogromna Galaktyka, nazywana Drogą Mleczną, to nasz międzygwiezdny DOM. Tutaj też żyje mała Protogwiazda Vena, która bardzo chce w przyszłości stać się Białym Karłem, tak jak większość jej kolegów. Jeżeli chcesz pomóc, to musisz jej dostarczyć międzygalaktyczne paliwo, którym jest wodór. Jak tego dokonać? To nic trudnego! Wejdź do gry i odpowiadaj na pytania, by Vena mogła spełnić swoje marzenia i zabłysnąć!",
                     (750, 325), 35, max_line_length=50, max_nr_of_lines=10)
            button("Graj!", 650, 600, 200, 100,
                   (24, 199, 24), (0, 255, 0), endIntro)
            animation1(100, 100, 1350, 100)

        # show game (questions)
        if game:
            screen.fill((40, 41, 35))

            animation2()
            # this delay is added to slow down the star animation (better would be probably to use some kind of a clock...)
            pygame.time.delay(100)

            # print the current question number and score
            add_text("Nr pytania: "+str(currentQuestionNr+1) +
                     " / " + str(nrOfQuestionsToAsk), (740, 660), 30)
            add_text("Zdobyte punkty: "+str(score), (740, 700), 30)

            # print the current question and answers
            currentQuestionEntry = questionsList[currentQuestionNr]
            add_text(currentQuestionEntry.question, (750, 80), 30, max_line_length=85, max_nr_of_lines=3)
            for i in range(nrOfPossibleAnswers):
                buttonPos =  buttonsConfig['positions'][i]
                button(currentQuestionEntry.answers[i], buttonPos[0], buttonPos[1], buttonPos[2], buttonPos[3], buttonsConfig['colorWhenIdle'], buttonsConfig['colorWhenActive'], processAnswer, i)

            # check if the answer was just given and show the correct/wrong ones
            global flagShowAnwers
            if flagShowAnwers:
                flagShowAnwers = False
                for i in range(nrOfPossibleAnswers):
                   buttonPos =  buttonsConfig['positions'][i]
                   buttonColor = pygame.colordict.THECOLORS['green'] if currentQuestionEntry.checkAnswer(i) else pygame.colordict.THECOLORS['red']
                   button(currentQuestionEntry.answers[i], buttonPos[0], buttonPos[1], buttonPos[2], buttonPos[3], buttonColor, buttonColor)

                # hold for a moment to see the answers
                pygame.display.update()
                pygame.time.delay(2000)

        # show summary and exit
        if game == False and intro == False:
            screen.fill((40, 41, 35))
            text = font.render("Brawo ", True, (255, 255, 255))
            text1 = font.render(name, True, (255, 255, 255))
            screen.blit(text, (25, 25))
            screen.blit(text1, (200, 25))
            add_text("Widzę, że starałeś się z całych sił, by pomóc małej Venie. Dzięki Tobie urosła! Możesz ją teraz obserwować na nocnym niebie w towarzystwie Syriusza!", (400, 200), 25, 60, 5)
            add_text("Zdobyłeś: ", (125, 350), 40)
            add_text(str(score) + " pkt!", (400, 350), 40)
            proc = score/nrOfQuestionsToAsk
            if proc <= 0.205:
                add_text(Zero25[quotation], (750, 750))
            elif proc >= 0.206 and proc <= 0.50:
                add_text(Zero50[quotation], (750, 750))

            elif proc >= 0.501 and proc <= 0.75:
                add_text(Zero75[quotation], (750, 750))
            else:
                add_text(Jeden[quotation], (750, 750))

            button("Wyjdź", 650, 550, 200, 100,
                   (24, 199, 24), (0, 255, 0), exitGame)
            animation1((scaleFactor * nrOfQuestionsToAsk) + (score * 15), (scaleFactor *
                                                                           nrOfQuestionsToAsk) + (score * 15))

        # display the screen and wait
        pygame.display.update()
        pygame.time.delay(100)

        clock.tick(60)


menu_theme = pygame_menu.themes.THEME_DARK.copy()
menu_theme.widget_font = pathFontMenu
menu_theme.title_font = pathFontMenu

menu = pygame_menu.Menu(800, 1500, 'PhyStar', theme=menu_theme)
menu.add_text_input('Imię: ', onchange=set_name)
menu.add_vertical_margin(100)
menu.add_button('Graj!', start_the_game)
menu.add_vertical_margin(10)
menu.add_button('Wyjdź', pygame_menu.events.EXIT)

menu.mainloop(screen)
