from constants import PG, SCREEN_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

PG.init()

PG.mouse.set_visible(False)

SCREEN = PG.display.set_mode(SCREEN_SIZE)
PG.display.set_caption('Зомбари')
ICON = PG.image.load('./src/images/icon.png').convert_alpha()
PG.display.set_icon(ICON)

CLOCK = PG.time.Clock()

SPRITE = PG.sprite.Sprite

GROUP = PG.sprite.Group

SPRITES_PATH = './src/sprites/'

FONTS_PATH = './src/fonts/'

def get_sprite(image_name):
    return PG.image.load(SPRITES_PATH + image_name).convert_alpha()

def get_sprite_sheet(image_name, frame_width, frame_height, frames):
    sprite_sheet = []

    image = get_sprite(image_name)
    image_width, image_height = image.get_width(), image.get_height()
    image_x, image_y = 0, 0
    current_frame = 0

    while image_y < image_height:
        while image_x < image_width:
            frame = PG.Surface((frame_width, frame_height), PG.SRCALPHA)
            image_part = (image_x, image_y, image_x + frame_width, image_y + frame_height)
            frame.blit(image, (0, 0), image_part)
            sprite_sheet.append(frame)
            image_x += frame_width
            current_frame += 1
            if (current_frame == frames):
                return sprite_sheet
        image_x = 0
        image_y += frame_height
    return sprite_sheet

def get_tile_image(tile_name):
    tile_image = PG.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    tile = PG.image.load(SPRITES_PATH + tile_name).convert()
    tile_width, tile_height = tile.get_width(), tile.get_height()
    tile_x, tile_y = 0, 0
    while tile_y < SCREEN_HEIGHT:
        while tile_x < SCREEN_WIDTH:
            tile_image.blit(tile, (tile_x, tile_y))
            tile_x += tile_width
        tile_x = 0
        tile_y += tile_height
    return tile_image

SPRITES = {
    'aim' : get_sprite('aim_64x64px.png'),
    'player' : get_sprite('player_128x128px.png'),
    'bullet' : get_sprite('bullet_12x12px.png'),

    'zombie_0' : get_sprite('zombie_0_128x128px.png'),
    'zombie_1' : get_sprite('zombie_1_128x128px.png'),
    'zombie_2' : get_sprite('zombie_2_128x128px.png'),
    'zombie_3' : get_sprite('zombie_3_128x128px.png'),
    'zombie_4' : get_sprite('zombie_4_128x128px.png'),

    'tree_0' : get_sprite('tree_0_256x256px.png'),
    'tree_1' : get_sprite('tree_1_256x256px.png'),
    'tree_2' : get_sprite('tree_2_256x256px.png'),
    'tree_3' : get_sprite('tree_3_256x256px.png'),
    'tree_4' : get_sprite('tree_4_256x256px.png'),

    'grenade': get_sprite('grenade_64x64px.png'),

    'box_bullets': get_sprite('box_bullets_64x64px.png'),
    'box_grenades': get_sprite('box_grenades_64x64px.png'),
    'box_health': get_sprite('box_health_64x64px.png'),
}

SPRITE_SHEETS = {
    'blood'  : get_sprite_sheet('blood_max_192x192px_8frames.png', 192, 192, 8),
    'blood0' : get_sprite_sheet('blood_0_128x128px_8frames.png', 128, 128, 8),
    'blood1' : get_sprite_sheet('blood_1_128x128px_8frames.png', 128, 128, 8),
    'blood2' : get_sprite_sheet('blood_2_128x128px_10frames.png', 128, 128, 10),

    'box' : get_sprite_sheet('box_64x64px_6frames.png', 64, 64, 6),

    'big_explosion' : get_sprite_sheet('explosion_256x256px_48frames.png', 256, 256, 48),
    'min_explosion' : get_sprite_sheet('explosion_128x128px_20frames.png', 128, 128, 20),
}

BACKGROUNDS = {
    'grass' : get_tile_image('bg_grass_128x128px.png'),
    'desert' : get_tile_image('bg_desert_128x128px.png'),
    'night' : get_tile_image('bg_night_128x128px.png'),
}

FONTS = {
    'main' : FONTS_PATH + 'Jura-Regular.ttf'
}

PG.mixer.init()

SOUNDS_PATH = './src/sounds/'

def play_bg_music():
    PG.mixer.music.play()

PG.mixer.music.load(SOUNDS_PATH + 'bg.mp3')
PG.mixer.music.set_volume(0.2)

SOUND = PG.mixer.Sound # SOUND.play( sound )

alarm = PG.mixer.Sound(SOUNDS_PATH + 'alarm.mp3')
alarm.set_volume(0.5)

box_bullets = PG.mixer.Sound(SOUNDS_PATH + 'box_bullets.mp3')
box_bullets.set_volume(0.5)

box_grenades = PG.mixer.Sound(SOUNDS_PATH + 'box_grenades.mp3')
box_grenades.set_volume(0.5)

box_health = PG.mixer.Sound(SOUNDS_PATH + 'box_health.mp3')
box_health.set_volume(0.5)

new_zombie = PG.mixer.Sound(SOUNDS_PATH + 'new_zombie.mp3')
new_zombie.set_volume(0.5)

zombie_0 = PG.mixer.Sound(SOUNDS_PATH + 'z0.mp3')
zombie_0.set_volume(0.5)

zombie_1 = PG.mixer.Sound(SOUNDS_PATH + 'z1.mp3')
zombie_1.set_volume(0.5)

zombie_2 = PG.mixer.Sound(SOUNDS_PATH + 'z2.mp3')
zombie_2.set_volume(0.5)

zombie_3 = PG.mixer.Sound(SOUNDS_PATH + 'z3.mp3')
zombie_3.set_volume(0.5)

zombie_4 = PG.mixer.Sound(SOUNDS_PATH + 'z4.mp3')
zombie_4.set_volume(0.5)

reload_gun = PG.mixer.Sound(SOUNDS_PATH + 'reload.mp3')
reload_gun.set_volume(0.5)

grenade_sound = PG.mixer.Sound(SOUNDS_PATH + 'grenade.mp3')
grenade_sound.set_volume(0.5)

mix_explosion = PG.mixer.Sound(SOUNDS_PATH + 'mix_explosion.mp3')
mix_explosion.set_volume(0.5)

shut = PG.mixer.Sound(SOUNDS_PATH + 'shut.mp3')
shut.set_volume(0.1)

game_over_sound = PG.mixer.Sound(SOUNDS_PATH + 'gameover.mp3')
game_over_sound.set_volume(1)

zombies_sounds_list = [zombie_0, zombie_1, zombie_2, zombie_3, zombie_4]