import random
from time import sleep

speed = 1 / float(input("Speed factor?"))

class t:
    roll =      [(0.25 + (i * 0.075)) * speed for i in range(0, 11)]
    find =      0.4 * speed
    hold =      0.25 * speed
    findMain =  0.5 * speed

for i in range(3, 0, -1):
    print(i)
    sleep(1)
print("Go!")

sleep(t.roll[10])

dice = [random.randint(1, 6) for i in range(10)]

sleep(t.findMain)

tmp = [0] * 6
for i in dice:
    tmp[i - 1] += 1

target = tmp.index(max(tmp)) + 1

while [i for i in dice if i != dice[0]] != []: #While all the dice are not the same
    print(", ".join(
        [
            str(i) for i in dice if i != target
        ]
    ))
    rolling = [i for i in range(10) if dice[i] != target]
    sleep(t.find + t.hold + t.roll[len(rolling)])
    for i in rolling:
        dice[i] = random.randint(1, 6)

sleep(t.find)

print("""
DDDDDDDDDDDDD             OOOOOOOOO     NNNNNNNN        NNNNNNNNEEEEEEEEEEEEEEEEEEEEEE
D::::::::::::DDD        OO:::::::::OO   N:::::::N       N::::::NE::::::::::::::::::::E
D:::::::::::::::DD    OO:::::::::::::OO N::::::::N      N::::::NE::::::::::::::::::::E
DDD:::::DDDDD:::::D  O:::::::OOO:::::::ON:::::::::N     N::::::NEE::::::EEEEEEEEE::::E
  D:::::D    D:::::D O::::::O   O::::::ON::::::::::N    N::::::N  E:::::E       EEEEEE
  D:::::D     D:::::DO:::::O     O:::::ON:::::::::::N   N::::::N  E:::::E             
  D:::::D     D:::::DO:::::O     O:::::ON:::::::N::::N  N::::::N  E::::::EEEEEEEEEE   
  D:::::D     D:::::DO:::::O     O:::::ON::::::N N::::N N::::::N  E:::::::::::::::E   
  D:::::D     D:::::DO:::::O     O:::::ON::::::N  N::::N:::::::N  E:::::::::::::::E   
  D:::::D     D:::::DO:::::O     O:::::ON::::::N   N:::::::::::N  E::::::EEEEEEEEEE   
  D:::::D     D:::::DO:::::O     O:::::ON::::::N    N::::::::::N  E:::::E             
  D:::::D    D:::::D O::::::O   O::::::ON::::::N     N:::::::::N  E:::::E       EEEEEE
DDD:::::DDDDD:::::D  O:::::::OOO:::::::ON::::::N      N::::::::NEE::::::EEEEEEEE:::::E
D:::::::::::::::DD    OO:::::::::::::OO N::::::N       N:::::::NE::::::::::::::::::::E
D::::::::::::DDD        OO:::::::::OO   N::::::N        N::::::NE::::::::::::::::::::E
DDDDDDDDDDDDD             OOOOOOOOO     NNNNNNNN         NNNNNNNEEEEEEEEEEEEEEEEEEEEEE
""")
