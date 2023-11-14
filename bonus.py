from init import SCREEN, SPRITE, SPRITES, GROUP
from constants import PG
from random import randint
#from game import PLAYER

bonuses_group = GROUP()

class Bonus(SPRITE):
    def __init__(self, x, y, direction):
        SPRITE.__init__(self)
        self.type = randint(0, 2)
        if self.type == 0 : self.image = SPRITES['box_bullets']
        elif self.type == 1 : self.image = SPRITES['box_grenades']
        else : self.image = SPRITES['box_health']
        self.image = PG.transform.rotate( self.image, direction )
        self.rect = self.image.get_rect(center = (x, y))

        bonuses_group.add(self)

    def update(self):
        SCREEN.blit(self.image, self.rect)