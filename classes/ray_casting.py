import math
import pygame

from settings import TILE, HALF_FOV, RESOLUTION, NUM_RAYS, PROJ_COEFF, TEXTURE_SCALE, SCALE, HALF_HEIGHT, DELTA_ANGLE


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def RayCasting(sc, player_pos, player_angle, matrix):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV
    if RESOLUTION[0] > ox >= 0 and 0 <= oy < RESOLUTION[1]:
        for ray in range(NUM_RAYS):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001
            texture_h = None
            texture_v = None
            # check_verticals
            x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
            for i in range(0, RESOLUTION[0], TILE):
                depth_v = (x - ox) / cos_a
                yv = oy + depth_v * sin_a
                tile_v = mapping(x + dx, yv)
                if tile_v[0] < 0 or tile_v[0] >= RESOLUTION[0] or tile_v[1] < 0 or tile_v[1] >= RESOLUTION[1]:
                    break
                if len(matrix[int(tile_v[1] // TILE)][int(tile_v[0] // TILE)]) > 0:
                    texture_v = matrix[int(tile_v[1] // TILE)][int(tile_v[0] // TILE)][0].animation.current_sprite
                    break
                x += dx * TILE
            # check_horizontals
            y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, RESOLUTION[1], TILE):
                depth_h = (y - oy) / sin_a
                xh = ox + depth_h * cos_a
                tile_h = mapping(xh, y + dy)
                if tile_h[0] < 0 or tile_h[0] >= RESOLUTION[0] or tile_h[1] < 0 or tile_h[1] >= RESOLUTION[1]:
                    break
                if len(matrix[int(tile_h[1] // TILE)][int(tile_h[0] // TILE)]) > 0:
                    texture_h = matrix[int(tile_h[1] // TILE)][int(tile_h[0] // TILE)][0].animation.current_sprite
                    break
                y += dy * TILE

            # projection
            depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
            if texture is not None:
                offset = int(offset) % TILE
                depth *= math.cos(player_angle - cur_angle)
                depth = max(depth, 0.00001)
                proj_height = min(int(PROJ_COEFF / depth), RESOLUTION[1])
                wall_column = texture.subsurface((TILE - offset - 1) * TEXTURE_SCALE, 0, TEXTURE_SCALE, 50)
                wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
                sc.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))

            cur_angle += DELTA_ANGLE
