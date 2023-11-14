from init import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE, SPRITES, GROUP
from constants import PG
from random import randint

trees_group = GROUP()

tree_probability = 10 # % на участок 128x128 пикселя
step = 128
def generate_trees():
    step_x = int(step / 2)
    step_y = int(step / 2)
    while step_y < SCREEN_HEIGHT:
        while step_x < SCREEN_WIDTH:
            if randint(0, 100) < tree_probability:
                trees_group.add( Tree(step_x, step_y) )
            step_x += step
        step_x = int(step / 2)
        step_y += step

class Tree(SPRITE):
    def __init__(self, x, y):
        SPRITE.__init__(self)
        image = SPRITES['tree_'+ str(randint(0, 4))]
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        self.image = PG.transform.rotate( image, randint(0, 360) )
        self.rect = self.image.get_rect(center = (x, y))

    def update(self):
        SCREEN.blit(self.image, self.rect)