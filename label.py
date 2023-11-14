from init import PG, FONTS, SCREEN

class Label ():
    def __init__(self,x, y, size = 24, offset = 6, color = (0, 255, 0), align = 'center', start_text = ''):
        self.font = PG.font.Font(FONTS['main'], size)
        self.color = color
        self.align = align
        self.offset = offset
        self.x = x
        self.y = y
        self.render(start_text)
    
    def render(self, text):
        text_image = self.font.render(str(text), True, self.color)
        text_image_rect = text_image.get_rect()
        self.image = PG.Surface((text_image_rect.width + self.offset * 2, text_image_rect.height + self.offset * 2), PG.SRCALPHA)
        self.image.fill((0,0,0,128))
        self.rect = self.image.get_rect()
        self.rect.y = self.y
        if self.align == 'left' :
            text_image_rect.left = self.offset
            self.rect.x = self.x
        elif self.align == 'right' :
            text_image_rect.right = text_image_rect.width + self.offset
            self.rect.x = self.x - self.rect.width
        else:
            text_image_rect.centerx = text_image_rect.width * 0.5 + self.offset
            self.rect.x = self.x - self.rect.width * 0.5
        self.image.blit(text_image, text_image_rect)

    def draw(self):
        SCREEN.blit(self.image, self.rect)