import re
import pymorphy2 as mr

from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
import udp_client
from threading import Thread

patterns = "[A-Za-z!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()

sl = {'собака', 'пёс'}
com = {"вперёд", "вперед", "прямо", "назад", "отступить", "перевернуться", "лечь", "живот",
       "опуститься", "вправо","направо","отойди вправо","влево","налево","отойди влево", "стой", "остановись", "замри", "стоить"}

sender = udp_client.Sender()

thread1 = Thread(target=sender.send_date)
thread1.start()

def declination(n):
    morph = mr.MorphAnalyzer()
    words = morph.parse('шаг')[0]
    return words.make_agree_with_number(n).word


def commands_forward(n):
    print('Распознана команда: идти вперед')
    r = declination(n)
    # CreateAudio.audio_sound('Распознана команда: ' + str(n) + f'{r} вперед')
    # return 'Распознана команда: ' + str(n) + 'шагов вперед'
    sender.change_value(1, 9)

def commands_back(n):
    r = declination(n)
    print('Распознана команда: идти назад')
    sender.change_value(1, 10)
    # CreateAudio.audio_sound('Распознана команда: ' + str(n) + f'{r} назад')
    # return 'Распознана команда: ' + str(n) + 'шагов назад'


def commands_down(args):
    n = args
    print('Распознана команда: Опуститься на живот')
    sender.change_value(1, 3)
    # CreateAudio.audio_sound('Распознана команда: Опуститься на живот')
    # return 'Распознана команда: Опуститься на живот'

def commands_go_right(args):
    n = args
    print('Распознана команда: идти вправо')
    sender.change_value(1, 8)
    # CreateAudio.audio_sound('Распознана команда: Опуститься на живот')
    # return 'Распознана команда: Опуститься на живот

def commands_go_left(args):
    n = args
    print('Распознана команда: идти влево')
    sender.change_value(1, 7)
    # CreateAudio.audio_sound('Распознана команда: Опуститься на живот')
    # return 'Распознана команда: Опуститься на живот

def commands_stay(args):
    n = args
    print('Распознана команда: стоять')
    sender.change_value(1, 4)
    # CreateAudio.audio_sound('Распознана команда: Опуститься на живот')
    # return 'Распознана команда: Опуститься на живот


commands = {
    ("вперёд", "прямо", "вперед"): commands_forward,
    ("назад", "отступить"): commands_back,
    ("вправо","направо","отойди вправо"): commands_go_right,
    ("влево","налево","отойди влево"): commands_go_left,
    ("лечь", "живот", "опуститься"): commands_down,
    ("стоить", "стой", "остановись", "замри"): commands_stay
}


def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)  # Удаляем мусор
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            tokens.append(token)
    return tokens


def result(stroka):
    n = len(stroka)
    flag = False
    for i in range(n):
        if stroka[i] in sl:
            commands_indentify(stroka[i + 1:])
            flag = True
            break
    if not flag:
        print("NONONO")


def commands_indentify(line):
    args = ['no']
    flag = True
    line_base = lemmatize(line)
    print(line_base)
    try:
        per = set(line_base) & com
        command_name = per.pop()
        # if command_name in ["вперёд", 'вперед', "прямо", "назад", "отступить"]:
        #     args = [int(line[i]) for i in range(len(line) - 1) if line[i + 1] in 'шаг']
        for key in commands.keys():
            if command_name in key:
                commands[key](args[0])
                flag = False
                break
        if flag:
            print("Command not found")
    except Exception as ex:
        print(ex)

