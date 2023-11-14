import sys
from init import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, CLOCK, BACKGROUNDS, play_bg_music, SOUND, alarm
from constants import FPS, PG
from aim import Aim
from player import Player
from bullet import bullets_group
from grenade import grenades_group
from zombie import Zombie, zombies_group, zombies_label
from random import randint
from blood import blood_group
from explosion import explosions_group
from label import Label
from tree import trees_group, generate_trees
from box import boxes_group, generate_boxes
from bonus import bonuses_group

# КОМАНДА КОНСОЛИ ДЛЯ БИЛДА ИСХОДНИКА
# pyinstaller --onefile --name ZombieS --icon=src\images\zombies_128x128.ico -F --noconsole game.py

bg_list = list( BACKGROUNDS.keys() )
bg_index = randint(0, len(bg_list) - 1)
bg_name = bg_list[bg_index]
BG = BACKGROUNDS[bg_name]

AIM = Aim()
PLAYER = Player()

GAME_OVER = Label(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 140, 200, 40, (255, 0, 0), 'center', 'ПОТРАЧЕНО')

new_zombie_time = 5
new_zombie_frame = new_zombie_time * FPS

generate_boxes()

generate_trees()

SOUND.play( alarm )

play_bg_music()

# ИГРОВОЙ ЦИКЛ
game_loop_is = True
frame = 0
while game_loop_is:
    CLOCK.tick(FPS)
    frame += 1

    if frame % new_zombie_frame == 0 : Zombie( randint(0, 4) )

    SCREEN.blit(BG, (0, 0))

    if PLAYER.hp > 0:
        bullets_group.update()
        boxes_group.update()
        zombies_group.update(PLAYER.rect.centerx, PLAYER.rect.centery)
        PLAYER.update(AIM.rect.centerx, AIM.rect.centery)
        blood_group.update()
        trees_group.update()
        explosions_group.update()
        bonuses_group.update()
        grenades_group.update()
        AIM.update()
    else:
        GAME_OVER.draw()

    PLAYER.magazine_label.draw()
    PLAYER.grenades_label.draw()
    zombies_label.draw()

    # отрисовка на экране
    PG.display.flip()

    for event in PG.event.get():
        if event.type == PG.MOUSEBUTTONDOWN and event.button == 1 : PLAYER.on_shut(True)
        if event.type == PG.MOUSEBUTTONUP and event.button == 1 : PLAYER.on_shut(False)

        if event.type == PG.MOUSEBUTTONUP and event.button == 3 : PLAYER.throw_grenade(AIM.rect.centerx, AIM.rect.centery)

        # проверка выхода из игры (Escape или нажали на кнопку закрытия окна с игрой)
        if event.type == PG.QUIT \
        or (event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE):
            game_loop_is = False

# завершение выполнения программы
PG.quit()
sys.exit()