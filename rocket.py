from pymunk.vec2d import Vec2d

import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *

from math import cos, sin

import vec2dext

class Rocket(object):
  def __init__(self, game, pos=Vec2d(0, 0)):
    self.game = game
    game.objects.append(self)
    self.mass = 1
    self.size = Vec2d(4, 12)
    self.shape = self.game.create_box(pos, self.size, self.mass)
    self.fuel = 10
    self.fuel_rate = 0.005

  def update(self, dt, throtle, turn):
    throtle = max(0, min(1, throtle))
    turn = max(-1, min(1, turn))

    # print((throtle, turn))
    if self.fuel > 0:
      intensity = throtle * 400
      v = Vec2d(0, intensity)
      # v.rotate(self.shape.body.angle)
      self.shape.body.apply_force_at_local_point(v, Vec2d.zero()) 
      self.fuel -= intensity * dt * self.fuel_rate

      intensity = turn * 100
      v = Vec2d(intensity, 0)
      # v.rotate(self.shape.body.angle)
      self.shape.body.apply_force_at_local_point(v, Vec2d(0, -6))
      self.shape.body.apply_force_at_local_point(v.mult(-1), Vec2d(0, 6))
      self.fuel -= intensity * dt * 2 * self.fuel_rate

      if self.fuel < 0:
        self.fuel = 0

  def draw(self):
    self.game.camera.draw_shape(self.shape)
