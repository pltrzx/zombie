from init import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE, SPRITE_SHEETS, GROUP, SOUND, mix_explosion
from constants import PG
from random import randint
from bullet import bullets_group
from explosion import Explosion
from bonus import Bonus

boxes_group = GROUP()

def generate_boxes():
    boxes_at_start = 5
    sprite_size = 64
    view_width = SCREEN_WIDTH - sprite_size * 2
    view_height = SCREEN_HEIGHT - sprite_size * 2
    while boxes_at_start > 0:
        boxes_at_start -= 1
        x = sprite_size + randint(0, view_width)
        y = sprite_size + randint(0, view_height)
        Box(x, y)

class Box(SPRITE):
    def __init__(self, x, y):
        SPRITE.__init__(self)
        self.frames = SPRITE_SHEETS['box']
        self.frame = 0
        self.hp = 60
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.angle = randint(0, 360)
        self.image = PG.transform.rotate( self.frames[0], self.angle )
        self.rect = self.image.get_rect(center = (x, y))

        boxes_group.add(self)

    def update(self):
        if PG.sprite.spritecollide(self, bullets_group, True):
            self.hp -= 5
            if self.hp > 50 : self.frame = 0
            elif self.hp > 40 : self.frame = 1
            elif self.hp > 30 : self.frame = 2
            elif self.hp > 20 : self.frame = 3
            elif self.hp > 10 : self.frame = 4
            elif self.hp > 0 : self.frame = 5
            else :
                SOUND.play( mix_explosion )
                Bonus(self.rect.centerx, self.rect.centery, self.angle)
                Explosion(self.rect.centerx, self.rect.centery, 'min_explosion', 50)
                return self.kill()

            self.image = PG.transform.rotate( self.frames[self.frame], self.angle )

        SCREEN.blit(self.image, self.rect)