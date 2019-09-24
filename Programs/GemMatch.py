import random, pygcurse, pygame, time, sys

pygame.init()

win = pygcurse.PygcurseWindow(8, 9, "GemmiPy", pygame.font.SysFont("Arial", 60))
win.autoupdate = False

COLORS = ["red", "blue", "green", "purple", "yellow"]
SYMBOLS = "♥■◆●▲"

board = []
for i in range(8):
    board.append([])
    for j in range(8):
        board[-1].append(random.choice(SYMBOLS))

def isDone():
    global score, goal
    return score < goal

def draw(delay=0.2):
    win.putchars("  " + ("{:°>4}".format(score)), 0, 8)
    for i in range(8):
        for j in range(8):
            if(board[i][j] == 0):
                win.putchar(" ", j, (7-i))
            else:
                win.putchar(board[i][j], j, (7 - i), fgcolor=COLORS[SYMBOLS.index(board[i][j])])
    win.update()
    time.sleep(delay)

def doRound():
    def getMove():
        gotMove = False
        down = False
        win.putchar(" ", 7, 8, bgcolor="green")
        win.update()
        while not gotMove:
            for event in pygame.event.get():
##                print(event.dict, event.type)
                if(event.type == 5):
                    x, y = win.getcoordinatesatpixel(event.pos)
                    if(y < 8):
                        down = (x, y)
                if(event.type == 6):
                    x, y = win.getcoordinatesatpixel(event.pos)
                    if(y < 8):
                        if(down is not False):
                            if((abs(down[0] - x) + abs(down[1] - y)) == 1):
                                index = {(0, -1):"u",
                                         (0, 1):"d",
                                         (-1, 0):"l",
                                         (1, 0):"r"}
                                win.putchar(" ", 7, 8, bgcolor="red")
                                win.update()
                                return chr(97 + down[0]) + str(8 - down[1]) + index[(x - down[0], y - down[1])]
                    else:
                        down = False
                if(event.type == 12):
                    pygame.quit()
                    sys.exit()
                

    def update(move, first = False):
        def swap(move):      
            global board
            def toNum(col):
                return "abcdefgh".find(col.lower())

            global board
            row = int(move[1])-1
            col = toNum(move[0])
            dir = move[2].lower()

            if(dir == "u"):
                newrow, newcol = row + 1, col
            elif(dir == "d"):
                newrow, newcol = row - 1, col
            elif(dir == "l"):
                newrow, newcol = row, col - 1
            elif(dir == "r"):
                newrow, newcol = row, col + 1

            tmp = board[row][col]
            board[row][col] = board[newrow][newcol]
            board[newrow][newcol] = tmp
            if(not first):
                draw(0)            

        def removeTiles(multi = 1):
            global board, score
            removed = False 
            remove = []
            for i in range(8):
                remove.append([])
                for j in range(8):
                    remove[-1].append(False)
                    
            for i in range(8):
                for j in range(6):
                    if((board[i][j] == board[i][j + 1]) and (board[i][j + 1] == board[i][j + 2])):
                        remove[i][j] = True
                        remove[i][j+1] = True
                        remove[i][j+2] = True
                    
            for j in range(8):
                for i in range(6):
                    if((board[i][j] == board[i + 1][j]) and (board[i + 1][j] == board[i + 2][j])):
                        remove[i][j] = True
                        remove[i+1][j] = True
                        remove[i+2][j] = True

            for i in range(8):
                for j in range(8):
                    if(remove[i][j]):
                        win.putchar(board[i][j], j, (7-i), bgcolor=(150, 0, 0))
                        removed = True
            if(not first and removed):
                draw()

            for i in range(8):
                for j in range(8):
                    if(remove[i][j]):
                        win.putchar("g", j, (7-i), bgcolor="black")
                        board[i][j] = 0
                        score += multi
            if(not first and removed):
                draw()
            return removed

        def dropTiles():
            global board
            for j in range(8):
                tmp = [board[i][j] for i in range(8) if board[i][j] != 0]
                for i in range(len(tmp)):
                    board[i][j] = tmp[i]

                for i in range(len(tmp), 8):
                     board[i][j] = 0

        def fillBoard():
            global board
            for i in range(8):
                for j in range(8):
                    if(board[i][j] == 0):
                        board[i][j] = random.choice(SYMBOLS)
            if(not first):
                draw()

        swap(move)
        if(not first):
            draw()
        more = True
        combo = 1
        while more:
            more = removeTiles(combo)
            dropTiles()
            fillBoard()
            if(not first and more):
                draw()
            combo += 1
    global turn
    if(turn == 0):
        for i in range(5):
            update("a1u", True)
        score = 0
        draw(0)

    move = getMove()

    update(move)

    
    turn += 1

score = 0
turn = 0
goal = 1000

draw(0)

while isDone():
    doRound()


win.tint(0, 20, 0)
draw()
time.sleep(1)
pygame.quit()
