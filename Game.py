import time
import pygame
from Core import Ball, Border, Cell, AI_plate, End


def menu():
    global current_location
    screen.fill(bg_color)
    menu_buttons.draw(screen)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in menu_buttons:
                    if (obj.rect.x <= event.pos[0]
                                <= obj.rect.x + obj.width) and (obj.rect.y <= event.pos[1]
                                                                <= obj.rect.y + obj.height):
                            if obj.number == 0:
                                running = False
                                current_location = 'exit'
                                break
                            
                            else:
                                running = False
                                current_location = 'level_' + str(obj.number)
                                
            if event.type == pygame.QUIT:
                running = False
                current_location = 'exit'
                
        pygame.display.flip()


def level(number):
    global current_location
    
    running = True
    score = [0, 0]
    pause = True
    
    pause_btn.update('Paused')
    scorer.update('{}:{}'.format(*score))
    
    AI_border.rect.x = (width - AI_border.width) // 2
    player_border.rect.x = (width - player_border.width) // 2
    ball.rect.x, ball.rect.y = width // 2 - ball.radius, (height - 57) // 2 + 57
    ball.vx, ball.vy = 0, -(2 * number + 5)
    
    
    while running:
        screen.fill(lvl_color)
        pygame.draw.rect(screen, (192, 192, 192), (0, 0, width, 56))
        pygame.draw.line(screen, (0, 0, 0), (0, 56), (width, 56), 1)        
        level_sprites.draw(screen)
            
        if not pause:
            x = next(AI_border.vx)
            AI_border.rect.x += x
            AI_border.rect.x = min(max(AI_border.rect.x, 15), width - 15 - AI_border.width)
            
            goal = ball.update(borders, AI_border, player_border, AI_goal, player_goal, width, 
                               height, number)
            score[0], score[1] = score[0] + goal[0], score[1] + goal[1]        
            scorer.update('{}:{}'.format(*score))
            
            if score[0] == 5:
                running = False
                end(True)
            elif score[1] == 5:
                running = False
                end(False)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for obj in level_sprites:
                        if isinstance(obj, Cell):
                            if (obj.rect.x <= event.pos[0]
                                <= obj.rect.x + obj.width) and (obj.rect.y <= event.pos[1]
                                                                <= obj.rect.y + obj.height):
                                    if obj.number == 7:
                                        running = False
                                        current_location = 'menu'
                                        break
                                    
                                    elif obj.number == 8:
                                        pause = True
                                        obj.update('Paused')
                                        level_sprites.draw(screen)
                                        
                if event.type == pygame.MOUSEMOTION:
                    player_border.rect.x = event.pos[0] - player_border.width // 2
                    player_border.rect.x = min(max(player_border.rect.x, 15), width - 15 
                                               - player_border.width)
                    
                if event.type == pygame.QUIT:
                    running = False
                    current_location = 'exit'
        
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for obj in level_sprites:
                        if isinstance(obj, Cell):
                            if (obj.rect.x <= event.pos[0]
                                <= obj.rect.x + obj.width) and (obj.rect.y <= event.pos[1]
                                                                <= obj.rect.y + obj.height):
                                if obj.number == 7:
                                    running = False
                                    current_location = 'menu'
                                    break
                                
                                elif obj.number == 8:
                                        pause = False
                                        obj.update('Pause')
                                        level_sprites.draw(screen)
                                        
                if event.type == pygame.QUIT:
                    running = False
                    current_location = 'exit'   
                    
        pygame.display.flip()
        
        
def end(victory):
    global current_location
    
    if victory:
        screen.blit(win.image, win.rect)
    else:
        screen.blit(losing.image, losing.rect)
        
    pygame.display.flip()
     
    time.sleep(5)
    current_location = 'menu'


pygame.init()

all_sprites = pygame.sprite.Group()
menu_buttons = pygame.sprite.Group()
level_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()

bg_color = (0, 96, 192)
lvl_color = (255, 255, 255)
info_object = pygame.display.Info()
width, height = info_object.current_w, info_object.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
current_location = 'menu'

level_btns = []
for i in range(1, 6):
    level_btns.append(Cell((width - 198) // 2, i * 106 - 56, i, 'Level ' + str(i), all_sprites, 
                           menu_buttons))
    
exit_btn = Cell((width - 198) // 2, height - 106, 0, 'Exit', all_sprites, menu_buttons)
menu_btn = Cell(0, 0, 7, 'Menu', all_sprites, level_sprites)
pause_btn = Cell(250, 0, 8, 'Pause', all_sprites, level_sprites)
scorer = Cell(width - 198, 0, 9, '0:0', all_sprites, level_sprites)
b1 = Border(0, 57, 15, height, 'gray', all_sprites, borders, level_sprites)
b2 = Border(width - 15, 57, width, height, 'gray', all_sprites, borders, level_sprites)
ball = Ball(20, width // 2, height // 2, 3, 4, all_sprites, level_sprites)
player_border = Border(5, height - 45, 305, height - 15, 'blue', all_sprites, level_sprites)
AI_border = AI_plate(5, 71, 305, 101, 'blue', all_sprites, level_sprites)
AI_goal = Border(15, 57, width - 15, 72, 'green', all_sprites, level_sprites)
player_goal = Border(15, height - 15, width - 15, height, 'green', all_sprites, level_sprites)
win = End(0, 0, width, height, 'gray', 'You win!', 200, all_sprites)
losing = End(0, 0, width, height, 'gray', 'You lose!', 200, all_sprites)

while current_location != 'exit':
    if current_location == 'menu':
        menu()
    else:
        level(int(current_location.lstrip('level_')))
    
pygame.quit()    