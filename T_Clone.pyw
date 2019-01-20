import time
from View import *
from Game import *

def down_event(game, view):
    run = True
    if game.check_move_down(): #if the shape can move down
        game.move(0)
        view.draw_board(game)
    else: #else, the shape is terminated
        game.freeze_shape()
        score_changed = game.boom()
        if (score_changed):
            view.update_score(game.score)
        game.change_shape()
        view.draw_board(game)
        run = not game.check_game_over()
        if (run == False ):
            time.sleep(0.5)#freezes game momentarily so end isn't so sudden
            view.game_over(game.grid)
            time.sleep(2)
            game.clear_board()
            view.new_game()
            view.draw_board(game)
    return run
    
pygame.init()
seconds_given = 1
ROWS = 15
COLUMNS = 10
game_control = Game(ROWS, COLUMNS)
view = IO(ROWS, COLUMNS)
run = True
nextmove = ''
timer = time.time() + seconds_given
view.show_controls_text()
view.draw_board(game_control)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if (timer < time.time()):
        seconds_given *= .99
        run = down_event(game_control, view)
        if (run == False):
            seconds_given = 1
        run = True
        timer = time.time()+ seconds_given
    keys = pygame.key.get_pressed()
    
    if event.type == pygame.KEYDOWN:
        if keys[pygame.K_ESCAPE]:
            nextmove = 'end'
        if keys[pygame.K_LEFT]:
            nextmove = 'left'
        if keys[pygame.K_RIGHT]:
            nextmove = 'right'
        if keys[pygame.K_SPACE]:
            nextmove = 'rotate'
        if keys[pygame.K_DOWN]:
            nextmove= 'down'       

    if event.type == pygame.KEYUP:
        if nextmove == 'end':
            run = False
        if nextmove == 'left':
            if game_control.check_move_left():
                game_control.move(-1)
                view.draw_board(game_control)
        if nextmove == 'right':
            if game_control.check_move_right():
                game_control.move(1)
                view.draw_board(game_control)
        if nextmove == 'rotate':
            if game_control.can_rotate(1):
                game_control.turn_shape()
                view.draw_board(game_control)
        if nextmove == 'down':
           run = down_event(game_control, view)
           if (run == False):
               seconds_given = 1 #reset speed for next game
               timer = time.time() + seconds_given
           run = True
        if not nextmove == '':
            nextmove = ''

pygame.quit()
        


