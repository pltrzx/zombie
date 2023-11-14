from init import SCREEN, SPRITE, SPRITES, SOUND, reload_gun, shut, game_over_sound, box_bullets, box_grenades, box_health
from constants import PG, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from bullet import Bullet
from grenade import Grenade
from label import Label
from utils import turn_sprite_to_target
from healthbar import Healthbar
from zombie import zombies_group
from blood import blood_group, Blood
from bonus import bonuses_group

class Player(SPRITE):
    def __init__(self):
        SPRITE.__init__(self)
        self.image = SPRITES['player']
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = 2
        self.direction = 0 # to right

        self.is_on_shut = False
        reload_time = 0.12 # sec
        self.reload_frames = round(reload_time * FPS)
        self.reload_delay = self.reload_frames

        self.magazine_max = 24
        self.magazine = self.magazine_max 
        magazine_reload_time = 2 # sec
        self.magazine_reload_frames = round(magazine_reload_time * FPS)
        self.magazine_reload_delay = self.magazine_reload_frames
        self.magazine_label_text = 'Обойма'
        self.magazine_label = Label(0, 0, 24, 6, (0, 255, 0), 'left', f'{self.magazine_label_text}: {self.magazine}')

        throw_time = 1 # sec
        self.throw_frames = round(throw_time * FPS)
        self.throw_delay = self.reload_frames
        self.grenades = 5
        self.grenades_label_text = 'Гранаты'
        self.grenades_label = Label(0, 40, 24, 6, (0, 255, 0), 'left', f'{self.grenades_label_text}: {self.grenades}')

        self.hp = 100
        self.healthbar = Healthbar(self)

    def on_shut(self, is_on_shut):
        self.is_on_shut = is_on_shut

    def update(self, aim_x, aim_y):
        turn_sprite_to_target(self, aim_x, aim_y)
        # Управление
        key = PG.key.get_pressed()
        if key[PG.K_LEFT] or key[PG.K_a]:
            self.rect.x -= self.speed
            if self.rect.left < 0 : self.rect.left = 0
        elif key[PG.K_RIGHT] or key[PG.K_d]:
            self.rect.x += self.speed
            if self.rect.right > SCREEN_WIDTH : self.rect.right = SCREEN_WIDTH
        elif key[PG.K_UP] or key[PG.K_w]:
            self.rect.y -= self.speed
            if self.rect.top < 0 : self.rect.top = 0
        elif key[PG.K_DOWN] or key[PG.K_s]:
            self.rect.y += self.speed
            if self.rect.bottom > SCREEN_HEIGHT : self.rect.bottom = SCREEN_HEIGHT 

        # ручная перезарядка
        if key[PG.K_r] and self.magazine > 0 and self.magazine != self.magazine_max:
            self.magazine = 0
            self.magazine_label.render( f'{self.magazine_label_text}: {self.magazine}' )
            SOUND.play( reload_gun )

        # Перезарядка и стрельба
        if self.reload_delay > 0:
            self.reload_delay -= 1

        elif self.magazine == 0:
            self.magazine_reload_delay -= 1
            if self.magazine_reload_delay < 1:
                self.magazine_reload_delay = self.magazine_reload_frames
                self.magazine = self.magazine_max
                self.magazine_label.render( f'{self.magazine_label_text}: {self.magazine}' )
        elif self.is_on_shut:
            SOUND.play( shut )
            self.reload_delay = self.reload_frames
            self.magazine -= 1
            if self.magazine == 0 : SOUND.play( reload_gun )
            self.magazine_label.render( f'{self.magazine_label_text}: {self.magazine}' )
            Bullet(self.rect.centerx, self.rect.centery, self.direction)

        # Ожидание броска гранаты
        if self.throw_delay > 0:
            self.throw_delay -= 1

        # проверка столкновения с зомби
        zombies = PG.sprite.spritecollide(self, zombies_group, False)
        if len(zombies) > 0:
            for zombie in zombies:
                damage = zombie.eat()
                self.hp -= damage
                if damage > 0 : blood_group.add( Blood(self.rect.centerx, self.rect.centery, zombie.direction, True) )

            if self.hp > 0:
                self.healthbar.render()
            else:
                SOUND.play( game_over_sound )

        # проверка столкновения с бонусами
        bonuses = PG.sprite.spritecollide(self, bonuses_group, False)
        if len(bonuses) > 0:
            bonus = bonuses[0]
            if bonus.type == 0 : # box_bullets
                self.magazine_max += 6
                SOUND.play( box_bullets )
            elif bonus.type == 1 : # box_grenades
                self.grenades += 3
                self.grenades_label.render( f'{self.grenades_label_text}: {self.grenades}' )
                SOUND.play( box_grenades )
            else : # box_health
                self.hp = 100
                self.healthbar.render()
                SOUND.play( box_health )
            bonus.kill()
        
        self.draw()

    def throw_grenade(self, target_x, target_y):
        if self.throw_delay == 0 and self.grenades > 0:
            self.throw_delay = self.throw_frames
            self.grenades -= 1
            Grenade(self.rect.centerx, self.rect.centery, self.direction, target_x, target_y)
            self.grenades_label.render( f'{self.grenades_label_text}: {self.grenades}' )

    def draw(self):
        # -self.direction - так как в PyGame угол отсчитывается против часовой стрелки
        rot_image = PG.transform.rotate(self.image, -self.direction)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        SCREEN.blit(rot_image, rot_rect)

        self.healthbar.draw()