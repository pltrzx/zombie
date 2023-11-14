from init import SCREEN, SPRITE, SPRITE_SHEETS, GROUP
from constants import PG
from random import randint

blood_group = GROUP()

class Blood(SPRITE):
    def __init__(self, x, y, direction, is_max = False):
        SPRITE.__init__(self)
        if is_max :
            self.frames = SPRITE_SHEETS['blood']
        else:
            blood_type = randint(0, 2)
            self.frames = SPRITE_SHEETS['blood' + str(blood_type)]
        self.frame = 0
        self.last_frame = len(self.frames) - 1
        self.is_next_frame = False
        self.direction = direction
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate( self.frames[0], -direction )
        self.rect = self.image.get_rect(center = (x, y))

        blood_group.add(self)

    def update(self):
        if self.is_next_frame :
            self.is_next_frame = False
            self.frame += 1
            if self.frame == self.last_frame : return self.kill()
            else : self.image = PG.transform.rotate( self.frames[self.frame], -self.direction )
        else:
            self.is_next_frame = True
        
        SCREEN.blit(self.image, self.rect)