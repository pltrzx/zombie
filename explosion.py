from init import SCREEN, SPRITE, SPRITE_SHEETS, GROUP
from constants import PG
from random import randint
from zombie import zombies_group

explosions_group = GROUP()

class Explosion(SPRITE):
    def __init__(self, x, y, animation, distance):
        SPRITE.__init__(self)
        self.frames = SPRITE_SHEETS[animation]
        self.mid_frame = len(self.frames)//2
        self.frame = 0
        self.last_frame = len(self.frames)
        self.image = PG.transform.rotate( self.frames[0], randint(0, 360) )
        self.rect = self.image.get_rect(center = (x, y))
        self.distance = distance
        explosions_group.add(self)

    def update(self):
        self.frame += 1
        if self.frame == self.last_frame : return self.kill()
        else :
            self.image = self.frames[self.frame]
            if self.frame == self.mid_frame:
                for zombie in zombies_group.sprites():
                    zombie.explosion_hit(self.rect.centerx, self.rect.centery, self.distance)
            SCREEN.blit(self.image, self.rect)