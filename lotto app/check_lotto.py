import random
lottery_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49]
winnings = []
while 1:
    try:
        a = raw_input("Enter 1st winning number: ")
        if a=='':
            choice = random.choice(lottery_numbers)
            while choice in winnings:
               choice = random.choice(lottery_numbers)
            winnings.append(choice)
            print "1st winning number: "+str(choice)
            break
    

        a=int(a)        
        if a < 1 or a > 49:
            raise
        else:
            winnings.append(a)
        break
    except:
       print "You must enter a valid number between 1 - 49"

while 1:
    try:
        a = raw_input("Enter 2nd winning number: ")
        if a=='':
            choice = random.choice(lottery_numbers)
            while choice in winnings:
               choice = random.choice(lottery_numbers)
            winnings.append(choice)
            print "2nd winning number: "+str(choice)
            break
        a=int(a)
        if a < 1 or a > 49:
            raise
        else:
            winnings.append(a)
        break
    except:
       print "You must enter a valid number between 1 - 49"

while 1:
    try:
        a = raw_input("Enter 3rd winning number: ")
        if a=='':
            choice = random.choice(lottery_numbers)
            while choice in winnings:
               choice = random.choice(lottery_numbers)
            winnings.append(choice)
            print "3rd winning number: "+str(choice)
            break
        a=int(a)
        if a < 1 or a > 49:
            raise
        else:
            winnings.append(a)
        break
    except:
       print "You must enter a valid number between 1 - 49"

while 1:
    try:
        a = raw_input("Enter 4th winning number: ")
        if a=='':
            choice = random.choice(lottery_numbers)
            while choice in winnings:
               choice = random.choice(lottery_numbers)
            winnings.append(choice)
            print "4th winning number: "+str(choice)
            break
        a=int(a)
        if a < 1 or a > 49:
            raise
        else:
            winnings.append(a)
        break
    except:
       print "You must enter a valid number between 1 - 49"

while 1:
    try:
        a = raw_input("Enter 5th winning number: ")
        if a=='':
            choice = random.choice(lottery_numbers)
            while choice in winnings:
               choice = random.choice(lottery_numbers)
            winnings.append(choice)
            print "5th winning number: "+str(choice)
            break
        a=int(a)
        if a < 1 or a > 49:
            raise
        else:
            winnings.append(a)
        break
    except:
       print "You must enter a valid number between 1 - 49"

while 1:
    try:
        a = raw_input("Enter 6th winning number: ")
        if a=='':
            choice = random.choice(lottery_numbers)
            while choice in winnings:
               choice = random.choice(lottery_numbers)
            winnings.append(choice)
            print "6th winning number: "+str(choice)
            break
        a=int(a)
        if a < 1 or a > 49:
            raise
        else:
            winnings.append(a)
        break
    except:
       print "You must enter a valid number between 1 - 49"

#for i in winnings:
#    print i

number_sets = []
f = open("lotto.txt","r")
while 1:
    a = f.readline()
    if a=='':
        break
    number_sets.append(a.strip("\n\r").split(","))

results = []

for n in number_sets:
    match = []
    for m in winnings:
        #print "m: " +str(m)
        #print "n: " +str(n)
        #print "m in n: " + str(str(m) in n)
        if str(m) in n:
            match.append(str(m))
    results.append((n,match))

#print str(results)
print

for j in results:
    print j[0][0],j[0][1],j[0][2],j[0][3],j[0][4],j[0][5] + " matches " + str(j[1])


    

