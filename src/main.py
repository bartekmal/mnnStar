import pygame
import pygame_menu
import random
import os
import sys
import io

pygame.init()
screen = pygame.display.set_mode((1500, 800))


def getDataFromFile(fileName):
    data = []
    try:
        with io.open(fileName, 'r', encoding='utf8') as f:
            data = f.read().split('$')
    except FileNotFoundError:
        print("Nie znaleziono pliku: {}".format(fileName))
    return data


# load the input data
questions = getDataFromFile('data.txt')
answers = getDataFromFile('odpowiedzi.txt')
cor_answers = getDataFromFile('poprawneODP.txt')

# check if the input data exist
if not (questions and answers and cor_answers):
    print("Nie znaleziono wymaganych danych.")
    pygame.quit()
    sys.exit(1)

was = []
intro = True
name = 'Nieznajomy!'
menupic = ['animations/menu1.png', 'animations/menu2.png', 'animations/menu3.png',
           'animations/menu4.png', 'animations/menu5.png', 'animations/menu6.png']
answergif = ['animations/odp1.png', 'animations/odp2.png']
actual_question = 0
was.append(actual_question)
ani1 = start_ticks = pygame.time.get_ticks()
ani2 = start_ticks = pygame.time.get_ticks()
i = 0
i2 = 0
print(len(questions))
print(len(answers))

user_answer = None
score = 0

game = False


def add_text(string, position, size=30):
    font = pygame.font.SysFont("freesansbold.ttf", size)
    text = font.render(string, True, (255, 255, 255))
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)


def set_name(player_name):
    global name
    name = player_name + "!"


def button(msg, x, y, w, h, ic, ac, action=None, answer=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            global user_answer
            user_answer = answer
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    add_text(msg, (x+(w/2), y+(h/2)))


def endIntro():
    global intro
    global game
    intro = False
    game = True
    screen.fill((40, 41, 35))


def animation1():
    for i in (0, 5):
        pic = pygame.image.load(menupic[i])
        screen.blit(pic, (1350, 0))
        pygame.display.update()
        pygame.time.delay(100)
        pygame.draw.rect(screen, (40, 41, 35), (1300, 0, 200, 100))


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
    global was
    global intro
    global game
    global user_answer
    print("d")
    score = 0
    was = []
    intro = True
    game = False
    user_answer = None
    menu.enable()


def check():
    global actual_question
    global score
    if user_answer == cor_answers[actual_question]:
        score += 1
    actual_question = random.randint(0, len(questions)-1)
    pygame.time.delay(100)
    if len(was) == len(questions)-1:
        global game
        game = False
    draw = True
    while draw:
        if actual_question in was:
            actual_question = random.randint(0, len(questions)-1)

        else:
            draw = False
    was.append(actual_question)


def start_the_game():
    menu.disable()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        clock = pygame.time.Clock()
        if intro:
            font = pygame.font.SysFont("", 80)
            text = font.render("Witaj", True, (255, 255, 255))
            text1 = font.render(name, True, (255, 255, 255))
            screen.fill((40, 41, 35))
            screen.blit(text, (0, 0))
            screen.blit(text1, (150, 0))
            add_text("Pomóż mi stać się większą gwiazdą!", (370, 80), 60)
            add_text("Odpowiadaj poprawnie na pytania, a urosnę!", (445, 120), 60)
            button("Graj!", 650, 400, 200, 100,
                   (24, 199, 24), (0, 255, 0), endIntro)
            animation1()

        if game:
            screen.fill((40, 41, 35))
            add_text(questions[actual_question], (750, 100), 40)

            if actual_question != 0:
                button(answers[(actual_question*4)+3], 100, 300, 600, 100, (24,
                                                                            199, 24), (0, 255, 0), check, answers[(actual_question*4)+3])
                button(answers[(actual_question*4)+2], 800, 300, 600, 100, (24,
                                                                            199, 24), (0, 255, 0), check, answers[(actual_question*4)+2])
                button(answers[(actual_question*4)+1], 100, 500, 600, 100, (24,
                                                                            199, 24), (0, 255, 0), check, answers[(actual_question*4)+1])
                button(answers[actual_question*4], 800, 500, 600, 100, (24,
                                                                        199, 24), (0, 255, 0), check, answers[actual_question*4])
                print(cor_answers[actual_question])

            else:
                button(answers[0], 100, 300, 600, 100,
                       (24, 199, 24), (0, 255, 0), check, answers[0])
                button(answers[1], 800, 300, 600, 100,
                       (24, 199, 24), (0, 255, 0), check, answers[1])
                button(answers[2], 100, 500, 600, 100,
                       (24, 199, 24), (0, 255, 0), check, answers[2])
                button(answers[3], 800, 500, 600, 100,
                       (24, 199, 24), (0, 255, 0), check, answers[3])

            add_text(str(score), (740, 700), 50)
            add_text("/", (790, 700), 50)
            add_text(str(len(questions)-1), (840, 700), 50)
            if ani2 >= 100:
                animation2()

            if game == False and intro == False:
                screen.fill((40, 41, 35))
                text = font.render("Dzięki", True, (255, 255, 255))
                text1 = font.render(name, True, (255, 255, 255))
                screen.blit(text, (0, 0))
                screen.blit(text1, (200, 0))
                add_text("Zdobyłeś: ", (110, 400), 60)
                add_text(str(score) + "pkt!", (400, 400), 60)

        pygame.display.update()
        clock.tick(60)


menu = pygame_menu.Menu(800, 1500, 'Quiz', theme=pygame_menu.themes.THEME_DARK)
menu.add_text_input('Imię: ', onchange=set_name)
menu.add_vertical_margin(100)
menu.add_button('Graj!', start_the_game)
menu.add_vertical_margin(10)
menu.add_button('Wyjdź', pygame_menu.events.EXIT)

menu.mainloop(screen)
