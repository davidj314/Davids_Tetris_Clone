class Shape:
    def __init__(self, coords):
        self.base = coords
        self.coordinates = []
        self.coordinates.append(self.base)

    #Replaces all coordinates of the shape with their rotated versions
    def rotate(self, direction):
        for index, block in enumerate(self.coordinates):
            self.coordinates[index] = self.get_rotated_coord(direction, self.coordinates[0][0], self.coordinates[0][1], block[0],block[1])
        self.base = self.coordinates[0]

    #Returns new array of an x and y coordinate, rotated from the original location
    def get_rotated_coord(self, direction, homeX, homeY, otherX,otherY):
        xDif = otherX - homeX
        yDif = otherY - homeY
        newX = 0
        newY = 0
        if (direction == 1):
            newX = homeX - yDif
            newY = homeY + xDif
        else:
            newX = homeX + yDif
            newY = homeY - xDif
        return [newX, newY]    

class L(Shape):
    def __init__(self, coords):
        Shape.__init__(self, coords)
        self.coordinates.append([coords[0]+1, coords[1]])
        self.coordinates.append([coords[0]-1, coords[1]])
        self.coordinates.append([coords[0]+1, coords[1]+1])

class Reverse_L(Shape):
    def __init__(self, coords):
        Shape.__init__(self, coords)
        self.coordinates.append([coords[0]+1, coords[1]])
        self.coordinates.append([coords[0]-1, coords[1]])
        self.coordinates.append([coords[0]-1, coords[1]+1])

class S(Shape):
    def __init__(self, coords):
        Shape.__init__(self, coords)
        self.coordinates.append([coords[0]+1, coords[1]])
        self.coordinates.append([coords[0], coords[1]+1])
        self.coordinates.append([coords[0]-1, coords[1]+1])

class Reverse_S(Shape):
    def __init__(self, coords):
        Shape.__init__(self, coords)
        self.coordinates.append([coords[0]-1, coords[1]])
        self.coordinates.append([coords[0], coords[1]+1])
        self.coordinates.append([coords[0]+1, coords[1]+1])

class Cube(Shape):
    def __init__(self, coords):
        Shape.__init__(self, coords)
        self.coordinates.append([coords[0]+1, coords[1]])
        self.coordinates.append([coords[0]+1, coords[1]+1])
        self.coordinates.append([coords[0], coords[1]+1])

class Bar(Shape):
    def __init__(self, coords):
        Shape.__init__(self, coords)
        self.coordinates.append([coords[0]+1, coords[1]])
        self.coordinates.append([coords[0]-1, coords[1]])
        self.coordinates.append([coords[0]+2, coords[1]])
