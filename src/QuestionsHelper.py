#!/usr/bin/env python

import io
import os
import random
import sys

import yaml


class QuestionEntry:
    question = ''
    answers = []
    correctAnswerId = 0

    def __init__(self, question, answers, correctAnswerId):
        self.question = question
        self.answers = answers
        self.correctAnswerId = correctAnswerId

    def checkAnswer(self, answerToCheck):
        if answerToCheck == self.correctAnswerId:
            return True
        else:
            return False


def getDataFromFile(fileName):
    data = []
    try:
        with io.open(fileName, 'r', encoding='utf8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print("Nie znaleziono pliku: {}".format(fileName))
    return data


def getRandomisedQuestionsList(fileName):

    randomisedQuestionsList = []

    # load the input data
    entries = getDataFromFile(fileName)

    # validate the input data
    if not entries:
        print("Nie znaleziono wymaganych danych.")
        sys.exit(1)

    # make a final list
    for entry in entries:
        randomisedQuestionsList.append(QuestionEntry(
            entry['question'], entry['answers'], entry['correctAnswerId']))

    # validate questions
    for el in randomisedQuestionsList:
        if not el.correctAnswerId < len(el.answers):
            print("W tym pytaniu podana poprawna odpowiedź jest spoza zakresu.")
            print("-->{}".format(el.question))
            sys.exit(1)

    # shuffle the list to get random questions (can be then read one by one)
    random.shuffle(randomisedQuestionsList)

    return randomisedQuestionsList
