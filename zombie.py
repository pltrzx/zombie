from init import SCREEN, SPRITE, SPRITES, GROUP, SOUND, new_zombie, zombies_sounds_list
from constants import PG, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_BULLET_POWER, EXPLOSION_POWER
from utils import turn_sprite_to_target, move_sprite_by_direction, get_distance
from bullet import bullets_group
from label import Label
from healthbar import Healthbar
from random import randint
from blood import blood_group, Blood

zombies_group = GROUP()

zombies_counter = 0
zombies_label= Label(SCREEN_WIDTH, 0, 24, 6, (255, 0, 0), 'right', f'Убито: {zombies_counter}')
def add_zombies_counter():
    global zombies_counter
    zombies_counter += 1
    zombies_label.render(f'Убито: {zombies_counter}')

class Zombie(SPRITE):
    def __init__(self, z_type):
        SPRITE.__init__(self)
        self.image = SPRITES['zombie_' + str(z_type)]
        self.image_rect = self.image.get_rect()
        self.rect = PG.Rect(0, 0, self.image_rect.width / 2, self.image_rect.height / 2)
        self.z_type = z_type

        side = randint(0, 3)
        if side == 0: # верх
            self.image_rect.centerx = randint(0, SCREEN_WIDTH)
            self.image_rect.bottom = 0
        elif side == 1: # право
            self.image_rect.left = SCREEN_WIDTH
            self.image_rect.centery = randint(0, SCREEN_HEIGHT)
        elif side == 2: # низ
            self.image_rect.centerx = randint(0, SCREEN_WIDTH)
            self.image_rect.top = SCREEN_HEIGHT
        else: # лево
            self.image_rect.right = 0
            self.image_rect.centery = randint(0, SCREEN_HEIGHT)
        self.center_x = self.rect.centerx = self.image_rect.centerx
        self.center_y = self.rect.centery = self.image_rect.centery
        self.direction = 0

        if z_type == 0: # простой зомби в синей майке
            self.speed = 1
            self.resistance = 3 # устойчивость (урон = сила атаки / устойчивость)
            self.power = 5 # урон, наносимый игроку
            eat_time = 2 # время задержки (секунд) после тока, как атаковал игрока

        elif z_type == 1: # быстрый зомби в красной майке
            self.speed = 2
            self.resistance = 2 # устойчивость (урон = сила атаки / устойчивость)
            self.power = 5 # урон, наносимый игроку
            eat_time = 1 # время задержки (секунд) после тока, как атаковал игрока

        elif z_type == 2: # токсичный зеленый зомби
            self.speed = 0.5
            self.resistance = 6 # устойчивость (урон = сила атаки / устойчивость)
            self.power = 20 # урон, наносимый игроку
            eat_time = 3 # время задержки (секунд) после тока, как атаковал игрока
        
        elif z_type == 3: # средний зомби в коричневой майке
            self.speed = 1
            self.resistance = 4 # устойчивость (урон = сила атаки / устойчивость)
            self.power = 5 # урон, наносимый игроку
            eat_time = 2 # время задержки (секунд) после тока, как атаковал игрока

        else: # сложный зомби-спецназовец
            self.speed = 1.5
            self.resistance = 5 # устойчивость (урон = сила атаки / устойчивость)
            self.power = 10 # урон, наносимый игроку
            eat_time = 1 # время задержки (секунд) после тока, как атаковал игрока

        self.eat_frames = round(eat_time * FPS)
        self.eat_delay = 0

        self.hp = 100
        self.healthbar = Healthbar(self)

        zombies_group.add(self)
        SOUND.play(new_zombie)

    def update(self, player_x, player_y):
        if self.eat_delay == 0:
            previous_x = self.center_x
            previous_y = self.center_y

            turn_sprite_to_target(self, player_x, player_y)
            move_x, move_y = move_sprite_by_direction(self, self.speed)
            self.center_x += move_x + move_x
            self.center_y += move_y + move_y
            self.rect.centerx = self.center_x
            self.rect.centery = self.center_y

            if len(PG.sprite.spritecollide(self, zombies_group, False)) > 1:
                self.rect.centerx = self.center_x = previous_x
                self.rect.centery = self.center_y = previous_y
        else:
            self.eat_delay -= 1

        bullets = PG.sprite.spritecollide(self, bullets_group, True)
        if len(bullets) > 0:
            for bullet in bullets:
                blood_group.add( Blood(bullet.center_x, bullet.center_y, bullet.direction) )
                self.hp -= PLAYER_BULLET_POWER / self.resistance
            if self.hp > 0:
                self.healthbar.render()
            else:
                blood_group.add( Blood(self.center_x, self.center_y, bullet.direction, True) )
                blood_group.add( Blood(self.center_x, self.center_y, bullet.direction - 45, True) )
                blood_group.add( Blood(self.center_x, self.center_y, bullet.direction + 45, True) )
                add_zombies_counter()
                return self.kill()

        self.draw()

    def eat(self):
        if self.eat_delay == 0:
            self.eat_delay = self.eat_frames
            self.hp += 5
            SOUND.play( zombies_sounds_list[self.z_type] )
            if self.hp > 100 : self.hp = 100
            self.healthbar.render()
            return self.power
        else:
            return 0

    def explosion_hit(self, x, y, radius):
        distance = get_distance(self.center_x, self.center_y, x, y)
        if distance < radius: 
            blood_group.add( Blood(self.center_x, self.center_y,  45, True) )
            blood_group.add( Blood(self.center_x, self.center_y, 165, True) )
            blood_group.add( Blood(self.center_x, self.center_y, 285, True) )
            self.hp -= EXPLOSION_POWER / self.resistance
            if self.hp > 0:
                self.healthbar.render()
            else:
                add_zombies_counter()
                return self.kill()

    def draw(self):
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        rot_image = PG.transform.rotate(self.image, -self.direction)
        rot_rect = rot_image.get_rect(center = self.rect.center)
        SCREEN.blit(rot_image, rot_rect)

        self.healthbar.draw()
