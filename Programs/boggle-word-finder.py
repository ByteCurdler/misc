#!/usr/bin/python3
########################################################
#                  Boggle Word Finder                  #
#                       By Ian B.                      #
#                                                      #
#              "dictionary.txt" file at:               #
#       https://inventwithpython.com/cracking/         #
########################################################

CAN_REPEAT = False

import random

with open("dictionary.txt") as f:
    words = f.read().split()

def startInWords(n):
    return [i for i in words if i.startswith(n)] != []

def startMoreWords(n):
    return [i for i in words if i != n and i.startswith(n)] != []

if(not input("Random? ").lower().startswith("y")): #True for user input, False to grab a board online
    board = []
    while True:
        inp = input("Boggle] ")
        if(inp != ""):
            board.append(inp.upper().split())
        else:
            break
else:
    board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    dice = ['ARELSC','TABIYL','EDNSWO','BIOFXR', 'MCDPAE','IHFYEE','KTDNUO','MOQAJB',
            'ESLUPT','INVTGE','ZNDVAE','UKGELY', 'OCATAI','ULGWIR','SPHEIN','MSHARO']
    random.shuffle(dice)

    #Get the letter from each die
    for i in range(16):
        tmp = dice[i][random.randint(0, 5)]
        if(tmp == "Q"):
            tmp = "Qu"
        dice[i] = tmp

    for i in range(16):
        board[i // 4][i % 4] = dice[i]

    for i in range(4):
        print("Boggle] " + " ".join(
            [
                (
                    "Qu" if dice[(j*4)+i] == "Qu" else dice[(j*4)+i] + " "
                ) for j in range(4)
            ]))

results = {}

def findWord(x, y, word="", past=[]):
    if( x not in range(len(board[0])) or
        y not in range(len(board))       ): #If I'm off the board:
        return
    if((x, y) in past and (not CAN_REPEAT)):
        return
    me = word + board[y][x]
    if(not startInWords(me)): #If I don't start any word (including myself):
        return
    if(me in words): #If I'm a word:
        results[me] = None
        if(not startMoreWords(me)): #If I don't start any word that's not myself:
            return
    for pos in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        findWord(pos[0] + x, pos[1] + y, me, past + [(x, y)])

for x in range(len(board[0])):
    for y in range(len(board)):
        print("%s%%\t(%s words)" % (
            round(
                (
                    (x*len(board)) + y
                ) * (100/(len(board[0]) * len(board)))
            ), len(results)
        ))
        findWord(x, y)

print("100%%\t(%s words)" % len(results))      

print(
    "\n".join(
        sorted(
            [i for i in results]
        )
    )
)
