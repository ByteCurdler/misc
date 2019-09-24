import pygcurse,pygame,time,sys
from pygame.locals import *

names = [ "HB", "NNN",      "LSL",   "LEL", "PT",  "JC",    "KC",""]
colors = ["red",(255,100,0),"yellow",(0, 255, 0),(0, 255, 255),"purple","navy","black"]

situations = []
for a in range(7):
    for b in range(7):
        for c in range(7):
            if(a < b and b < c):
                tmp = [0,0,0,0,0,0,0]
                tmp[a] = 1
                tmp[b] = 1
                tmp[c] = 1
                situations.append(tmp)

def filt(data):
    global situations
    tmpSit = []
    for sit in situations:
        ok = False
        for pat in data:
            patOk = True
            for j in range(7):
                if(pat[j] != -1 and pat[j] != sit[j]):
                    patOk = False
            ok = ok or patOk
        if(ok):
            tmpSit.append(sit)
    situations = tmpSit

    if(len(situations) == 0):
        win = pygcurse.PygcurseWindow(34,3,None, None)
        win.font = pygame.font.Font(None,50)
        win.putchars("I think you messed up somewhere.",1,1,"red")
        time.sleep(5)
        pygame.quit()
        sys.exit()
    elif(len(situations) == 1):
        cor = []
        for i in range(7):
            if(situations[0][i] == 1):
                cor.append(names[i])
        win = pygcurse.PygcurseWindow(len(" It's {}, {}, and {}! ".format(cor[0],cor[1],cor[2])),4,None, None)
        win.font = pygame.font.Font(None,50)
        win.putchars("I've got it!",1,1,"green")
        win.putchars("It's ",1,2,"green")
        win.putchars(str(cor[0]) + ", ",6,2,colors[names.index(cor[0])])
        win.putchars(str(cor[1]) + ", and ",len("It's {}, ".format(cor[0]))+1,2,colors[names.index(cor[1])])
        win.putchars(str(cor[2]) + "!",len("It's {}, {}, and ".format(cor[0],cor[1]))+1,2,colors[names.index(cor[2])])
        time.sleep(5)
        pygame.quit()
        sys.exit()

def cardFilt(inN,in1,in2,in3):
    ret = [[-1,-1,-1,-1,-1,-1,-1]]
    if(inN == 0):
        ret = [-1,-1,-1,-1,-1,-1,-1]
        ret[in1] = 0
        ret[in2] = 0
        ret[in3] = 0
        ret = [ret]
    elif(inN == 1):
        ret = []
        for i in range(3):
            retPart = [-1,-1,-1,-1,-1,-1,-1]
            retPart[in1] = (i == 0)
            retPart[in2] = (i == 1)
            retPart[in3] = (i == 2)
            ret.append(retPart)
    elif(inN == 2):
        ret = []
        for i in range(3):
            retPart = [-1,-1,-1,-1,-1,-1,-1]
            retPart[in1] = not (i == 0)
            retPart[in2] = not (i == 1)
            retPart[in3] = not (i == 2)
            ret.append(retPart)
            
    filt(ret)

while True:
    win = pygcurse.PygcurseWindow(9,11,"Three Of A Crime")
    win.font = pygame.font.Font(None,100)
    ##win.fill("o")

    for i in range(-1,7):
        win.putchars(names[i],1,i+1,colors[i])
        win.putchars("o",5,i+1,colors[i])


    numColors = [(255,150,0),(0, 255, 255),(0, 255, 0),"black"]

    for i in range(-1,3):
        win.putchar(str(i),1+i,9,numColors[i])

    win.putchars("Go!",5,9,"black",(0, 255, 0))

    def inRange(spot,area):
        return spot[0] >= min(area[0],area[2]) and spot[0] <= max(area[0],area[2]) and spot[1] >= min(area[1],area[3]) and spot[1] <= max(area[1],area[3])

    select = [-1,[]]

    go = False
    
    while not go:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN):
                x, y = win.getcoordinatesatpixel(event.pos)
                if(inRange((x,y),(5,1,5,7))):
                    if(y-1 in select[1]):
                        win.putchar("o",x,y,None,"black")
                        select[1].remove(y-1)
                        print("Removed suspect {} ({})".format(y-1,names[y-1]))
                    else:
                        win.putchar("o",x,y,None,"gray")
                        select[1].append(y-1)
                        print("Added suspect {} ({})".format(y-1,names[y-1]))
                elif(inRange((x,y),(1,9,3,9))):
                    win.putchar(str(select[0]),select[0]+1,9,None,"black")
                    select[0] = x - 1
                    win.putchar(str(select[0]),x,y,None,"gray")
                    print("Swiched number of suspects to {}.".format(x-1))  
                elif(inRange((x,y),(5,9,7,9))):
                    if(len(select[1]) == 3): #Checking selected suspects
                        if(select[0] != -1): #Checking number of suspects
                            go = True
    cardFilt(select[0],*select[1])
    
                
pygame.quit()
