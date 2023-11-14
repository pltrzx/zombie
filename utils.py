from math import sqrt, atan2, cos, sin, degrees, radians

def get_distance(sprite_x, sprite_y, target_x, target_y):
    dx = target_x - sprite_x
    dy = target_y - sprite_y
    return sqrt(dx * dx + dy * dy)

def turn_sprite_to_target(sprite, target_x, target_y):
    pointDirection = atan2(target_y - sprite.rect.centery, target_x - sprite.rect.centerx)
    sprite.direction = degrees(pointDirection)

def move_sprite_by_direction(sprite, path):
    angle = radians(sprite.direction)
    move_x = cos(angle) * path
    move_y = sin(angle) * path
    return (move_x, move_y)