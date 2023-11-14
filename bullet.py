from init import SCREEN, SPRITE, SPRITES, GROUP
from constants import PG, SCREEN_WIDTH, SCREEN_HEIGHT
from math import sin, cos, radians

bullets_group = GROUP()

class Bullet(SPRITE):
    def __init__(self, x, y, direction):
        SPRITE.__init__(self)
        image = SPRITES['bullet']
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate( image, -direction )
        self.rect = self.image.get_rect(center = (x, y))
        self.direction = direction

        self.speed = 12
        angle = radians(direction)
        self.speed_x = cos(angle) * self.speed
        self.speed_y = sin(angle) * self.speed

        # смещаем пулю к краю спрайта (появление в конце дула)
        self.center_x = x + self.speed_x * (64 / self.speed)
        self.center_y = y + self.speed_y * (64 / self.speed)
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

        bullets_group.add(self)

    def update(self):
        self.center_x += self.speed_x
        self.center_y += self.speed_y
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH \
        or self.rect.centery < 0 or self.rect.centery > SCREEN_HEIGHT :
            self.kill()
        else:
            SCREEN.blit(self.image, self.rect)