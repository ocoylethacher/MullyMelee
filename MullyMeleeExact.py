"""
Investigate the Melee at the Mully problem more exactly than before
"""
from fractions import Fraction

def meleeOddsExactHelper(seats, i, n):
    """Calculates the odds that the last person sitting down will
    sit in their assigned seat given some starting state
    Inputs:
        seats: the current state of who's sitting where, a list
               of length n where unoccupied seats are None, while
               occupied seats are marked with the index of the
               person who sat there
        i: the index of the person to be seated next
        n: the total number of seats
    Results:
        return: the odds that the last person will sit in their
                assigned seat
    Ex.
    meleeOddsExactHelper([None, 1, 0], 2, 3) -> Fraction(0, 1)
    meleeOddsExactHelper([None, 0 None], 1, 3) -> Fraction(1, 2)
    meleeOddsExactHelper([None, 0, None, None], 1, 4) -> Fraction(1, 2)
    """
    if seats[n-1] != None: #if the last seat is already occupied, 0% chance
        return Fraction(0, 1)
    elif (i == n-1) and (seats[n-1] == None):
        return Fraction(1, 1)
    elif seats[i] == None: #if my seat is still open, sit their
        seatsCopy = seats.copy() #make a copy of the input list to prevent side effects
        seatsCopy[i] = i #sit in my seat
        return meleeOddsExactHelper(seatsCopy, i+1, n)
    else: #my seat is occupied, so need to pick randomly from available
        #find all the open seats
        openSeats = []
        index = 0
        while(index < n):
            if seats[index] == None:
                openSeats.append(index)
            index += 1
        #calculate the odds if I pick randomly for each
        f = Fraction(1, len(openSeats))
        odds = Fraction(0, 1)
        for seat in openSeats:
            seatsCopy = seats.copy()
            seatsCopy[seat] = i #sit in this open seat
            odds += f*meleeOddsExactHelper(seatsCopy, i+1, n)
        return odds

def meleeOddsExact(n):
    """Calculate the exact odds that if n people sit down to dinner
    at pre-assigned seats, but the 1st person sits in the wrong seat, that the
    last person will sit in the exact right place
    Inputs:
        n: the number of people sitting down
    Ex.
    meleeOddsExact(2) -> Fraction(0, 1)
    meleeOddsExact(3) -> Fraction(1, 4)
    meleeOddsExact(4) -> Fraction(1, 3)
    meleeOddsExact(5) -> Fraction(3, 8)
    """
    #set up the seats
    seats = []
    for i in range(n):
        seats.append(None)
    #calculate the odds for each possible starting place for the first person
    odds = Fraction(0, 1)
    f = Fraction(1, n-1)
    for i in range(n-1):
        seatsCopy = seats.copy()
        seatsCopy[i+1] = 0
        odds += f*meleeOddsExactHelper(seatsCopy, 1, n)
    return odds

def meleeOddsExactFastHelper(seats, nPre, lookup):
    """
    Calculate the exact odds that the last person sitting down
    will sit in the correct seat given the following inputs:
    Inputs:
        seats: the status of seats for the ith person and above
               None = unoccupied, 1 = occupied
        nPre: how many seats are available below the ith index
        lookup: a lookup table for previous requests
    Results:
        return: the odds that the last person will sit in the right seat
    Ex.
    meleeOddsExactFastHelper([None, None, None, 1, None], 1, {}) -> Fraction(1, 2)
    meleeOddsExactFastHelper([1, None, None, None, None], 1, {}) -> Fraction(1, 2)
    meleeOddsExactFastHelper([None, None, None, None, 1], 1, {}) -> Fraction(0, 1)
    """
    if seats[-1] != None: #if the last seat is occupied
        return Fraction(0, 1)
    elif (1 in seats) == False: #if all blocking seats are unoccupied
        return Fraction(1, 1)

    s = str(seats) + ", "+str(nPre)
    if(s in lookup): #have I already run this situation?
        return lookup[s]
    elif seats[0] == None: #if my seat is available, sit there
        seatsCopy = seats.copy()
        odds = meleeOddsExactFastHelper(seatsCopy[1:], nPre, lookup)
        lookup[s] = odds
        return odds
    else:
        seatsCopy = seats.copy()
        #how many seats are available post?
        nAvail = 0
        for seat in seatsCopy:
            if seat == None:
                nAvail += 1
        #what if I sit pre?
        f = Fraction(nPre, (nPre+nAvail))
        oddsPre = f*meleeOddsExactFastHelper(seatsCopy[1:], nPre - 1, lookup)
        #what if I sit post?
        oddsPost = Fraction(0, 1)
        for i in range(1, len(seatsCopy)):
            seat = seatsCopy[i]
            if seat == None:
                seatsCopyCopy = seatsCopy.copy()
                seatsCopyCopy[i] = 1 #sit there
                oddsPost += Fraction(1, (nPre+nAvail))*meleeOddsExactFastHelper(seatsCopyCopy[1:], nPre, lookup)
        odds = oddsPre + oddsPost
        lookup[s] = odds
        return odds

def meleeOddsExactFast(n):
    """
    Calculate the exact melee odds using a faster recursive method
    Inputs:
        n: the number of people sitting down
    Ex.
    meleeOddsExactFast(2) -> Fraction(0, 1)
    meleeOddsExactFast(3) -> Fraction(1, 4)
    meleeOddsExactFast(4) -> Fraction(1, 3)
    meleeOddsExactFast(5) -> Fraction(3, 8)
    """
    odds = Fraction(0, 1)
    lookup = {}
    for i in range(n-1):
        seats = []
        for j in range(n-1):
            if j != i:
                seats.append(None)
            else:
                seats.append(1)
        odds += Fraction(1, n-1)*meleeOddsExactFastHelper(seats, 1, lookup)
    return odds
