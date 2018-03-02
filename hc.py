import os.path
from copy import copy
import sys
INPUT = "problems/a_example.in"
print os.path.basename(INPUT)

print sys.argv
if len(sys.argv)==2:
    INPUT = sys.argv[1]

OUTPUT = "solutions/"+os.path.basename(INPUT)

f = open(INPUT, "r")

def dist(a,b,c,d):
    return abs(a-c)+abs(b-d)
class Ride:
    def __init__(self, f, i):
        self.rideId=i
        (self.a,self.b,self.x,self.y,self.s,self.f) = readInts(f)
    def distance(self):
        return abs(self.a - self.x) + abs(self.b - self.y)
    def distanceToStart(self,x,y):
        return abs(self.a - x) + abs(self.b - y)

#states = MOVETOSTART, WAITTOSTART, MOVETODEST, IDLE
class Car:
    def __init__(self,i):
        self.x = 0
        self.y = 0
        self.state = "IDLE"
        self.ride = None
        self.assignedRides = []
        self.carId = i
    def setRide(self,r):
        self.ride = r
        if not (self.x == r.a and self.y == r.b):
            self.state = "MOVETOSTART"
        else:
            self.state = "MOVETODEST"
        self.assignedRides.append(r)

    def isAt(self, a, b):
        return self.x==a and self.y == b

    def moveToward(self, destx, desty):
        if self.x != destx:
            self.x += 1 if destx>self.x else -1
        elif self.y != desty:
            self.y += 1 if desty>self.y else -1
        #else:
            #print("tried to move but already there "+str(self.ride.rideId))

    def move(self, simStep):
        #if self.state == "IDLE":
        #    print("car is idle but tried to move")
        if self.state == "MOVETOSTART":
            if self.isAt(self.ride.a, self.ride.b):
                if self.ride.s > simStep:
                    self.state = "WAITTOSTART"
                    return
                self.state = "MOVETODEST"
            self.moveToward(self.ride.a, self.ride.b)

        if self.state == "WAITTOSTART" and self.ride.s <= simStep:
            self.state = "MOVETODEST"

        if self.state == "MOVETODEST":
            if self.isAt(self.ride.x, self.ride.y):
                self.state = "IDLE"
                return

            self.moveToward(self.ride.x, self.ride.y)
#        if self.state == "IDLE":
#            print "idle"
    def __str__(self):
        if self.state == "IDLE":
            return "car %d at (%d,%d): %s" % (self.carId, self.x,self.y, self.state)
        return "car %d at (%d,%d): %s ride : (%d,%d)->(%d,%d)" % (self.carId, self.x,self.y, self.state, self.ride.a, self.ride.b, self.ride.x, self.ride.y)



#begin parse
def readInts(f):
    line = f.readline().strip()
    n = line.split(" ")
    return map(int, n)

(rows, cols, numCars, numRides, perRideBonus, steps) = readInts(f)
rides = []

for i in range(numRides):
    r = Ride(f, i)
    rides.append(r)

rides = sorted(rides, key=lambda x:x.s)

cars = [Car(i) for i in range(numCars)]
#end parse
def whichNextRide(car, simStep):
    myrides = copy(rides)
    myrides = filter(lambda r:r.f >= simStep+ dist(car.x,car.y, r.a,r.b), myrides)

    rankings = []
    for ride in myrides:
        score = 0
        startStep = simStep + dist(car.x,car.y,r.a,r.b)
        if ride.s >= startStep:
            score += perRideBonus
        startPen = ride.s - startStep
        if startPen < 0:
            startPen = 0
        score = ride.distance() - startPen
        rankings.append((score,ride.rideId))
    rankings = sorted(rankings, key=lambda x:x[0], reverse=True)

    if len(rankings)>0:
        return rankings[0][1]
    else:
        return -1


def findClosestRideIdx(car, simStep):
    best = 99999999999999
    best_i = -1
    for i in range(min(20,len(rides))):
        d = dist(rides[i].a,rides[i].b,car.x,car.y)
        if d<best and rides[i].f >= simStep+dist(car.x,car.y, rides[i].a, rides[i].b):
            best = d
            best_i = i
    return i

def getRideIdxWidthId(id):
    for i in range(len(rides)):
        if rides[i].rideId == id:
            return i
    return -1

for simStep in range(steps):
    ridesLeft = len(rides)
    print "Step ",simStep, " Rides remain ",ridesLeft
    #clear out missed rides
    #rides = filter(lambda x:x.s>=simStep, rides)
    for car in cars:
        #print car
        if car.state == "IDLE" and len(rides)>0:
            i = findClosestRideIdx(car, simStep)
            #i = whichNextRide(car, simStep)

            if i!=-1:
                #idx = getRideIdxWidthId(i)
                ride = rides.pop(i)
                car.setRide(ride)
        car.move(simStep)

#begin output
out = open(OUTPUT, "w")
for car in cars:
    print >>out, len(car.assignedRides),
    for r in car.assignedRides:
        print >>out, r.rideId,
    print >>out
