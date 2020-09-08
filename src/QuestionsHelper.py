import random
import os
import sys
import io


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


def getRandomisedQuestionsList():

    randomisedQuestionsList = []

    # load the input data
    questions = getDataFromFile('data.txt')
    answers = getDataFromFile('odpowiedzi.txt')
    cor_answers = getDataFromFile('poprawneODP.txt')

    # validate the input data
    if not (questions and answers and cor_answers):
        print("Nie znaleziono wymaganych danych.")
        sys.exit(1)
    elif (len(cor_answers) != len(questions)) or (len(answers) != 4*len(questions)):
        print("Niespodziewany format danych.")
        sys.exit(1)

    # combine the input data into a single list
    for i in range(len(questions)):
        # four consecutive entries in the answers list are for the given question
        answersToCurrentQuestion = [answers[i*4 + j] for j in range(4)]

        randomisedQuestionsList.append(QuestionEntry(
            questions[i], answersToCurrentQuestion, cor_answers[i]))

    # shuffle the list to get random questions (can be then read one by one)
    random.shuffle(randomisedQuestionsList)

    return randomisedQuestionsList
