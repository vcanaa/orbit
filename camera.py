from pymunk.vec2d import Vec2d
from pymunk.shapes import *
import vec2dext

import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *
from math import cos, sin

class Camera(object):
  def __init__(self, game):
    self.game = game
    self.pos = Vec2d.zero()
    self.prev_pos = Vec2d.zero()
    self.screen_size = Vec2d(
        self.game.screen.get_width(), self.game.screen.get_height())
    self.zoom = 1
    self.prev_zoom = self.zoom

  def update(self, pos, vel, center, dt):
    d = pos - center
    l = d.normalize_return_length()
    dist = 300
    prev_pos = self.prev_pos
    self.prev_pos = self.pos
    self.pos = (pos.mult(dist) + center.mult(l-dist)).mult(1/l)
    lerp = 0.95
    self.pos = self.pos.mult(1 - lerp) + prev_pos.mult(lerp)
    prev_zoom = self.prev_zoom
    self.prev_zoom = self.zoom
    self.zoom = min(1, 250 / (l - dist))
    lerp = 0.99
    self.zoom = self.zoom * (1-lerp) + self.prev_zoom * lerp

  def get_int_pos(self, pos):
    return ((pos - self.pos).mult(self.zoom) + self.screen_size.mult(0.5)).int_tuple

  def draw_shape(self, shape):
    if isinstance(shape, Poly):
      self.draw_poly(shape)

  def draw_poly(self, poly):
    v_list = []
    for v in poly.get_vertices():
      x,y = v.rotated(poly.body.angle) + poly.body.position
      v_list.append(
        ((x - self.pos.x) * self.zoom + self.screen_size.y / 2, 
         (y - self.pos.y) * self.zoom + self.screen_size.y / 2))

    pygame.draw.polygon(self.game.screen, THECOLORS["white"], v_list, 2)

  def draw_circle(self, circle):
    pos = self.get_int_pos(circle.body.position)
    # print(pos)
    # print(circle.radius)
    pygame.draw.circle(self.game.screen, THECOLORS["white"], pos, int(circle.radius * self.zoom), 2)