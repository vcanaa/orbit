from pymunk.vec2d import Vec2d

import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *
from math import cos, sin

class Planet(object):
  def __init__(self, game, pos=Vec2d(0, 0), radius=40, mass=10000):
    self.game = game
    game.objects.append(self)

    self.radius = radius
    self.mass = mass
    self.shape = self.game.create_circle(pos, radius, mass)

  def draw(self):
    self.game.camera.draw_circle(self.shape)