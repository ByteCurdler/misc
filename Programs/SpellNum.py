ones = ["zero", "one", "two", "three", "four",
       "five", "six", "seven", "eight", "nine"]
tens = ["ERROR", "ERROR", "twenty", "thirty", "fourty",
       "fifty", "sixty", "seventy", "eighty", "ninety"]
teens = ["ten", "eleven", "twelve", "thirteen", "fourteen",
       "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
millions = ["thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
       "sextillion", "septillion", "octillion", "nonillion", "decillion", "undecillion",
       "duodecillion", "tredecillion", "quattuordecillion", "quindecillion", "sexdecillion",
       "septendecillion", "octodecillion", "novemdecillion", "vigintillion"]

def spell2digit(n):
    if(n in range(10)):
        return ones[n]
    elif(n in range(10, 20)):
        return teens[n-10]
    elif(n % 10 == 0):
        return tens[n // 10]
    else:
        return tens[n // 10] + "-" + ones[n % 10]

def spell3digit(n):
    if(n in range(100)):
        return spell2digit(n)
    elif(n % 100 == 0):
        return ones[n // 100] + " hundred"
    else:
        return ones[n // 100] + " hundred and " + spell2digit(n % 100)

def spellNum(n):
    comp = []
    tmp = n // 1000
    for i in millions:
        if(tmp == 0):
            break
        if(tmp % 1000 != 0):
            comp.append(spell3digit(tmp % 1000) + " " + i + " ")
        tmp = tmp // 1000
    if(tmp > 0):
        if(tmp < 1000):
            comp.append(spell3digit(tmp) + " centillion ")
        else:
            comp.append("[" + spellNum(tmp).replace("\n", "\n\t") + "] centillion ")
    if(n % 1000 != 0):
        comp.insert(0, spell3digit(n % 1000) + " ")
    tmp = "\n".join(comp[::-1])[:-1]
    return tmp[0].upper() + tmp[1:]

s2, s3, s = spell2digit, spell3digit, spellNum

if __name__ == "__main__":
    while True:
        dd = eval(input("}}} "))
        print(s(dd))
