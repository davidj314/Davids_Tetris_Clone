import pygame

class IO:
    def __init__(self, rows, columns):
        self.win = pygame.display.set_mode((30*columns+200, 30*rows+45))
        self.colors = {
            "END_BACKGROUND" : (0,0,0),
            "GRID_BLOCKS": (0, 0, 0),
            "END_TEXT" : (255,255,255),
            "BACKGROUND" : (0,0,255),
            "POINTS_TEXT" : (0,255,0)
            }
        self.new_game()

    #Used with all text-displaying functions
    #Displays given text with given font and color centered at a given location
    def show_text(self, font, text, center_location, color):
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = center_location
        self.win.blit(text, text_rect)
        pygame.display.update()

    #Displays controls instructios on right side of board
    def show_controls_text(self):
        controls_text = ('Left Arrow = Move Left','Right Arrow = Move Right', 'Down Arror = Move Down', 'SPACE = Rotate Shape')
        controls_font = pygame.font.Font('freesansbold.ttf', 15)
        x = self.win.get_width() - 100
        y = 90
        for controls in controls_text:
            self.show_text(controls_font, controls, (x,y), self.colors["POINTS_TEXT"])
            y += 20

    #Covers previous score and displays new score
    def update_score(self, score):
        r = pygame.Rect((0,0),(500,45))
        self.win.fill((0,0,255), r)
        self.show_points_text(score)        

    #Displays a new game, erasing old if applicable
    def new_game(self):
        self.win.fill(self.colors["BACKGROUND"])
        self.show_points_text(0)
        self.show_controls_text()

    #Displays game over screen
    def game_over(self, board):
        self.win.fill(self.colors["END_BACKGROUND"])
        game_over_font = pygame.font.Font('freesansbold.ttf', 30)
        text = "GAME OVER"
        x = self.win.get_width()/2
        y = self.win.get_height()/2
        self.show_text(game_over_font, text, (x, y), self.colors["END_TEXT"])

    #Draws a single sell of a board with given location and color
    def draw_cell (self, x, y,c):
        x_coordinate = x * 30
        y_coordinate = (y * 30)+45
        color = c
        pygame.draw.rect(self.win,(0,0,0), (x_coordinate,y_coordinate,30,30) )
        pygame.draw.rect(self.win,color,(x_coordinate+2,y_coordinate+2,26,26) )
        pygame.display.update()

    #Used in conjunction with update_score. Displays given int as the points earned
    def show_points_text(self, score):
        points_font = pygame.font.Font('freesansbold.ttf', 30)
        points_string = "Points: " + str(score)
        x = self.win.get_width()/2
        y = 45/2 
        self.show_text(points_font,points_string , (x, y), self.colors["POINTS_TEXT"])

    #Returns the desired color for a cell depending on its state
    def choose_cell_color(self, cell):
        color = (0,0,0)
        if (cell.is_shape):
            color=(0,0,255) #blue
        elif (cell.is_free):
            color = (255,255,255) #white
        else:
            color = (255,0,0)#red
        return color

    #Draws each cell needing drawn
    #After initial board drawing, only altered cells are redrawn
    def draw_board(self,game):
        color = (0,0,0)
        if (len(game.change_queue)==0): #This indicates a new board
            for i in range(game.GRID_ROWS): #i is y coord
                for j in range(game.GRID_COLUMNS): #j is x coord
                    color = self.choose_cell_color(game.grid[j][i])
                    self.draw_cell(j,i, color)
        else:
            for coords in game.change_queue: #array holds x and y coordinates of all cells needing updated
                x = coords[0]
                y = coords[1]
                color = self.choose_cell_color(game.grid[x][y])
                self.draw_cell(coords[0],coords[1],color)
            game.change_queue.clear() #All cells updated, so clear the change queue
