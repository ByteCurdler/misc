#!/usr/bin/python3
"""Deadfish X
https://esolangs.org/wiki/Deadfish_x

Varible N starts as 0
N stays between 0 and 255

Commands:
F: Start a function: F<name><code>f
i: Increment N
d: Decrement N
s: Square N
o: Output N as number
f: End a function: See [F] OR
   Execute function: f<name> 
a: Output N as ASCII
r: Set N to 0
"""

class GoToInteractive(Exception):
    pass

n = 0
funcs = {}

def execute(code):
    global n, funcs, openEnd
    stack = list(code.replace(" ", "").replace("\n", ""))
    while stack:
        cmd = stack.pop(0)
        if(cmd == "F"):
            try:
                funcName = stack.pop(0)
                funcs[funcName] = ""
                try:
                    while stack[0] != "f":
                        if(stack[0] not in "Fidsofar"):
                            print("\nUnknown command %s in function %s." % (stack[0], funcName))
                            halt() 
                        funcs[funcName] += stack.pop(0)
                    stack.pop(0)
                except IndexError:
                    print("\nError: Expected more code or 'f' in function %s, got EOF." % funcName)
                    halt()
            except IndexError:
                print("\nError: Expected function name, got EOF.")
                halt()
        elif(cmd == "i"):
            n += 1
        elif(cmd == "d"):
            n -= 1
        elif(cmd == "s"):
            n *= n
        elif(cmd == "o"):
            print(n)
            openEnd = False
        elif(cmd == "f"):
            try:
                funcName = stack.pop(0)
                execute(funcs[funcName])
            except IndexError:
                print("\nError: Expected function name, got EOF.")
                halt()
        elif(cmd == "a"):
            try:
                print(chr(n), end="")
            except UnicodeEncodeError:
                print("\\" + hex(n)[1:])
            except IndexError:
                print("\nError: Expected function name, got EOF.")
                halt()
            openEnd = True
        elif(cmd == "r"):
            n = 0
        else:
            print("\nUnknown command %s." % cmd)
            halt()
        if(n not in range(256)):
            n = 0

import sys

if(len(sys.argv) > 1):
    from sys import exit as halt
    try:
       f = open(sys.argv[1], "r")
       code = f.read()
       f.close()
    except FileNotFoundError:
        print("Cannot find file %s." % sys.argv[1])
        halt()
    except IsADirectoryError:
        print("%s is a directory." % sys.argv[1])
        halt()
    execute(code)
    if(openEnd):
        print()
else:
    def halt():
        raise GoToInteractive()
    while True:
        code = input("n={: <3}>".format(n))
        openEnd = False
        try:
            execute(code)
        except GoToInteractive:
            pass
        if(openEnd):
            print()

