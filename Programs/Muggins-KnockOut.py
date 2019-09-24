if(input("(M)uggins or (K)nockout?") == "M"):
    ops = ["+", "-", "*", "/"]
    while True:
        roll = [int(i) for i in input("\n\n\n\n\nRoll: ")]
        nums = {}
        for rot in range(3):
            opStr = "%s %%s %s %%s %s" % tuple(roll[rot:] + roll[:rot])
            for op1 in ops:
                for op2 in ops:
                    result = eval(opStr % (op1, op2))
                    if(result in range(1, 37) and result not in nums):
                        nums[int(result)] = opStr % (op1, op2)
        for i in sorted(list(nums)):
            print("%s:\t%s" % (i, nums[i]))
else:
    cache = {1:[[1]]}
    def find(n):
        try:
            if(n == 0):
                return []
            if(n in cache):
                return cache[n]
            results = []
            for i in range(1, n+1):
                for j in find(n - i):
                    tmp = [[i] + j]
                    if(len([x for x in range(len(tmp)) if tmp[x] in tmp[:x]]) == 0): #If all cells are unique
                        results += tmp
            results = [sorted(i) for i in results]
            cache[n] = [results[x] for x in range(len(results)) if results[x] not in results[:x]]
            return results
        except:
            print(results, cache)
            raise
    while True:
        roll = [int(i) for i in input("\n\n\n\n\nRoll: ")]
        total = roll[0] + roll[1] + roll[2]
        print("\nTotal: %s\n" % (total))
        combos = find(total) + [[total]]
        combos = [combos[x] for x in range(len(combos)) if combos[x] not in combos[:x]]
        
        for i in combos:
            if(len([x for x in range(len(i)) if i[x] in i[:x]]) != 0):
                continue
            print(", ".join([str(x) for x in i]))
