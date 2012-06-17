def go_lotto():
    import random
    lottery_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49]
    picked_numbers = ['a','b','c','d','e','f']
    for n in picked_numbers:
        if n not in lottery_numbers:
            choice = random.choice(lottery_numbers)
            while choice in picked_numbers:
                choice = random.choice(lottery_numbers)        
            picked_numbers[picked_numbers.index(n)] = choice
    return picked_numbers

print ""
num = raw_input('Enter number of lotto numbers to generate: ')
try:
    print
    print "Here are your numbers: "
    print
    for i in range(0,int(num)):        
        print go_lotto()
    print
    print "Goodluck! :-)"
except:
    print "You did not enter a number. Quitting.."


