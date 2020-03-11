"""
Solve a problem about diners arriving to the dining hall
put forward by Kurt Meyer
"""
from random import choice

def simulateDinerShuffleOnce(nDiners):
    """
    Simulate 1 round of the diner shuffle problem.
    Return 1 if the last diner gets to sit in their chair
    0 if they cannot
    """
    #initialize a list nDiners long to False
    seatOccupied = [False]*nDiners
    for i in range(nDiners):
        #the first person does not sit where they are assigned
        if i == 0:
            #pick a random seat that is not the first seat
            seat = pickRandomAvailableSeat(seatOccupied[1:]) + 1
            seatOccupied[seat] = True
        #if this is the last person, check if they can sit at their seat
        elif i == (nDiners - 1):
            #the last person's seat is occupied, return 0
            if seatOccupied[i] == True:
                return 0
            #the last person's seat is free, return 1
            else:
                return 1
        #everyone else tries to sit in their seat, otherwise they pick a random available seat
        else:
            if seatOccupied[i] == False:
                seatOccupied[i] = True
            else:
                seat = pickRandomAvailableSeat(seatOccupied)
                seatOccupied[seat] = True

def dinerShuffleMonteCarlo(nDiners, nRounds):
    """
    Simulate nRounds of the Diner Shuffle problem
    Return the frequency with which the last diner is able to take their seat
    """
    nSuccess = 0
    for i in range(nRounds):
        nSuccess += simulateDinerShuffleOnce(nDiners)
    return nSuccess / (1.0*nRounds)

def pickRandomAvailableSeat(occupiedSeats):
    """
    Given a list containing False and True, pick the index
    of a random seat containing False, return -1 if impossible
    """
    availableSeats = []
    for i in range(len(occupiedSeats)):
        if occupiedSeats[i] == False:
            availableSeats.append(i)
    if len(availableSeats) == 0:
        return -1
    else:
        return choice(availableSeats)

if __name__ == "__main__":
    nDiners = int(input("How many seats should there be in the Mully? "))
    nRounds = int(input("How many times would you like to simulate? "))
    print("Simulating...")
    print("Avg. Freq. of Last Seat Available: %f" % dinerShuffleMonteCarlo(nDiners, nRounds))
