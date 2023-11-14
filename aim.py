from init import SCREEN, SPRITE, SPRITES
from constants import PG

class Aim(SPRITE):
    def __init__(self):
        SPRITE.__init__(self)
        self.image = SPRITES['aim']
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.centerx, self.rect.centery = PG.mouse.get_pos()
        SCREEN.blit(self.image, self.rect)