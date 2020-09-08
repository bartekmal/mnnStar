import pygame
import pygame_menu
import random
import os
import sys
import io

# --> config part
nrOfQuestionsToAsk = 5
# <-- end of config


class QuestionEntry:
    question = ''
    answers = []
    correctAnswer = ''

    def __init__(self, question, answers, correctAnswer):
        self.question = question
        self.answers = answers
        self.correctAnswer = correctAnswer

    def checkAnswer(self, answerToCheck):
        if answerToCheck == self.correctAnswer:
            return True
        else:
            return False


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

# validate the input data
if not (questions and answers and cor_answers):
    print("Nie znaleziono wymaganych danych.")
    pygame.quit()
    sys.exit(1)
elif (len(cor_answers) != len(questions)) or (len(answers) != 4*len(questions)):
    print("Niespodziewany format danych.")
    pygame.quit()
    sys.exit(1)

# combine the input data into a single list
questionsList = []
for i in range(len(questions)):
    # four consecutive entries in the answers list are for the given question
    answersToCurrentQuestion = [answers[i*4 + j] for j in range(4)]

    questionsList.append(QuestionEntry(
        questions[i], answersToCurrentQuestion, cor_answers[i]))

# shuffle the list to get random questions (can be then read one by one)
random.shuffle(questionsList)

# prepare the game display
pygame.init()
screen = pygame.display.set_mode((1500, 800))

intro = True
name = 'Nieznajomy!'
menupic = ['animations/menu1.png', 'animations/menu2.png', 'animations/menu3.png',
           'animations/menu4.png', 'animations/menu5.png', 'animations/menu6.png']
answergif = ['animations/odp1.png', 'animations/odp2.png']
currentQuestionNr = 0
ani1 = start_ticks = pygame.time.get_ticks()
ani2 = start_ticks = pygame.time.get_ticks()
i = 0
i2 = 0

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


def exitGame():
    pygame.quit()
    sys.exit(0)


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
    global intro
    global game
    global user_answer
    print("d")
    score = 0
    intro = True
    game = False
    user_answer = None
    menu.enable()


def processAnswer():
    global currentQuestionNr
    global score

    # update the score and mark that a question was asked
    if questionsList[currentQuestionNr].checkAnswer(user_answer):
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

        # show game (questions)
        if game:
            screen.fill((40, 41, 35))

            # print the current question number and score
            add_text("Nr pytania: "+str(currentQuestionNr+1) +
                     " / " + str(nrOfQuestionsToAsk), (740, 660), 50)
            add_text("Zdobyte punkty: "+str(score), (740, 700), 50)

            # print the current question
            currentQuestionEntry = questionsList[currentQuestionNr]
            add_text(currentQuestionEntry.question, (750, 100), 40)
            button(currentQuestionEntry.answers[0], 100, 300, 600, 100, (24,
                                                                         199, 24), (0, 255, 0), processAnswer, currentQuestionEntry.answers[0])
            button(currentQuestionEntry.answers[1], 800, 300, 600, 100, (24,
                                                                         199, 24), (0, 255, 0), processAnswer, currentQuestionEntry.answers[1])
            button(currentQuestionEntry.answers[2], 100, 500, 600, 100, (24,
                                                                         199, 24), (0, 255, 0), processAnswer, currentQuestionEntry.answers[2])
            button(currentQuestionEntry.answers[3], 800, 500, 600, 100, (24,
                                                                         199, 24), (0, 255, 0), processAnswer, currentQuestionEntry.answers[3])

            if ani2 >= 100:
                animation2()

        # show summary and exit
        if game == False and intro == False:
            screen.fill((40, 41, 35))
            text = font.render("Dzięki", True, (255, 255, 255))
            text1 = font.render(name, True, (255, 255, 255))
            screen.blit(text, (0, 0))
            screen.blit(text1, (200, 0))
            add_text("Zdobyłeś: ", (110, 400), 60)
            add_text(str(score) + " pkt!", (400, 400), 60)
            button("Wyjdź", 650, 500, 200, 100,
                   (24, 199, 24), (0, 255, 0), exitGame)

        pygame.display.update()
        clock.tick(60)


menu = pygame_menu.Menu(800, 1500, 'Quiz', theme=pygame_menu.themes.THEME_DARK)
menu.add_text_input('Imię: ', onchange=set_name)
menu.add_vertical_margin(100)
menu.add_button('Graj!', start_the_game)
menu.add_vertical_margin(10)
menu.add_button('Wyjdź', pygame_menu.events.EXIT)

menu.mainloop(screen)
