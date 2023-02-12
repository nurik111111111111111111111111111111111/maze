#создай игру "Лабиринт"!
from pygame import *
fps = 120
x1 = 70
y1 = 70
x2 = 140
y2 = 140
x1 = 500
y3 = 500
win_height = 700
win_width = 1300
game = True
clock = time.Clock()
BLUE = (29, 32, 76)
font.init()

phon = transform.scale(image.load('background.jpg'), (win_width, win_height))
okno = display.set_mode((win_width, win_height))
display.set_caption('огонь и вода')
okno.blit(phon,(0, 0))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        okno.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_width - 80:
            self.direction = 'left'
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def draw_wall(self):
        okno.blit(self.image, (self.rect.x, self.rect.y))

player = Player('hero.png', 5, 80, 4)
monster = Enemy('cyborg.png', 90, 200, 5)
end = GameSprite('treasure.png', 400, 120, 80)
w1 = Wall(0, 0, 5, 700)
w2 = Wall(400, 10, 15, 500)
w3 = Wall(600, 0, 15, 400)
finish = False
font = font.Font(None, 36)
win = font.render('ты выйграл', True, (255, 215, 0))

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
    if finish != True:
        okno.blit(phon, (0, 0))
        player.update()
        monster.update()
        player.reset()
        monster.reset()
        end.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3):
            finish = True
        elif sprite.collide_rect(player, end):
            okno.blit(win, (200, 200))
            finish = True
            money.play()


    display.update()
    clock.tick(fps)