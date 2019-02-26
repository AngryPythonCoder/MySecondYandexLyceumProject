import math
import pygame
from itertools import chain, cycle


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, vx, vy, borders, all_sprites, *groups):
        super().__init__(all_sprites)
        
        for group in groups:
            self.add(group)
        
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx, self.vy = vx, vy
 
    def update(self, borders, AI_border, player_border, AI_goal, player_goal, width, 
               height, level):      
        self.rect = self.rect.move(self.vx, self.vy)
        
        if pygame.sprite.collide_rect(self, AI_border):
            ball_center = self.rect.x + self.radius - 0.5
            border_center = AI_border.rect.x + AI_border.width / 2 - 0.5
            
            speed = 2 * level + 5
            self.vx = max(min(2 * (ball_center - border_center) / AI_border.width * speed, 
                              speed), -speed)
            self.vy = max(1, math.sqrt(speed ** 2 - self.vx ** 2))
            self.vx, self.vy = round(self.vx), round(self.vy)
            
        if pygame.sprite.collide_rect(self, player_border):
            ball_center = self.rect.x + self.radius - 0.5
            border_center = player_border.rect.x + player_border.width / 2 - 0.5
            
            speed = 2 * level + 5
            self.vx = max(min(2 * (ball_center - border_center) / player_border.width * speed, 
                              speed), -speed)
            self.vy = -max(1, math.sqrt(speed ** 2 - self.vx ** 2))
            self.vx, self.vy = round(self.vx), round(self.vy)
            
            AI_border.logic_1(self.rect.x, self.rect.y, self.vx, self.vy, self.radius, width, 
                              height, level)
            
        if pygame.sprite.spritecollideany(self, borders):
            self.vx = -self.vx
            
        if pygame.sprite.collide_rect(self, AI_goal):
            self.rect.x, self.rect.y = width // 2 - self.radius, (height - 57) // 2 + 57
            self.vx, self.vy = -self.vx, -self.vy
            return [1, 0]
        
        elif pygame.sprite.collide_rect(self, player_goal):
            self.rect.x, self.rect.y = width // 2 - self.radius, (height - 57) // 2 + 57
            self.vx, self.vy = -self.vx, -self.vy
            AI_border.logic_1(self.rect.x, self.rect.y, self.vx, self.vy, self.radius, width, 
                              height, level)
            return [0, 1]
        
        else:
            return [0, 0]

            
class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, color, all_sprites, *groups):
        super().__init__(all_sprites)
        
        for group in groups:
            self.add(group)
        
        self.width = x2 - x1
        self.height = y2 - y1
        
        self.image = pygame.Surface([x2 - x1, y2 - y1])
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 0, x2 - x1, y2 - y1))
        
        
class End(Border):
    def __init__(self, x1, y1, x2, y2, color, text, text_size, all_sprites, *groups):
        super().__init__(x1, y1, x2, y2, color, all_sprites, *groups)
        
        self.font = pygame.font.Font(None, text_size)
        
        text = self.font.render(text, 1, (255, 255, 255))       
                           
        text_x = self.width // 2 - text.get_width() // 2
        text_y = self.height // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))          
        
        
class AI_plate(Border):
    def __init__(self, x1, y1, x2, y2, color, all_sprites, *groups):
        super().__init__(x1, y1, x2, y2, color, all_sprites, *groups)
        self.vx = cycle(iter([0]))
    
    def logic_1(self, ball_x, ball_y, ball_vx, ball_vy, ball_radius, width, height, level):
        time = (ball_y - (self.rect.y + self.height)) / abs(ball_vy)
        contact = (time * ball_vx + ball_x) // (width - 30)
        final_x = (time * ball_vx + ball_x) % (width - 30)
        
        if contact % 2 == 1:
            final_x = width - final_x - 30
            
        length = final_x - (self.rect.x + self.width // 2)
        time = int(time)
        length = int(length)
        
        try:
            lst = [length // abs(length) * (abs(length) // time)] * time
                
        except ZeroDivisionError:
            lst = [0] * time
         
        for i in range(abs(length) % time):
            lst[i] += length // abs(length)
            
        for i in range(len(lst)):
            try:
                sign = lst[i] // abs(lst[i])
            
            except ZeroDivisionError:
                sign = 0
            
            lst[i] = sign * min(2 * level, abs(lst[i]))          
            
        lst = iter(lst)
        self.vx = chain(lst, self.vx)


class Cell(pygame.sprite.Sprite):
    image = pygame.image.load('Cell.png')
    
    def __init__(self, x, y, number, btn_text, all_sprites, *groups):
        super().__init__(all_sprites)
        
        for group in groups:
            self.add(group)
        
        self.number = number       
        
        self.image = Cell.image.copy()
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.font = pygame.font.Font(None, 50)
        
        text = self.font.render(btn_text, 1, (255, 255, 255))
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()         
                           
        text_x = self.width // 2 - text.get_width() // 2
        text_y = self.height // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))    
        
    def update(self, btn_text):
        self.image = Cell.image.copy()
        text = self.font.render(btn_text, 1, (255, 255, 255))        
        
        text_x = self.image.get_width() // 2 - text.get_width() // 2
        text_y = self.image.get_height() // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))           