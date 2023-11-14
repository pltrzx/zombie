from init import SCREEN, SPRITE, SPRITES, GROUP, SOUND, grenade_sound
from constants import PG, FPS
from math import sin, cos, radians
from utils import get_distance
from explosion import Explosion

grenades_group = GROUP()

min_scale = 0.5
max_scale = 1
max_size = 64
fly_time = 1 # секунд
fly_frames = round(fly_time * FPS)

class Grenade(SPRITE):
    def __init__(self, x, y, direction, target_x, target_y):
        SPRITE.__init__(self)
        self.normal_image = SPRITES['grenade']
        self.size = max_size * min_scale
        self.image = PG.transform.scale(self.normal_image, (self.size, self.size))
        self.rect = self.image.get_rect(center = (x, y))
        distance = get_distance(x, y, target_x, target_y)
        self.steps = fly_frames
        self.mid_step = round(fly_frames / 2)
        self.scale = min_scale
        self.scale_step = (max_scale - min_scale) / self.mid_step 
        step_size = distance / fly_frames
        self.direction = direction
        self.rotation_speed = 5
        angle = radians(direction)
        self.speed_x = cos(angle) * step_size
        self.speed_y = sin(angle) * step_size

        self.center_x = x
        self.center_y = y
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

        SOUND.play( grenade_sound )
        grenades_group.add(self)

    def update(self):
        self.steps -= 1
        if self.steps > 0:
            self.center_x += self.speed_x
            self.center_y += self.speed_y
            self.direction += self.rotation_speed
            if self.steps > self.mid_step : self.scale += self.scale_step
            else : self.scale -= self.scale_step
            self.size = max_size * self.scale
            image =  PG.transform.scale(self.normal_image, (self.size, self.size))
            self.image = PG.transform.rotate( image, self.direction )
            self.rect = self.image.get_rect(center = (self.center_x, self.center_y))

            self.rect.centerx = self.center_x
            self.rect.centery = self.center_y

            SCREEN.blit(self.image, self.rect)

        else:
            Explosion(self.rect.centerx, self.rect.centery, 'big_explosion', 100)
            self.kill()