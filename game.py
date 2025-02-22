# for checking if ships sunk, count the amount of a certain number left in grid of opposite player
# all ships sunk

#add hitgrid later if needed

import random

gameOver = False
numTurns = 0
huntMode = True
hitStack = []

def createGrid():
    grid = []
    for i in range(10):
        grid.append([])
        for j in range(10):
            grid[i].append("0")
    return grid

p1grid = createGrid()
p2grid = createGrid()

p1hits = createGrid()
p2hits = createGrid()

class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.hp = length
        self.position = []

def initShips():
    p1ship5 = Ship("carrier", 5)
    p1ship4 = Ship("battleship", 4)
    p1ship3 = Ship("submarine", 3)
    p1ship2 = Ship("cruiser", 3)
    p1ship1 = Ship("destroyer", 2)

    p1ships = [p1ship5, p1ship4, p1ship3, p1ship2, p1ship1]
    return p1ships

p1ships = initShips()
p2ships = initShips()



def OrganizePrint(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j], end = " ")
        print()


def PlaceShip(grid, ships):
    for ship in ships:
        print("Place your " + ship.name + f"({ship.length})")
        choicePos = input("Horizontal or Vertical (H or V): ")
        choiceRow = int(input("Row: "))
        choiceCol = int(input("Column: "))

        if choicePos.lower() == "h":
            while True:
                validPlacement = True
                if (10-choiceCol) < ship.length:
                    validPlacement = False
                for shipH in ships:
                    for [rp, cp] in shipH.position:
                        if rp == choiceRow and cp == choiceCol:
                            validPlacement = False
                if not validPlacement:
                    print("invalid placement")
                    choiceRow = int(input("Row: "))
                    choiceCol = int(input("Column: "))
                if validPlacement: break
            for i in range(ship.length):
                grid[choiceRow][choiceCol+i] = ship.length
                ship.position.append([choiceRow, choiceCol+i])


        if choicePos.lower() == "v":
            while True:
                validPlacement = True
                if (10-choiceRow) < ship.length:
                    validPlacement = False
                for shipV in ships:
                    for [rp, cp] in shipV.position:
                        if rp == choiceRow and cp == choiceCol:
                            validPlacement = False
                if not validPlacement:
                    print("invalid placement")
                    choiceRow = int(input("Row: "))
                    choiceCol = int(input("Column: "))
                if validPlacement: break
            for i in range(ship.length):
                grid[choiceRow+i][choiceCol] = ship.length
                ship.position.append([choiceRow+i, choiceCol])

        # OrganizePrint(grid)

def CheckIfHit(grid, row, col):
    if grid[row][col] == "X" or grid[row][col] == "M":
        # print("You have already hit this spot!")
        return True
    return False

def CheckDead(ships):
    for s in ships:
        if s.hp > 0:
            return False
    return True
            

def Turns(grid, hitgrid, ships):
    # OrganizePrint(hitgrid)
    choiceRow = int(input("Row: "))
    choiceCol = int(input("Column: "))
    while CheckIfHit(hitgrid, choiceRow, choiceCol):
        choiceRow = int(input("Row: "))
        choiceCol = int(input("Column: "))
    Hit(grid, ships, choiceRow, choiceCol)

def Setup():
    global p1ships, p2ships, p1grid, p2grid
    p1ships = initShips()
    p2ships = initShips()
    p1grid = createGrid()
    p2grid = createGrid()

    PlaceShipRandom(p1grid, p1ships)
    # print("\n\n\n\n\n\n\n")
    PlaceShipRandom(p2grid, p2ships)
    # print("\n\n\n\n\n\n\n")

def Main():
    Setup()
    while not gameOver:
        print("Player 1 turn!")
        Turns(p2grid, p2hits, p2ships)
        if CheckDead(p2ships):
            print("game over print p1 wins")
            break
        
        #maybe add blank space
        print("Player 2 turn!")
        Turns(p1grid, p1hits, p1ships) 
        if CheckDead(p1ships):
            print("game over print p2 wins")
            break

def TestMain():
    global numTurns
    Setup()
    while not gameOver:
        numTurns += 1
        # print("Player 2 turn!")
        RandomAttack(p1grid, p1ships) 
        if CheckDead(p1ships):
            # print("game over print p2 wins")
            # print(numTurns)
            break
    # OrganizePrint(p1grid)


def PlaceShipRandom(grid, ships):
    for ship in ships:
        if random.randint(0,9) < 5: #horizontal
            while True:
                choiceRow = random.randint(0,9)
                choiceCol = random.randint(0,10-ship.length)
                validPlacement = True
                for shipH in ships:
                    for offset in range(ship.length):
                        for [rp, cp] in shipH.position:
                            if rp == choiceRow and cp == choiceCol + offset:
                                validPlacement = False
                if validPlacement: break
            for i in range(ship.length):
                grid[choiceRow][choiceCol+i] = ship.length
                ship.position.append([choiceRow, choiceCol+i])


        else: #vertical
            while True:
                choiceRow = random.randint(0,10-ship.length)
                choiceCol = random.randint(0,9)
                validPlacement = True
                for shipV in ships:
                    for offset in range(ship.length):
                        for [rp, cp] in shipV.position:
                            if rp == choiceRow + offset and cp == choiceCol:
                                validPlacement = False
                if validPlacement: break
            for i in range(ship.length):
                grid[choiceRow+i][choiceCol] = ship.length
                ship.position.append([choiceRow+i, choiceCol])

    # OrganizePrint(grid)
    # print("\n\n\n\n\n\n\n\n")



def Hit(grid, ships, choiceRow, choiceCol):
    if grid[choiceRow][choiceCol] == "0":
        # print("miss.")
        grid[choiceRow][choiceCol] = "M"
        return "M"
    else:
        for ship in ships:
            for i in ship.position:
                if i[0] == choiceRow and i[1] == choiceCol:
                    ship.hp -= 1
                    # if hp == 0:
                        # print(f"You sunk my {ship.name}")
        # print("hit!", choiceRow, choiceCol)
        grid[choiceRow][choiceCol] = "X"
        return "X"

def AttemptHit(grid, ships, choiceRow, choiceCol):
    if not CheckIfHit(grid, choiceRow, choiceCol):
        return Hit(grid, ships, choiceRow, choiceCol)
    else:
        # print("duplicate hit")
        return False


def RandomAttack(grid, ships):
    global huntMode, hitStack
    if not hitStack: #huntmode
        RA = random.randint(0, 9)
        CA = random.randint(0, 9)
        while CheckIfHit(grid, RA, CA):
            RA = random.randint(0, 9)
            CA = random.randint(0, 9)

        hitShip = AttemptHit(grid, ships, RA, CA)
        if hitShip == "X":
            huntMode = False
            addNextMove(RA, CA, grid)
        # OrganizePrint(grid)
    else:
        target = hitStack.pop()
        RA, CA = target[0], target[1]
        hitShip = AttemptHit(grid, ships, target[0], target[1])
        if hitShip == "X":
            huntMode = False
            addNextMove(RA, CA, grid)
        if len(hitStack) == 0:
            huntMode = True
            
def addNextMove(RA, CA, grid): #use checkifhit func instead of condition in ()'s
    if RA != 0 and not CheckIfHit(grid, RA-1, CA):
        hitStack.append([RA-1, CA])
    if CA != 0 and not CheckIfHit(grid, RA, CA-1):
        hitStack.append([RA, CA-1])
    if RA != 9 and not CheckIfHit(grid, RA+1, CA):
        hitStack.append([RA+1, CA])
    if CA != 9 and not CheckIfHit(grid, RA, CA+1):
        hitStack.append([RA, CA+1])

    # if RA != 0 and (grid[RA-1][CA] != "X" and grid[RA-1][CA] != "M"):
    #     hitStack.append([RA-1, CA])
    # if CA != 0 and (grid[RA][CA-1] != "X" and grid[RA][CA-1] != "M"):
    #     hitStack.append([RA, CA-1])
    # if RA != 9 and (grid[RA+1][CA] != "X" and grid[RA+1][CA] != "M"):
    #     hitStack.append([RA+1, CA])
    # if CA != 9 and (grid[RA][CA+1] != "X" and grid[RA][CA+1] != "M"):
    #     hitStack.append([RA, CA+1])


sum = 0
if __name__ == "__main__":
    for i in range(10000):
        numTurns = 0
        TestMain()
        sum += numTurns
    print(sum/10000)

