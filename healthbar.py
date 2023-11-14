from init import PG, SCREEN

HB_WIDTH = 100
HB_HEIGHT = 10
HB_BORDER = 2

HB_BG_WIDTH = HB_WIDTH + HB_BORDER * 2
HB_BG_HEIGHT = HB_HEIGHT + HB_BORDER * 2

class Healthbar ():
    def __init__(self, sprite):
        self.sprite = sprite
        self.render()
    
    def render(self):
        # ФОН
        self.image = PG.Surface((HB_BG_WIDTH, HB_BG_HEIGHT), PG.SRCALPHA)
        self.image.fill((0, 0, 0, 85))
        self.rect = self.image.get_rect()
        
        # ПОЛОСА ЗДОРОВЬЯ
        health = PG.Surface((self.sprite.hp, HB_HEIGHT), PG.SRCALPHA)
        if self.sprite.hp > 50 : health.fill((0, 255, 0, 128))
        elif self.sprite.hp > 20 : health.fill((255, 255, 0, 128))
        else : health.fill((255, 0, 0, 128))
        self.image.blit(health, (HB_BORDER, HB_BORDER))

        # РАМКА
        PG.draw.rect(self.image, (0,0,0), (HB_BORDER, HB_BORDER, HB_WIDTH, HB_HEIGHT), HB_BORDER)

    def draw(self):
        self.rect.bottom = self.sprite.rect.top
        self.rect.centerx = self.sprite.rect.centerx
        SCREEN.blit(self.image, self.rect)