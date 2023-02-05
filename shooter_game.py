#Створи власний Шутер!

from pygame import*
from random import*

class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_width, player_height, player_image, player_x, player_y, player_speed):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.width = player_width
        self.height = player_height
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global bullet_time
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE] and bullet_time == 0:
            fire.play()
            list_bullet.append(Bullet(20, 25, "bullet.png", rocket.rect.x + rocket.width / 2, rocket.rect.y, 5))
            bullet_time = 30
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

class Enemy(GameSprite):
    def set_route(self):
        self.steps_ruh = randint(1, 100)
        self.x_ruh = randint(-3, 3)
        self.y_ruh = randint(-3, 3)
        self.route = [
            [self.x_ruh, self.y_ruh, self.steps_ruh], #швидкість по горизонталі, по вертикалі, кроки
            [self.x_ruh * -1, self.y_ruh * -1, self.steps_ruh]
        ]
        self.max_points = len(self.route) - 1
        self.point = len(self.route)
        self.steps = 0

    def update(self):
        if self.steps == 0:
            self.point += 1
            if self.point > self.max_points:
                self.point = 0

            self.speed_x = self.route[self.point][0]
            self.speed_y = self.route[self.point][1]
            self.steps = self.route[self.point][2]

        self.rect.x += self.speed_x 
        self.rect.y +=  self.speed_y
        self.steps -= 1
class Asteroid(GameSprite):
    def set_route(self):
        self.x_ruh = randint(-3, 3)
        self.y_ruh = randint(1, 5)
    def update(self):
        self.rect.x += self.x_ruh
        self.rect.y += self.y_ruh

ufo_time = 0
bullet_time = 0  
list_bullet = []
list_ufo = []
list_asteroid = []
asteroid_time = 300

win_width = 700
win_height = 500

clock = time.Clock()
FPS = 60

rocket = Player(65, 80, "rocket.png", win_width / 2, win_height - 100, 3)

window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

# музика
'''mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.05)
mixer.music.play()


fire = mixer.Sound('fire.ogg')'''

game = True
while game:
    window.blit(background, (0, 0))
    if bullet_time != 0:
        bullet_time -= 1
    rocket.update()
    rocket.reset()
    
    for i in list_asteroid:
        i.update()
        i.reset()
        if i.rect.y > win_height:
            list_asteroid.remove(i)

    for i in list_bullet:
        i.update()
        i.reset()
        if i.rect.y < 0:
            list_bullet.remove(i)
            
    if ufo_time == 0:
        new_ufo = Enemy(70, 70, "ufo.png", randint(100, win_width - 200), randint(100, win_height - 400), 0)
        new_ufo.set_route()
        list_ufo. append(new_ufo)
        ufo_time += 600

    if ufo_time != 0:
        ufo_time -= 1

    if asteroid_time == 0:
        new_asteroid = Asteroid(100, 100, "asteroid.png", randint(100, 400), 0, 0)
        new_asteroid.set_route()
        list_asteroid. append(new_asteroid)
        asteroid_time += 300

    if asteroid_time != 0:
        asteroid_time -= 1

    if len(list_ufo) != 0:
        for i in list_ufo:
            i.update()
            i.reset()

    for i in list_ufo:
        for a in list_bullet:
            if sprite.collide_rect(i , a):
                list_ufo.remove(i)

    for i in list_asteroid:
        if sprite.collide_rect(i, rocket):
            game = False
        for a in list_bullet:
            if sprite.collide_rect(i , a):
                list_asteroid.remove(i)


    if len(list_ufo) == 10:
        game = False

    
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    display.update()
    clock.tick(FPS)