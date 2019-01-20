import random, copy
from Cell import *
from Shapes import *

class Game:
    def __init__(self, rows, columns):
        self.GRID_ROWS = rows
        self.GRID_COLUMNS = columns
        self.grid = [[Cell(j,i) for i in range(rows)] for j in range(columns)]
        self.current = L([int(columns/2), 0])
        self.score = 0 
        for c in self.current.coordinates:
            self.grid[c[0]][c[1]].make_shape()
        self.change_queue = []

    #Returns true if shape can move in given direction, false otherwise
    #Direction is right if above 0, left if below 0, and down if exactly 0 
    def check_movement(self, direction):
        for coords in self.current.coordinates:#for each coordinate of a shape, check if it can move the direction
            if not direction == 0:
                if (coords[0]+direction < 0 or coords[0]+direction >= self.GRID_COLUMNS):#boundary check
                    return False
                if not (self.grid[coords[0]+direction][coords[1]].is_free):
                    return False
            else: #direction is 0, meaning go down
                if ( coords[1]+1 >= self.GRID_ROWS):#boundary check
                    return False
                if not (self.grid[coords[0]][coords[1]+1].is_free):
                    return False
        return True

    #Resets everything in order to begin a new game
    def clear_board(self):
        for i in range(self.GRID_ROWS):
            for j in range (self.GRID_COLUMNS):
                self.grid[j][i] = Cell(j,i)#makes all cells new
        self.change_shape()
        self.score = 0
        self.change_queue.clear()

    #Sets the current shape to a new shape at the top of the screen
    def new_shape(self):
        num = random.randint(0,5)
        if num == 0:
            return L([int(self.GRID_COLUMNS/2),0])
        elif num == 1:
            return Bar([int(self.GRID_COLUMNS/2),0])
        elif num == 2:
            return Reverse_L([int(self.GRID_COLUMNS/2),0])
        elif num == 3:
            return S([int(self.GRID_COLUMNS/2),0])
        elif num == 4:
            return Reverse_S([int(self.GRID_COLUMNS/2),0])
        else:
            return Cube([int(self.GRID_COLUMNS/2),0])
        
    #compares the coordinates of the current shape rotates and those on the grid
    #Returns true if current shape can rotate, false otherwise
    def can_rotate(self, direction):
        x = self.current.base[0]
        y = self.current.base[1]
        for t in self.current.coordinates:
            rot_coords = self.current.get_rotated_coord(direction, x, y, t[0],t[1])
            if rot_coords[0] >= self.GRID_COLUMNS or rot_coords[0] < 0:
                return False
            elif rot_coords[1] >= self.GRID_ROWS or rot_coords[1] < 0:
                return False
            elif (self.grid[rot_coords[0]][rot_coords[1]].is_free==False):
                return False
        return True

    def check_move_left(self):
        return self.check_movement(-1)
    def check_move_right(self):
        return self.check_movement(1)
    def check_move_down(self):
        return self.check_movement(0)

    #changes all coodinates of a shape depending on parameter passed
    #Validity of movement is checked before calling this function
    def move(self, direction):
        for coords in self.current.coordinates:
            self.change_queue.append([coords[0],coords[1]])
            self.grid[coords[0]][coords[1]].make_free()#make all cells of the grid indicating previous shape now free
        if not direction == 0:
            for coords in self.current.coordinates:
                coords[0]+= direction#adjust the x coordinate of each cell of a shape by the direction value        
        else:
            for coords in self.current.coordinates:
                coords[1]+= 1 #add 1 to the y coordinate of each cell of a shape
        for coords in self.current.coordinates:
            self.change_queue.append(coords)
            self.grid[coords[0]][coords[1]].make_shape()#change cells of the grid to reflect new shape positions
            
    #Sets all cells composing the current shape to frozen
    def freeze_shape(self):
        for coords in self.current.coordinates:
            self.change_queue.append(coords)
            self.grid[coords[0]][coords[1]].make_froze()

    #checks all rows for a completed row
    #frees all cells that were in completed row
    #calls function to pull all rows above completed row down
    def boom(self):
        boomed = False
        for i in range(self.GRID_ROWS):
            nowhite=True
            for j in range(self.GRID_COLUMNS):
                if (self.grid[j][i].is_free):
                    nowhite = False
            if (nowhite): #pull everything down
                self.score += 1
                boomed = True
                if (i == 0):
                    for j in range(self.GRID_COLUMNS):
                        self.change_queue.append([j, k])
                        self.grid[j][i].make_free()
                else:
                    self.shift_down(i)
        return boomed
    
    #frees up cells that previously composed the shape
    #alters cells to reflect which now make up the shape
    def turn_shape(self):
        for block in self.current.coordinates:
            self.change_queue.append(block)
            self.grid[block[0]][block[1]].make_free()
        self.current.rotate(1)
        for block in self.current.coordinates:
            self.change_queue.append(block)
            self.grid[block[0]][block[1]].make_shape()

    #checks if the new shape collides with frozen shapes.
    #If new shape collides with frozen shapes, returns true to signify game over. Otherwise returns false.        
    def check_game_over(self):
        for coords in self.current.coordinates:
            if self.grid[coords[0]][coords[1]].is_free == False:
                return True
        return False
    
    #spawns a new shape with new coordinates. Assigns new shape to current
    def change_shape(self):
        self.current = copy.deepcopy(self.new_shape())
        self.current.base = self.current.coordinates[0]
        for coords in self.current.coordinates:
            self.change_queue.append(coords)
            self.grid[coords[0]][coords[1]].make_shape()
            
    #Shifts all cells above a completed line down by one row
    def shift_down(self, boomed):
        for i in reversed(range(1, boomed+1)):
            done = True;#if all above a row being processed are free we can stop iterating
            for j in range(self.GRID_COLUMNS):
                self.change_queue.append([j, i])
                self.grid[j][i].is_free = self.grid[j][i-1].is_free
                self.grid[j][i].is_shape = self.grid[j][i-1].is_shape
                self.grid[j][i].is_base = self.grid[j][i-1].is_base
                if (self.grid[j][i].is_free == False):
                    done = False
            if (done):
                return
                             
        #top row has no above row to reference but should always be blank after
        #a row is completed
        for i in range(self.GRID_COLUMNS):
            self.change_queue.append([i, 0])
            self.grid[i][0].make_free() #clear top row 
