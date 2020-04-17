
"""
Michael Trani
9/4/2019
Introduction to the Software Profession:
CompSci 4500 - 001

This program plays a circle jumping game, described in section Reference 01.
The program reads a file to collect the number of circles, the number of routes, and a map of the routes formatted as such: [Source Circle][blank space][Destination Circle]
The program ensures there are not more than ten circles, and no less than two. It also ensures that the number of routes given match the quantity of routes given.
The program also ensures that no route leads to itself.

The circles are given their own class containing a list for routes, a dictionary to track the use of routes, a visit count, a boolean to check when the circle has been visited, and a unique ID for troubleshooting.
These circle classes are stored in a list for easy access. The 0th element of the list is populated with a dummy circle for easier bookkeeping.

Once populated, an infinite loop goes through the process described in Reference 01.




#### Reference 01 ####
Imagine there is white board. You draw non-intersecting circles on the board, numbered 1 to N, where N is an integer from 2 to 10. You next draw arrows from one circle to another, making sure that each circle has at least one OUT arrow and one IN arrow. Now you play the following “game:”

Place a magnetic marker in circle #1, and put a check mark in circle #1. The circle where the marker resides is called the “current circle.”
Randomly choose among the out arrows in the current circle. (If there is only one out arrow, that choice is trivial.) In this selection, all the out arrows should be equally likely to be picked.
Move the marker to the circle pointed to by the out arrow. This becomes the new current circle.
Put a check mark in the current circle.
If all the circles have at least one check mark, stop the game. If not, go to step 2 and repeat.
Your first programming assignment is to implement this game. You will use the language Python 3. You may use any IDE that you'd prefer, but you will hand in a ".py" file, not a file that is specialized to any particular IDE. I will be running your program from a command line.  The program will read from a textfile in the same directory as the executable program, and will write to another textfile in that same directory.

Let N and K be positive integers. For HW1, N is between 2 and 10 inclusive.

The input text file should be named HW1infile.txt. It should be in this form:

The first line has only the number N, the number of circles that will be used in your game.
The second line has the number K, the number of arrows you will “drawing” between the circles.
The next K lines designate the arrows, one arrow per line. Each arrow line consists of two numbers, each number being one of circles in the game. These two numbers are separated by a single blank. The first number designates the circle that is the source (back end) of the arrow; the second number designates the circle that is the destination (pointed end) of the arrow.
The circles and arrows of this game describe a directed graph, sometimes known as a “diagraph.” In order to set up the game correctly, you should describe a “strongly connected diagraph” in your input file. A diagraph is strongly connected when there is a path between any two nodes. In our game, our paths are the arrows, and our nodes are circles.

If the text in the input file does not follow the format described above, your program should end with an error message to the screen and to an output file. The output file should be a textfile. Name your output textfile “HW1lastnameOutfile.txt” where “lastname” is replaced by your last name. My output file would be called HW1millerOutfile.txt.

If the text in the input file DOES follow the description above, then you should play the game until each circle has at least one check. When that happens, the game stops. At the end of the game, you should print out to the screen, and to the output textfile, the following numbers:

The number of circles that were used for this game
The number of arrows that were used for this game
The total number of checks on all the circles combined. (Thought question: how is this related to the number of arrows traversed?)
The average number of checks in a circle marked during the game.
The maximum number of checks in any one circle. (NOTE: this number may occur in more than one circle, and that’s fine.)

#### End of Reference 01 ####



"""
import random
# Circle class to keep track of all node data
class Circles:
    def __init__(self, visited, TimesVisited, Odometer, testID):
        self.visited = visited  # Bool to check if circle has been visited, or "checked"
        self.TimesVisited = TimesVisited # Integer to track amount of times circle has been "checked"
        self.Odometer = {} # Dictionary to keep track of which routes, of "arrows" have been used
        self.RouteList = [] # List of routes, or "arrows" 
        self.testID = testID # Unique ID, or serial number


# Get amount of circles and routes from infile, create List of Circles. Create output file.
inFile = open('HW1infile.txt','r')
outFile = open('HW1traniOutfile.txt','w')

# Check Circle Count
CircleCount = int(inFile.readline())
if (CircleCount > 10 or CircleCount < 2):
    print("Circle count out of bounds from input file.")
    outFile.write("Circle count out of bounds from input file.")
    exit()

routeCount = int(inFile.readline()) # Obtain number of routes, or "arrows"
CircleSet = [] # List of Circle objects

# Create empty Circle for easier bookkeeping:
CircleSet.append(Circles(bool(True), 0, [] , ("testID: EMPTY CIRCLE") ))


#Circle List Constructor
for i in range (1, CircleCount + 1 ):
    CircleSet.append(Circles(bool(False),int(0), [] , ("testID: ",i) ))
   # print (CircleSet[i].testID)


# Route Populator reads inFile to obtain source and destination routes
# Populates a list in the Circle Class and Creates an Odometer for each route in a dictionary.

MasterOdometer = 0 # Used for counting route maps

for line in inFile:
    circle, destination = line.split()
    circle = int(circle)
    destination = int(destination)

    if (circle == destination): # Make sure no route returns to itself
        print ("Invalid Route Detected in input file.")
        outFile.write("Invalid Route Detected in input file.")
        exit()
    
    CircleSet[circle].RouteList.append(destination)
    CircleSet[circle].Odometer[destination] = 0
    MasterOdometer += 1

if (MasterOdometer != routeCount): # Make sure there is the proper amount of routes
    print ("Invalid Route Count in input file.")
    outFile.write( "Invalid Route Count in input file." )
    exit()

inFile.close()

def DataVomit(): # Formatted data check on all Circles for troubleshooting and verification 
    print(' \n Data Vomit: \n ')
    for c in range (1, CircleCount + 1):
        print ("################", CircleSet[c].testID )
        print ("Route List: \n ", CircleSet[c].RouteList )     
        print ("Odometer: \n ", CircleSet[c].Odometer      )
        print ("Visited:")
        print (CircleSet[c].visited)
        print ("Times Visited: ", CircleSet[c].TimesVisited)
        print ("      " )


# Loop checks all visited bools, a false indicates that not all nodes have been visited. 
# Since checked sequentially, Only the last node will have say on when to end the program.
def Visited( ):
    for j in range (1, CircleCount + 1):

        if CircleSet[j].visited == False:
            return False

        elif ((CircleSet[j].visited == True) and (j == (CircleCount ))):
            return True



# Checks average visit count
def TotalChecksCounter():
    Total = 0
    for c in range (1, CircleCount + 1):
        Total += CircleSet[c].TimesVisited
    return Total

	

Marker =int(1) # Game piece
Round = 1 # Iteration counter, will always be higer than the total number of visits since the initial circle is not visited in the first round.
CircleSet[1].TimesVisited = -1 # This fixes an inaccuracy in the visit counter


# Program runs on a while loop, ending when all circles have been visited - This is checked with the Visited() function.
loopLock = bool(False)
while (loopLock == False):

   
    NewMarker = random.choice(CircleSet[Marker].RouteList) # Randomly obtain next circle to visit from the current circle's route list
#    print("Source ", Marker)
#    print("Destination ", NewMarker)
    CircleSet[Marker].Odometer[NewMarker] += 1 # Increment odometer for route
    Marker = NewMarker  # Update the marker for the next round.
    CircleSet[Marker].visited = True # Update the next circle to be used. Doing this now prevents the first circle from a false positve. Don't move.
    CircleSet[Marker].TimesVisited += 1 # Increment visit count
    Round = Round + 1 # Increment the round counter before visit check for accurate round counting


    LoopLock = Visited() # Check to see if end game conditions have been met.
    if (LoopLock == True):
        break



# Data Output
print ("Circles Used: ",CircleCount)
print ("Arrows Used: ", Round)
TotalChecks = TotalChecksCounter()
AvgChecks = TotalChecks / CircleCount
print ("Total number of Checks: ",TotalChecks)
print ("Average of Checks: ",AvgChecks)

outFile.write("\n")
outFile.write( "Circles Used: " + str(CircleCount))
outFile.write("\n")
outFile.write("Arrows Used: "+ str( Round))
outFile.write("\n")
outFile.write("Total number of Checks: "+ str(TotalChecks))
outFile.write("\n")
outFile.write("Average of Checks: "+ str(AvgChecks))
outFile.write("\n")

# Checks TimesVisited varible in Circles class to determine which circle has been visited the most. 
MostVisits = int(0)
CurrentVisits = int(0)
CircleMostVisited = int(0)
for c in range (1, CircleCount + 1):
    CurrentVisits =  CircleSet[c].TimesVisited
    if(CurrentVisits > MostVisits):
        MostVisits = CurrentVisits
        CircleMostVisited = c

print ("Most checked was: "+ str(CircleMostVisited)+ " with: "+ str(MostVisits)+ " checks.")
outFile.write("Most checked was: " + str(CircleMostVisited))
outFile.write(" with a check count of: " + str(MostVisits))
outFile.write("\n")

outFile.close() # Close output file

# DataVomit() #Prints data to screen for troubleshooting and verification

exit()
